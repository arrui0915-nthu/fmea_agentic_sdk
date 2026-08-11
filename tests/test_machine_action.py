import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.machine_action import (
    MACHINE_ID,
    SETPOINT_IDS,
    MachineActionService,
    MachineActionValidationError,
    PvdMachineSimulator,
    parse_machine_action,
)
from src.my_splitter import load_all_documents


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def make_action(
    button_1: float = 10,
    button_2: float = 20,
    button_3: float = 30,
) -> dict[str, object]:
    return {
        "machine_id": MACHINE_ID,
        "setpoints": {
            "button_1": button_1,
            "button_2": button_2,
            "button_3": button_3,
        },
    }


def test_parse_machine_action_accepts_dict_and_json_string() -> None:
    action = make_action()

    parsed_dict = parse_machine_action(action)
    parsed_json = parse_machine_action(json.dumps(action))

    assert parsed_dict == action
    assert parsed_json == action
    assert parsed_dict is not action
    assert parsed_dict["setpoints"] is not action["setpoints"]


@pytest.mark.parametrize(
    "action, message",
    [
        ("not json", "not valid JSON"),
        ("[]", "JSON object"),
        ([], "JSON string or dictionary"),
        ({"machine_id": "OTHER", "setpoints": {}}, "machine_id"),
        ({"machine_id": MACHINE_ID, "setpoints": []}, "setpoints must be an object"),
        (
            {
                "machine_id": MACHINE_ID,
                "setpoints": {"button_1": 1, "button_2": 2},
            },
            "missing: button_3",
        ),
        (
            {
                "machine_id": MACHINE_ID,
                "setpoints": {
                    "button_1": 1,
                    "button_2": 2,
                    "button_3": 3,
                    "button_4": 4,
                },
            },
            "unexpected: button_4",
        ),
    ],
)
def test_parse_machine_action_rejects_invalid_shapes(
    action: object,
    message: str,
) -> None:
    with pytest.raises(MachineActionValidationError, match=message):
        parse_machine_action(action)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "value, message",
    [
        (True, "boolean is not allowed"),
        ("10", "must be a number"),
        (-0.1, "between 0 and 100"),
        (100.1, "between 0 and 100"),
        (float("nan"), "finite number"),
        (float("inf"), "finite number"),
    ],
)
def test_parse_machine_action_rejects_unsafe_setpoint_values(
    value: object,
    message: str,
) -> None:
    action = make_action()
    action["setpoints"]["button_2"] = value  # type: ignore[index]

    with pytest.raises(MachineActionValidationError, match=message):
        parse_machine_action(action)


def test_parse_machine_action_accepts_inclusive_range_boundaries() -> None:
    parsed = parse_machine_action(make_action(0, 50.5, 100))

    assert parsed["setpoints"] == {
        "button_1": 0,
        "button_2": 50.5,
        "button_3": 100,
    }


def test_simulator_starts_at_zero_and_applies_atomically() -> None:
    simulator = PvdMachineSimulator()

    assert simulator.snapshot() == {
        "machine_id": MACHINE_ID,
        "setpoints": {setpoint_id: 0 for setpoint_id in SETPOINT_IDS},
        "history": [],
    }

    result = simulator.apply("PVD-0001", make_action(), "wf-1:PVD-0001")

    assert result == {
        "sequence": 1,
        "machine_id": MACHINE_ID,
        "document_id": "PVD-0001",
        "idempotency_key": "wf-1:PVD-0001",
        "source": "workflow",
        "before": {"button_1": 0, "button_2": 0, "button_3": 0},
        "after": {"button_1": 10, "button_2": 20, "button_3": 30},
        "changed": True,
        "changed_setpoints": ["button_1", "button_2", "button_3"],
    }
    snapshot = simulator.snapshot()
    assert snapshot["setpoints"] == result["after"]
    assert snapshot["history"] == [result]
    assert simulator.history() == [result]


def test_apply_with_same_values_records_changed_false() -> None:
    simulator = PvdMachineSimulator()

    result = simulator.apply("PVD-0001", make_action(0, 0, 0), "same")

    assert result["changed"] is False
    assert result["changed_setpoints"] == []
    assert len(simulator.history()) == 1


def test_duplicate_idempotency_key_returns_original_without_new_record() -> None:
    simulator = PvdMachineSimulator()
    first = simulator.apply("PVD-0001", make_action(1, 2, 3), "duplicate")

    duplicate = simulator.apply("PVD-9999", make_action(90, 91, 92), "duplicate")

    assert duplicate == first
    assert simulator.snapshot()["setpoints"] == first["after"]
    assert simulator.history() == [first]


def test_invalid_action_does_not_partially_update_state_or_history() -> None:
    simulator = PvdMachineSimulator()
    before = simulator.snapshot()
    invalid = make_action()
    invalid["setpoints"]["button_3"] = 101  # type: ignore[index]

    with pytest.raises(MachineActionValidationError):
        simulator.apply("PVD-0001", invalid, "invalid")

    assert simulator.snapshot() == before


def test_manual_apply_uses_same_validation_and_history() -> None:
    simulator = PvdMachineSimulator()

    result = simulator.apply_manual(
        {"button_1": 4, "button_2": 5, "button_3": 6},
        idempotency_key="manual-1",
    )

    assert result["document_id"] == "MANUAL"
    assert result["source"] == "manual"
    assert result["after"] == {"button_1": 4, "button_2": 5, "button_3": 6}
    assert simulator.snapshot()["setpoints"] == result["after"]


def test_reset_restores_initial_state_and_clears_idempotency() -> None:
    simulator = PvdMachineSimulator()
    simulator.apply("PVD-0001", make_action(1, 2, 3), "reusable")

    reset_snapshot = simulator.reset()

    assert reset_snapshot == simulator.snapshot()
    assert reset_snapshot["setpoints"] == {
        "button_1": 0,
        "button_2": 0,
        "button_3": 0,
    }
    assert reset_snapshot["history"] == []

    replay = simulator.apply("PVD-0002", make_action(7, 8, 9), "reusable")
    assert replay["document_id"] == "PVD-0002"
    assert replay["sequence"] == 1


def test_returned_data_cannot_mutate_internal_state() -> None:
    simulator = PvdMachineSimulator()
    result = simulator.apply("PVD-0001", make_action(), "isolated")
    snapshot = simulator.snapshot()

    result["after"]["button_1"] = 99
    snapshot["setpoints"]["button_2"] = 99
    snapshot["history"].clear()

    fresh = simulator.snapshot()
    assert fresh["setpoints"] == {"button_1": 10, "button_2": 20, "button_3": 30}
    assert len(fresh["history"]) == 1


def test_concurrent_updates_have_a_single_atomic_history_order() -> None:
    simulator = PvdMachineSimulator()

    def update(index: int) -> dict[str, object]:
        value = index % 101
        return simulator.apply(
            f"PVD-{index:04d}",
            make_action(value, value, value),
            f"concurrent-{index}",
        )

    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(update, range(1, 41)))

    history = simulator.history()
    assert len(history) == 40
    assert [record["sequence"] for record in history] == list(range(1, 41))
    assert history[0]["before"] == {
        "button_1": 0,
        "button_2": 0,
        "button_3": 0,
    }
    for previous, current in zip(history, history[1:]):
        assert current["before"] == previous["after"]
    assert simulator.snapshot()["setpoints"] == history[-1]["after"]


def test_real_pvd_row_applies_its_three_demo_setpoints() -> None:
    documents = load_all_documents(PROJECT_ROOT / "data" / "markdown")
    simulator = PvdMachineSimulator()
    service = MachineActionService(
        {
            "PVD": {
                "process_code": "PVD",
                "documents": documents["PVD"],
            }
        },
        simulator,
    )

    result = service.execute(
        "PVD-0001",
        allowed_document_ids=["PVD-0001"],
        idempotency_key="workflow-1:apply_machine_action:PVD-0001",
    )

    assert result["before"] == {
        "button_1": 0,
        "button_2": 0,
        "button_3": 0,
    }
    assert result["after"] == {
        "button_1": 10,
        "button_2": 20,
        "button_3": 30,
    }


def make_document(
    document_id: str,
    process_code: str,
    machine_action: object = None,
) -> SimpleNamespace:
    return SimpleNamespace(
        document_id=document_id,
        metadata={
            "document_id": document_id,
            "process_code": process_code,
            "machine_action": machine_action,
        },
    )


def make_knowledge_base(
    process_code: str,
    *documents: SimpleNamespace,
) -> SimpleNamespace:
    return SimpleNamespace(process_code=process_code, documents=list(documents))


def test_service_executes_action_mapped_by_stable_pvd_document_id() -> None:
    simulator = PvdMachineSimulator()
    service = MachineActionService(
        {
            "PVD": make_knowledge_base(
                "PVD",
                make_document("PVD-0001", "PVD", json.dumps(make_action(11, 22, 33))),
            )
        },
        simulator,
    )

    result = service.execute(
        "PVD-0001",
        allowed_document_ids=["PVD-0001"],
        idempotency_key="workflow:PVD-0001",
    )

    assert result["document_id"] == "PVD-0001"
    assert result["after"] == {"button_1": 11, "button_2": 22, "button_3": 33}
    assert simulator.snapshot()["setpoints"] == result["after"]


def test_service_rejects_document_not_returned_by_current_retrieval() -> None:
    service = MachineActionService(
        {
            "PVD": make_knowledge_base(
                "PVD",
                make_document("PVD-0001", "PVD", make_action()),
            )
        },
        PvdMachineSimulator(),
    )

    with pytest.raises(PermissionError, match="was not retrieved"):
        service.execute(
            "PVD-0001",
            allowed_document_ids=["PVD-0002"],
            idempotency_key="not-allowed",
        )


def test_service_rejects_unknown_allowed_document_id() -> None:
    service = MachineActionService({}, PvdMachineSimulator())

    with pytest.raises(LookupError, match="unknown document_id"):
        service.execute(
            "PVD-9999",
            allowed_document_ids=["PVD-9999"],
            idempotency_key="unknown",
        )


@pytest.mark.parametrize("machine_action", [None, "", "   ", {}])
def test_service_rejects_pvd_document_without_machine_action(
    machine_action: object,
) -> None:
    service = MachineActionService(
        {
            "PVD": make_knowledge_base(
                "PVD",
                make_document("PVD-0001", "PVD", machine_action),
            )
        },
        PvdMachineSimulator(),
    )

    with pytest.raises(LookupError, match="no configured machine_action"):
        service.execute(
            "PVD-0001",
            allowed_document_ids=["PVD-0001"],
            idempotency_key="unset",
        )


def test_service_rejects_non_pvd_even_if_it_has_an_action() -> None:
    # A malformed action on another process is intentionally not parsed at startup.
    service = MachineActionService(
        {
            "ECD": make_knowledge_base(
                "ECD",
                make_document("ECD-0001", "ECD", "not-json"),
            )
        },
        PvdMachineSimulator(),
    )

    with pytest.raises(ValueError, match="only available for PVD"):
        service.execute(
            "ECD-0001",
            allowed_document_ids=["ECD-0001"],
            idempotency_key="wrong-process",
        )


def test_service_fails_fast_for_invalid_configured_pvd_action() -> None:
    invalid = make_action()
    invalid["setpoints"]["button_1"] = 101  # type: ignore[index]

    with pytest.raises(
        MachineActionValidationError,
        match="document PVD-0001 has invalid machine_action",
    ):
        MachineActionService(
            {
                "PVD": make_knowledge_base(
                    "PVD",
                    make_document("PVD-0001", "PVD", invalid),
                )
            },
            PvdMachineSimulator(),
        )


def test_service_uses_document_metadata_process_over_knowledge_base_key() -> None:
    service = MachineActionService(
        {
            "PVD": make_knowledge_base(
                "PVD",
                make_document("ECD-0001", "ECD", make_action()),
            )
        },
        PvdMachineSimulator(),
    )

    with pytest.raises(ValueError, match="ECD-0001 is ECD"):
        service.execute(
            "ECD-0001",
            allowed_document_ids=["ECD-0001"],
            idempotency_key="metadata-process",
        )


def test_service_supports_mapping_shaped_knowledge_bases_and_documents() -> None:
    action = make_action(3, 6, 9)
    service = MachineActionService(
        {
            "PVD": {
                "process_code": "PVD",
                "documents": [
                    {
                        "document_id": "PVD-0003",
                        "metadata": {
                            "process_code": "PVD",
                            "machine_action": action,
                        },
                    }
                ],
            }
        },
        PvdMachineSimulator(),
    )

    result = service.execute(
        "PVD-0003",
        allowed_document_ids=(document_id for document_id in ["PVD-0003"]),
        idempotency_key="duck-typed",
    )

    assert result["after"] == action["setpoints"]


def test_service_rejects_duplicate_stable_document_ids() -> None:
    duplicate = make_document("PVD-0001", "PVD", make_action())

    with pytest.raises(ValueError, match="duplicate document_id: PVD-0001"):
        MachineActionService(
            {
                "first": make_knowledge_base("PVD", duplicate),
                "second": make_knowledge_base("PVD", duplicate),
            },
            PvdMachineSimulator(),
        )


def test_service_preserves_simulator_idempotency() -> None:
    simulator = PvdMachineSimulator()
    service = MachineActionService(
        {
            "PVD": make_knowledge_base(
                "PVD",
                make_document("PVD-0001", "PVD", make_action(1, 2, 3)),
                make_document("PVD-0002", "PVD", make_action(7, 8, 9)),
            )
        },
        simulator,
    )

    first = service.execute(
        "PVD-0001",
        allowed_document_ids=["PVD-0001", "PVD-0002"],
        idempotency_key="shared-key",
    )
    duplicate = service.execute(
        "PVD-0002",
        allowed_document_ids=["PVD-0001", "PVD-0002"],
        idempotency_key="shared-key",
    )

    assert duplicate == first
    assert simulator.history() == [first]
