from dataclasses import dataclass

import pytest

from src.fmea_query import FmeaQueryError, FmeaQueryService, QUERY_RESULT_LIMIT
from src.fmea_tools import FMEA_TOOLS, FmeaToolDispatcher
from src.my_splitter import FmeaDocument


@dataclass
class FakeKnowledgeBase:
    documents: list[FmeaDocument]


class FakeMachineActionService:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def execute(
        self,
        document_id: str,
        *,
        allowed_document_ids: list[str],
        idempotency_key: str,
    ) -> dict[str, object]:
        self.calls.append(
            {
                "document_id": document_id,
                "allowed_document_ids": allowed_document_ids,
                "idempotency_key": idempotency_key,
            }
        )
        return {"document_id": document_id, "changed": True}


def _document(
    number: int,
    *,
    process: str = "TAZMO",
    rpn: int | None = None,
    failure_mode: str = "膜厚異常",
) -> FmeaDocument:
    document_id = f"{process}-{number:04d}"
    metadata = {
        "document_id": document_id,
        "process_code": process,
        "process": process,
        "functional_requirement": "維持製程穩定",
        "potential_failure_mode": failure_mode,
        "potential_failure_effect": "產品異常",
        "potential_causes": "設備偏移",
        "current_process_controls": "定期點檢",
        "recommended_actions": "縮短保養週期",
        "severity_before": 8,
        "occurrence_before": 4,
        "detection_before": 3,
        "rpn_before": number if rpn is None else rpn,
        "severity_after": None,
        "occurrence_after": None,
        "detection_after": None,
        "rpn_after": None,
        "owner_date": "",
        "source_excel_row": number + 2,
    }
    return FmeaDocument(document_id=document_id, content="row", metadata=metadata)


def _service(*documents: FmeaDocument) -> FmeaQueryService:
    grouped: dict[str, list[FmeaDocument]] = {}
    for document in documents:
        grouped.setdefault(str(document.metadata["process_code"]), []).append(document)
    return FmeaQueryService(
        {
            process: FakeKnowledgeBase(items)  # type: ignore[arg-type]
            for process, items in grouped.items()
        }
    )


def test_query_evaluates_every_row_but_returns_only_twenty() -> None:
    service = _service(*(_document(number) for number in range(1, 26)))

    result = service.query_records(processes=["tazmo"])

    assert result["total_matches"] == 25
    assert result["returned_count"] == QUERY_RESULT_LIMIT == 20
    assert result["has_more"] is True
    assert [record["rpn_before"] for record in result["records"]] == list(
        range(25, 5, -1)
    )


def test_query_applies_process_numeric_and_text_filters() -> None:
    service = _service(
        _document(1, process="TAZMO", rpn=150),
        _document(2, process="TAZMO", rpn=240, failure_mode="溫度過高"),
        _document(3, process="PVD", rpn=300, failure_mode="溫度過高"),
    )

    result = service.query_records(
        processes=["TAZMO"],
        text_contains="溫度",
        rpn_min=200,
    )

    assert result["total_matches"] == 1
    assert result["records"][0]["document_id"] == "TAZMO-0002"


def test_missing_numeric_value_does_not_match_a_numeric_filter() -> None:
    service = _service(_document(1, rpn=None))
    service.knowledge_bases["TAZMO"].documents[0].metadata["rpn_before"] = None

    result = service.query_records(rpn_min=1)

    assert result["total_matches"] == 0


def test_invalid_range_is_rejected() -> None:
    service = _service(_document(1))

    with pytest.raises(FmeaQueryError, match="最小值不可大於最大值"):
        service.query_records(rpn_min=300, rpn_max=100)


def test_unknown_process_is_reported_without_falling_back_to_all() -> None:
    service = _service(_document(1))

    result = service.query_records(processes=["UNKNOWN"])

    assert result["total_matches"] == 0
    assert result["processes"] == []
    assert result["unknown_processes"] == ["UNKNOWN"]


def test_rpn_summary_uses_every_numeric_record_and_sorts_processes() -> None:
    service = _service(
        _document(1, process="PVD", rpn=100),
        _document(2, process="PVD", rpn=200),
        _document(3, process="PI", rpn=60),
        _document(4, process="PI", rpn=None),
    )
    service.knowledge_bases["PI"].documents[1].metadata["rpn_before"] = None

    result = service.summarize_rpn_by_process()

    assert result == {
        "processes": ["PI", "PVD"],
        "unknown_processes": [],
        "summaries": [
            {
                "process": "PVD",
                "average_rpn": 150.0,
                "records_with_rpn": 2,
                "total_records": 2,
            },
            {
                "process": "PI",
                "average_rpn": 60.0,
                "records_with_rpn": 1,
                "total_records": 2,
            },
        ],
    }


def test_rpn_summary_honors_process_filter_and_reports_unknowns() -> None:
    service = _service(
        _document(1, process="PVD", rpn=100),
        _document(2, process="PI", rpn=60),
    )

    result = service.summarize_rpn_by_process(processes=["pvd", "unknown"])

    assert result["processes"] == ["PVD"]
    assert result["unknown_processes"] == ["UNKNOWN"]
    assert [item["process"] for item in result["summaries"]] == ["PVD"]


def test_dispatcher_exposes_query_without_a_configurable_limit() -> None:
    service = _service(_document(1))
    dispatcher = FmeaToolDispatcher(service)

    result = dispatcher.execute("query_fmea_records", {"processes": ["TAZMO"]})
    properties = FMEA_TOOLS[0]["function"]["parameters"]["properties"]

    assert result["returned_count"] == 1
    assert "limit" not in properties


def test_dispatcher_exposes_exact_rpn_summary_tool() -> None:
    dispatcher = FmeaToolDispatcher(
        _service(
            _document(1, process="PVD", rpn=100),
            _document(2, process="PVD", rpn=200),
        )
    )

    result = dispatcher.execute("summarize_rpn_by_process", {})
    tool = next(
        item
        for item in FMEA_TOOLS
        if item["function"]["name"] == "summarize_rpn_by_process"
    )

    assert result["summaries"][0]["average_rpn"] == 150.0
    assert set(tool["function"]["parameters"]["properties"]) == {"processes"}
    assert tool["function"]["parameters"]["additionalProperties"] is False


def test_machine_action_tool_schema_accepts_only_a_document_id() -> None:
    tool = next(
        tool
        for tool in FMEA_TOOLS
        if tool["function"]["name"] == "apply_machine_action"
    )
    parameters = tool["function"]["parameters"]

    assert parameters["required"] == ["document_id"]
    assert set(parameters["properties"]) == {"document_id"}
    assert parameters["additionalProperties"] is False


def test_dispatcher_passes_machine_action_security_context() -> None:
    machine_service = FakeMachineActionService()
    dispatcher = FmeaToolDispatcher(
        _service(_document(1, process="PVD")),
        machine_action_service=machine_service,  # type: ignore[arg-type]
    )

    result = dispatcher.execute(
        "apply_machine_action",
        {"document_id": "pvd-0001"},
        workflow_id="workflow-123",
        retrieved_document_ids=["PVD-0001", "PVD-0002"],
        perceived_intent="machine_control",
    )

    assert result == {"document_id": "PVD-0001", "changed": True}
    assert machine_service.calls == [
        {
            "document_id": "PVD-0001",
            "allowed_document_ids": ["PVD-0001", "PVD-0002"],
            "idempotency_key": (
                "workflow-123:apply_machine_action:PVD-0001"
            ),
        }
    ]


def test_dispatcher_rejects_machine_action_without_service_or_intent() -> None:
    query_service = _service(_document(1, process="PVD"))
    without_service = FmeaToolDispatcher(query_service)

    with pytest.raises(RuntimeError, match="not configured"):
        without_service.execute(
            "apply_machine_action",
            {"document_id": "PVD-0001"},
            workflow_id="workflow-123",
            retrieved_document_ids=["PVD-0001"],
            perceived_intent="machine_control",
        )

    machine_service = FakeMachineActionService()
    dispatcher = FmeaToolDispatcher(
        query_service,
        machine_action_service=machine_service,  # type: ignore[arg-type]
    )
    with pytest.raises(PermissionError, match="machine_control"):
        dispatcher.execute(
            "apply_machine_action",
            {"document_id": "PVD-0001"},
            workflow_id="workflow-123",
            retrieved_document_ids=["PVD-0001"],
            perceived_intent="internal_fmea",
        )
    assert machine_service.calls == []


def test_dispatcher_rejects_unregistered_tools() -> None:
    dispatcher = FmeaToolDispatcher(_service(_document(1)))

    with pytest.raises(ValueError, match="不允許的工具"):
        dispatcher.execute("delete_fmea_record", {})
