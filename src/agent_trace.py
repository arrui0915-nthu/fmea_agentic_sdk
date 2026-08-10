"""Build a serialisable, UI-safe execution trace from Agentic SDK events."""

from __future__ import annotations

from copy import deepcopy
from time import perf_counter
from typing import Any, Callable, Mapping


TRACE_STAGES: tuple[tuple[str, str], ...] = (
    ("perceive", "理解問題"),
    ("plan", "決定處理方式"),
    ("retrieve", "搜尋 FMEA 資料"),
    ("action", "產生回答"),
    ("reflect", "檢查回答"),
)

_SUMMARY_METADATA_KEYS = (
    "processes",
    "top_k",
    "hit_count",
    "cross_table",
    "candidate_count",
    "accepted_count",
    "duplicate_count",
    "threshold",
    "ok",
    "model",
    "tool_names",
    "needs_process_clarification",
    "verdict",
    "reason",
    "strategy",
    "suggestion",
    "correction_count",
    "max_corrections",
    "will_retry",
    "correction_exhausted",
)


class AgentTraceRecorder:
    """Record public stage facts without retaining SDK state or raw output."""

    def __init__(self, clock: Callable[[], float] = perf_counter) -> None:
        self._clock = clock
        self._started_at = clock()
        self._stage_started_at: dict[str, float] = {}
        self._trace: dict[str, Any] = {
            "status": "running",
            "duration_ms": None,
            "input_tokens": 0,
            "output_tokens": 0,
            "stages": [
                {
                    "module": module,
                    "label": label,
                    "status": "pending",
                    "duration_ms": None,
                    "module_class": None,
                    "visit_count": 0,
                    "next_module": None,
                    "fields": [],
                    "summary": {},
                    "usage": None,
                    "reason": None,
                    "attempts": [],
                }
                for module, label in TRACE_STAGES
            ],
        }

    @property
    def snapshot(self) -> dict[str, Any]:
        """Return a detached snapshot suitable for Streamlit session state."""

        return deepcopy(self._trace)

    def record_stage(self, event: Mapping[str, Any]) -> dict[str, Any]:
        """Record one SDK stage event and return its safe public projection."""

        now = self._clock()
        module = str(event.get("module") or event.get("stage") or "").strip()
        phase = str(event.get("phase") or "").strip()
        visit_count = _safe_int(event.get("visit_count"), default=1)
        visit_id = str(event.get("visit_id") or f"{module}:{visit_count}")
        stage = self._stage(module)
        if stage is None:
            stage = {
                "module": module or "unknown",
                "label": str(event.get("label") or module or "Unknown"),
                "status": "pending",
                "duration_ms": None,
                "module_class": None,
                "visit_count": 0,
                "next_module": None,
                "fields": [],
                "summary": {},
                "usage": None,
                "reason": None,
                "attempts": [],
            }
            self._trace["stages"].append(stage)

        stage["label"] = str(event.get("label") or stage["label"])
        stage["module_class"] = _optional_text(event.get("module_class"))
        stage["visit_count"] = visit_count

        if phase == "start":
            self._stage_started_at[visit_id] = now
            stage["status"] = "running"
            stage["duration_ms"] = None
            stage["next_module"] = None
            stage["fields"] = []
            stage["summary"] = {}
            stage["usage"] = None
            stage["reason"] = None
        elif phase == "finish":
            stage["status"] = "complete"
            stage["duration_ms"] = self._duration_ms(visit_id, now)
            stage["next_module"] = _optional_text(event.get("next_module"))
            stage["fields"] = _safe_fields(event.get("fields"))
            stage["summary"] = _output_summary(event.get("output"))
            stage["usage"] = _output_usage(event.get("output"))
            self._add_usage(stage["usage"])
            stage["attempts"].append(_attempt_snapshot(stage))
        elif phase == "abort":
            stage["status"] = "error"
            stage["duration_ms"] = self._duration_ms(visit_id, now)
            stage["reason"] = _optional_text(event.get("reason"))
            stage["attempts"].append(_attempt_snapshot(stage))

        return {
            "type": "stage",
            "phase": phase,
            "status": stage["status"],
            "module": stage["module"],
            "label": stage["label"],
            "module_class": stage["module_class"],
            "visit_count": visit_count,
            "next_module": stage["next_module"],
            "duration_ms": stage["duration_ms"],
            "fields": deepcopy(stage["fields"]),
            "summary": deepcopy(stage["summary"]),
            "usage": deepcopy(stage["usage"]),
            "reason": stage["reason"],
        }

    def finish(self, *, failed: bool = False, reason: str | None = None) -> None:
        """Close the trace and mark unvisited stages as skipped."""

        now = self._clock()
        for stage in self._trace["stages"]:
            if stage["status"] == "pending":
                stage["status"] = "skipped"
            elif failed and stage["status"] == "running":
                stage["status"] = "error"
                stage["reason"] = reason
        self._trace["status"] = "error" if failed else "complete"
        self._trace["duration_ms"] = max(0, round((now - self._started_at) * 1000))

    def _stage(self, module: str) -> dict[str, Any] | None:
        return next(
            (stage for stage in self._trace["stages"] if stage["module"] == module),
            None,
        )

    def _duration_ms(self, visit_id: str, now: float) -> int | None:
        started_at = self._stage_started_at.pop(visit_id, None)
        if started_at is None:
            return None
        return max(0, round((now - started_at) * 1000))

    def _add_usage(self, usage: dict[str, Any] | None) -> None:
        if not usage:
            return
        self._trace["input_tokens"] += _safe_int(usage.get("input_tokens"))
        self._trace["output_tokens"] += _safe_int(usage.get("output_tokens"))


def _safe_fields(raw_fields: object) -> list[dict[str, Any]]:
    if not isinstance(raw_fields, list):
        return []
    fields: list[dict[str, Any]] = []
    for item in raw_fields[:20]:
        if not isinstance(item, Mapping):
            continue
        field = str(item.get("field") or "").strip()
        if not field:
            continue
        fields.append({"field": field, "value": _safe_value(item.get("value"))})
    return fields


def _attempt_snapshot(stage: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "visit_count": stage.get("visit_count"),
        "status": stage.get("status"),
        "duration_ms": stage.get("duration_ms"),
        "next_module": stage.get("next_module"),
        "fields": deepcopy(stage.get("fields") or []),
        "summary": deepcopy(stage.get("summary") or {}),
        "usage": deepcopy(stage.get("usage")),
        "reason": stage.get("reason"),
    }


def _output_summary(output: object) -> dict[str, Any]:
    context_updates = _get_value(output, "context_updates")
    if not isinstance(context_updates, (list, tuple)):
        return {}
    summary: dict[str, Any] = {}
    for entry in context_updates:
        metadata = _get_value(entry, "metadata")
        if not isinstance(metadata, Mapping):
            continue
        for key in _SUMMARY_METADATA_KEYS:
            if key in metadata:
                summary[key] = _safe_value(metadata[key])
    return summary


def _output_usage(output: object) -> dict[str, Any] | None:
    payload = _get_value(output, "payload")
    if not isinstance(payload, Mapping):
        return None
    raw_usage = payload.get("_llm_usage")
    if not isinstance(raw_usage, Mapping):
        return None
    return {
        "model": _optional_text(raw_usage.get("model")),
        "input_tokens": _safe_int(raw_usage.get("input_tokens")),
        "output_tokens": _safe_int(raw_usage.get("output_tokens")),
    }


def _get_value(source: object, key: str) -> object:
    if isinstance(source, Mapping):
        return source.get(key)
    return getattr(source, key, None)


def _safe_value(value: object, *, depth: int = 0) -> Any:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value if len(value) <= 240 else value[:237] + "…"
    if depth >= 2:
        return str(value)[:240]
    if isinstance(value, Mapping):
        return {
            str(key): _safe_value(item, depth=depth + 1)
            for key, item in list(value.items())[:12]
        }
    if isinstance(value, (list, tuple, set)):
        return [_safe_value(item, depth=depth + 1) for item in list(value)[:12]]
    return str(value)[:240]


def _safe_int(value: object, default: int = 0) -> int:
    try:
        return int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
