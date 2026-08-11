"""Deterministic structured queries over loaded FMEA documents."""

from __future__ import annotations

from collections.abc import Mapping
from math import fsum
from typing import Any

from src.faiss_knowledge_base import FmeaFaissKnowledgeBase


QUERY_RESULT_LIMIT = 20

NUMERIC_FIELDS = {
    "severity_before",
    "occurrence_before",
    "detection_before",
    "rpn_before",
    "severity_after",
    "occurrence_after",
    "detection_after",
    "rpn_after",
}

SORTABLE_FIELDS = NUMERIC_FIELDS | {"source_excel_row"}

TEXT_SEARCH_FIELDS = (
    "functional_requirement",
    "potential_failure_mode",
    "potential_failure_effect",
    "potential_causes",
    "current_process_controls",
    "recommended_actions",
)

RESULT_FIELDS = (
    "document_id",
    "process_code",
    "process",
    "functional_requirement",
    "potential_failure_mode",
    "potential_failure_effect",
    "potential_causes",
    "current_process_controls",
    "recommended_actions",
    "severity_before",
    "occurrence_before",
    "detection_before",
    "rpn_before",
    "severity_after",
    "occurrence_after",
    "detection_after",
    "rpn_after",
    "owner_date",
)


class FmeaQueryError(ValueError):
    """Raised when a structured FMEA query is invalid."""


class FmeaQueryService:
    """Query metadata already loaded by the FAISS knowledge bases.

    All matching rows are evaluated so ``total_matches`` is exact. Only the
    first 20 sorted records are returned to keep tool responses bounded.
    """

    def __init__(
        self,
        knowledge_bases: Mapping[str, FmeaFaissKnowledgeBase],
    ) -> None:
        self.knowledge_bases = {
            process_code.upper(): knowledge_base
            for process_code, knowledge_base in knowledge_bases.items()
        }

    def query_records(
        self,
        *,
        processes: list[str] | None = None,
        document_id: str | None = None,
        text_contains: str | None = None,
        severity_min: float | None = None,
        severity_max: float | None = None,
        occurrence_min: float | None = None,
        occurrence_max: float | None = None,
        detection_min: float | None = None,
        detection_max: float | None = None,
        rpn_min: float | None = None,
        rpn_max: float | None = None,
        sort_by: str = "rpn_before",
        sort_order: str = "desc",
    ) -> dict[str, Any]:
        selected, unknown = self._select_processes(processes)
        resolved_sort_by = str(sort_by).strip().lower()
        if resolved_sort_by not in SORTABLE_FIELDS:
            raise FmeaQueryError(f"不支援的排序欄位：{sort_by}")
        resolved_sort_order = str(sort_order).strip().lower()
        if resolved_sort_order not in {"asc", "desc"}:
            raise FmeaQueryError("sort_order 只能是 asc 或 desc")

        numeric_filters = {
            "severity_before": (severity_min, severity_max),
            "occurrence_before": (occurrence_min, occurrence_max),
            "detection_before": (detection_min, detection_max),
            "rpn_before": (rpn_min, rpn_max),
        }
        self._validate_numeric_filters(numeric_filters)

        resolved_document_id = (document_id or "").strip().casefold()
        resolved_text = (text_contains or "").strip().casefold()
        matches: list[dict[str, Any]] = []

        for process_code in selected:
            for document in self.knowledge_bases[process_code].documents:
                metadata = dict(document.metadata)
                metadata.setdefault("document_id", document.document_id)
                metadata.setdefault("process_code", process_code)
                if resolved_document_id and document.document_id.casefold() != resolved_document_id:
                    continue
                if resolved_text and not _contains_text(metadata, resolved_text):
                    continue
                if not _matches_numeric_filters(metadata, numeric_filters):
                    continue
                matches.append(
                    {
                        field: metadata.get(field)
                        for field in RESULT_FIELDS
                    }
                )

        matches = _sort_records(
            matches,
            field=resolved_sort_by,
            descending=resolved_sort_order == "desc",
        )
        returned = matches[:QUERY_RESULT_LIMIT]
        return {
            "total_matches": len(matches),
            "returned_count": len(returned),
            "limit": QUERY_RESULT_LIMIT,
            "has_more": len(matches) > QUERY_RESULT_LIMIT,
            "processes": selected,
            "unknown_processes": unknown,
            "sort_by": resolved_sort_by,
            "sort_order": resolved_sort_order,
            "records": returned,
        }

    def summarize_rpn_by_process(
        self,
        *,
        processes: list[str] | None = None,
    ) -> dict[str, Any]:
        """Return an exact average RPN for every selected process."""

        selected, unknown = self._select_processes(processes)
        summaries: list[dict[str, Any]] = []
        for process_code in selected:
            documents = self.knowledge_bases[process_code].documents
            values = [
                document.metadata.get("rpn_before")
                for document in documents
                if _is_number(document.metadata.get("rpn_before"))
            ]
            average_rpn = round(fsum(values) / len(values), 2) if values else None
            summaries.append(
                {
                    "process": process_code,
                    "average_rpn": average_rpn,
                    "records_with_rpn": len(values),
                    "total_records": len(documents),
                }
            )

        summaries.sort(
            key=lambda summary: (
                summary["average_rpn"] is not None,
                summary["average_rpn"] or 0,
            ),
            reverse=True,
        )
        return {
            "processes": selected,
            "unknown_processes": unknown,
            "summaries": summaries,
        }

    def _select_processes(
        self,
        processes: list[str] | None,
    ) -> tuple[list[str], list[str]]:
        if not processes:
            return sorted(self.knowledge_bases), []
        requested = list(dict.fromkeys(str(item).strip().upper() for item in processes if str(item).strip()))
        selected = [item for item in requested if item in self.knowledge_bases]
        unknown = [item for item in requested if item not in self.knowledge_bases]
        return selected, unknown

    @staticmethod
    def _validate_numeric_filters(
        filters: dict[str, tuple[float | None, float | None]],
    ) -> None:
        for field, (minimum, maximum) in filters.items():
            if minimum is not None and not _is_number(minimum):
                raise FmeaQueryError(f"{field} 最小值必須是數字")
            if maximum is not None and not _is_number(maximum):
                raise FmeaQueryError(f"{field} 最大值必須是數字")
            if minimum is not None and maximum is not None and minimum > maximum:
                raise FmeaQueryError(f"{field} 最小值不可大於最大值")


def _contains_text(metadata: dict[str, Any], query: str) -> bool:
    return any(query in str(metadata.get(field) or "").casefold() for field in TEXT_SEARCH_FIELDS)


def _matches_numeric_filters(
    metadata: dict[str, Any],
    filters: dict[str, tuple[float | None, float | None]],
) -> bool:
    for field, (minimum, maximum) in filters.items():
        if minimum is None and maximum is None:
            continue
        value = metadata.get(field)
        if not _is_number(value):
            return False
        if minimum is not None and value < minimum:
            return False
        if maximum is not None and value > maximum:
            return False
    return True


def _sort_records(
    records: list[dict[str, Any]],
    *,
    field: str,
    descending: bool,
) -> list[dict[str, Any]]:
    present = [record for record in records if _is_number(record.get(field))]
    missing = [record for record in records if not _is_number(record.get(field))]
    present.sort(key=lambda record: record[field], reverse=descending)
    return [*present, *missing]


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)
