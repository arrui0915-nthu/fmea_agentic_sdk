"""Validated, thread-safe simulator for the PVD demo machine."""

from __future__ import annotations

import json
import math
from collections.abc import Iterable, Mapping
from copy import deepcopy
from numbers import Real
from threading import RLock
from typing import Any
from uuid import uuid4


MACHINE_ID = "PVD-DEMO-01"
SETPOINT_IDS = ("button_1", "button_2", "button_3")
SETPOINT_MIN = 0
SETPOINT_MAX = 100

MachineActionInput = str | dict[str, Any]
MachineAction = dict[str, Any]


class MachineActionValidationError(ValueError):
    """Raised when a machine action is malformed or unsafe to execute."""


def parse_machine_action(action: MachineActionInput) -> MachineAction:
    """Parse and validate a PVD machine action.

    The returned value is a new canonical dictionary, so later mutations to the
    caller's input cannot change the validated action.
    """

    if isinstance(action, str):
        try:
            parsed = json.loads(action)
        except json.JSONDecodeError as exc:
            raise MachineActionValidationError(
                f"machine_action is not valid JSON: {exc.msg}"
            ) from exc
    elif isinstance(action, dict):
        parsed = action
    else:
        raise MachineActionValidationError(
            "machine_action must be a JSON string or dictionary"
        )

    if not isinstance(parsed, dict):
        raise MachineActionValidationError("machine_action must be a JSON object")

    machine_id = parsed.get("machine_id")
    if machine_id != MACHINE_ID:
        raise MachineActionValidationError(
            f"machine_id must be {MACHINE_ID!r}"
        )

    setpoints = parsed.get("setpoints")
    if not isinstance(setpoints, dict):
        raise MachineActionValidationError("setpoints must be an object")

    expected_keys = set(SETPOINT_IDS)
    actual_keys = set(setpoints)
    if actual_keys != expected_keys:
        missing = sorted(expected_keys - actual_keys)
        extra = sorted(actual_keys - expected_keys, key=str)
        details: list[str] = []
        if missing:
            details.append(f"missing: {', '.join(missing)}")
        if extra:
            details.append(f"unexpected: {', '.join(map(str, extra))}")
        detail = f" ({'; '.join(details)})" if details else ""
        raise MachineActionValidationError(
            f"setpoints must contain exactly {', '.join(SETPOINT_IDS)}{detail}"
        )

    normalized_setpoints: dict[str, Real] = {}
    for setpoint_id in SETPOINT_IDS:
        value = setpoints[setpoint_id]
        if isinstance(value, bool) or not isinstance(value, Real):
            raise MachineActionValidationError(
                f"{setpoint_id} must be a number (boolean is not allowed)"
            )
        try:
            is_finite = math.isfinite(value)
        except OverflowError:
            # Very large integers are finite but will fail the range check below.
            is_finite = True
        if not is_finite:
            raise MachineActionValidationError(
                f"{setpoint_id} must be a finite number"
            )
        if value < SETPOINT_MIN or value > SETPOINT_MAX:
            raise MachineActionValidationError(
                f"{setpoint_id} must be between {SETPOINT_MIN} and {SETPOINT_MAX}"
            )
        normalized_setpoints[setpoint_id] = value

    return {
        "machine_id": MACHINE_ID,
        "setpoints": dict(normalized_setpoints),
    }


class PvdMachineSimulator:
    """In-memory PVD machine with atomic updates and idempotent execution."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._setpoints: dict[str, Real] = self._zero_setpoints()
        self._history: list[dict[str, Any]] = []
        self._idempotent_results: dict[str, dict[str, Any]] = {}

    def snapshot(self) -> dict[str, Any]:
        """Return an isolated snapshot of current state and execution history."""

        with self._lock:
            return {
                "machine_id": MACHINE_ID,
                "setpoints": deepcopy(self._setpoints),
                "history": deepcopy(self._history),
            }

    def history(self) -> list[dict[str, Any]]:
        """Return an isolated copy of the ordered execution history."""

        with self._lock:
            return deepcopy(self._history)

    def apply(
        self,
        document_id: str,
        action: MachineActionInput,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Atomically apply a validated action for a retrieved PVD document."""

        return self._apply(
            document_id=document_id,
            action=action,
            idempotency_key=idempotency_key,
            source="workflow",
        )

    def apply_manual(
        self,
        setpoints: dict[str, Any],
        *,
        idempotency_key: str | None = None,
    ) -> dict[str, Any]:
        """Apply values supplied directly by the Streamlit machine controls."""

        key = idempotency_key or f"manual:{uuid4()}"
        action = {
            "machine_id": MACHINE_ID,
            "setpoints": setpoints,
        }
        return self._apply(
            document_id="MANUAL",
            action=action,
            idempotency_key=key,
            source="manual",
        )

    def reset(self) -> dict[str, Any]:
        """Restore the initial state and clear history and idempotency records."""

        with self._lock:
            self._setpoints = self._zero_setpoints()
            self._history.clear()
            self._idempotent_results.clear()
            return {
                "machine_id": MACHINE_ID,
                "setpoints": deepcopy(self._setpoints),
                "history": [],
            }

    def _apply(
        self,
        *,
        document_id: str,
        action: MachineActionInput,
        idempotency_key: str,
        source: str,
    ) -> dict[str, Any]:
        normalized_document_id = self._required_string(document_id, "document_id")
        normalized_key = self._required_string(idempotency_key, "idempotency_key")
        normalized_action = parse_machine_action(action)

        with self._lock:
            cached = self._idempotent_results.get(normalized_key)
            if cached is not None:
                return deepcopy(cached)

            before = deepcopy(self._setpoints)
            after = deepcopy(normalized_action["setpoints"])
            changed_setpoints = [
                setpoint_id
                for setpoint_id in SETPOINT_IDS
                if before[setpoint_id] != after[setpoint_id]
            ]
            result = {
                "sequence": len(self._history) + 1,
                "machine_id": MACHINE_ID,
                "document_id": normalized_document_id,
                "idempotency_key": normalized_key,
                "source": source,
                "before": before,
                "after": after,
                "changed": bool(changed_setpoints),
                "changed_setpoints": changed_setpoints,
            }

            # State, history, and idempotency cache are changed under one lock.
            self._setpoints = deepcopy(after)
            stored_result = deepcopy(result)
            self._history.append(stored_result)
            self._idempotent_results[normalized_key] = deepcopy(stored_result)
            return deepcopy(stored_result)

    @staticmethod
    def _required_string(value: object, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string")
        return value.strip()

    @staticmethod
    def _zero_setpoints() -> dict[str, Real]:
        return {setpoint_id: 0 for setpoint_id in SETPOINT_IDS}


class MachineActionService:
    """Resolve validated PVD recipes by stable document ID and execute them safely."""

    def __init__(
        self,
        knowledge_bases: Mapping[str, Any] | Iterable[Any],
        simulator: PvdMachineSimulator,
    ) -> None:
        self._simulator = simulator
        self._document_processes: dict[str, str] = {}
        self._actions_by_document_id: dict[str, MachineAction] = {}

        for fallback_process, knowledge_base in self._iter_knowledge_bases(
            knowledge_bases
        ):
            knowledge_base_process = self._normalize_process_code(
                self._field(knowledge_base, "process_code", fallback_process)
            )
            documents = self._field(knowledge_base, "documents", ())
            if documents is None:
                continue
            try:
                iterator = iter(documents)
            except TypeError as exc:
                raise ValueError("knowledge base documents must be iterable") from exc

            for document in iterator:
                metadata = self._field(document, "metadata", {})
                document_id = self._required_document_id(
                    self._field(
                        document,
                        "document_id",
                        self._field(metadata, "document_id", None),
                    )
                )
                process_code = self._normalize_process_code(
                    self._field(metadata, "process_code", knowledge_base_process)
                )

                if document_id in self._document_processes:
                    raise ValueError(f"duplicate document_id: {document_id}")
                self._document_processes[document_id] = process_code

                machine_action = self._field(metadata, "machine_action", None)
                if process_code != "PVD" or self._is_empty_action(machine_action):
                    continue

                try:
                    parsed_action = parse_machine_action(machine_action)
                except MachineActionValidationError as exc:
                    raise MachineActionValidationError(
                        f"document {document_id} has invalid machine_action: {exc}"
                    ) from exc
                self._actions_by_document_id[document_id] = parsed_action

    def execute(
        self,
        document_id: str,
        *,
        allowed_document_ids: Iterable[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Execute a configured action only when its row was retrieved this turn."""

        normalized_document_id = self._required_document_id(document_id)
        allowed = self._normalize_allowed_document_ids(allowed_document_ids)
        if normalized_document_id not in allowed:
            raise PermissionError(
                f"document {normalized_document_id} was not retrieved in this request"
            )

        process_code = self._document_processes.get(normalized_document_id)
        if process_code is None:
            raise LookupError(f"unknown document_id: {normalized_document_id}")
        if process_code != "PVD":
            raise ValueError(
                f"machine actions are only available for PVD documents: "
                f"{normalized_document_id} is {process_code or 'unknown process'}"
            )

        action = self._actions_by_document_id.get(normalized_document_id)
        if action is None:
            raise LookupError(
                f"document {normalized_document_id} has no configured machine_action"
            )

        return self._simulator.apply(
            normalized_document_id,
            action,
            idempotency_key,
        )

    @staticmethod
    def _field(source: object, name: str, default: object = None) -> object:
        if isinstance(source, Mapping):
            return source.get(name, default)
        return getattr(source, name, default)

    @classmethod
    def _iter_knowledge_bases(
        cls,
        knowledge_bases: Mapping[str, Any] | Iterable[Any],
    ) -> Iterable[tuple[object, Any]]:
        if isinstance(knowledge_bases, Mapping):
            return knowledge_bases.items()
        try:
            iterator = iter(knowledge_bases)
        except TypeError as exc:
            raise ValueError("knowledge_bases must be a mapping or iterable") from exc
        return ((None, knowledge_base) for knowledge_base in iterator)

    @staticmethod
    def _normalize_process_code(value: object) -> str:
        return str(value or "").strip().upper()

    @staticmethod
    def _required_document_id(value: object) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("document_id must be a non-empty string")
        return value.strip()

    @staticmethod
    def _is_empty_action(value: object) -> bool:
        if value is None:
            return True
        if isinstance(value, str):
            return not value.strip()
        if isinstance(value, Mapping):
            return not value
        return False

    @classmethod
    def _normalize_allowed_document_ids(
        cls,
        values: Iterable[str],
    ) -> set[str]:
        if isinstance(values, (str, bytes)):
            raise ValueError("allowed_document_ids must be an iterable of document IDs")
        try:
            return {cls._required_document_id(value) for value in values}
        except TypeError as exc:
            raise ValueError(
                "allowed_document_ids must be an iterable of document IDs"
            ) from exc
