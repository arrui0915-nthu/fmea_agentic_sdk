"""OpenAI tool definitions and the allow-listed FMEA tool dispatcher."""

from __future__ import annotations

from typing import Any

from src.fmea_query import FmeaQueryService


QUERY_FMEA_RECORDS_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "query_fmea_records",
        "description": (
            "依製程、document ID、文字或 S/O/D/RPN 數值條件精確查詢公司 FMEA 紀錄。"
            "適用於門檻、範圍、排序、計數與列出紀錄；固定最多回傳 20 筆。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "processes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "製程代碼；省略代表查詢全部製程。",
                },
                "document_id": {
                    "type": "string",
                    "description": "完整且唯一的 FMEA document ID。",
                },
                "text_contains": {
                    "type": "string",
                    "description": "在失效模式、效應、原因、控制及建議措施中做不分大小寫的文字包含查詢。",
                },
                "severity_min": {"type": "number"},
                "severity_max": {"type": "number"},
                "occurrence_min": {"type": "number"},
                "occurrence_max": {"type": "number"},
                "detection_min": {"type": "number"},
                "detection_max": {"type": "number"},
                "rpn_min": {"type": "number"},
                "rpn_max": {"type": "number"},
                "sort_by": {
                    "type": "string",
                    "enum": [
                        "severity_before",
                        "occurrence_before",
                        "detection_before",
                        "rpn_before",
                        "severity_after",
                        "occurrence_after",
                        "detection_after",
                        "rpn_after",
                        "source_excel_row",
                    ],
                    "default": "rpn_before",
                },
                "sort_order": {
                    "type": "string",
                    "enum": ["asc", "desc"],
                    "default": "desc",
                },
            },
            "additionalProperties": False,
        },
    },
}

FMEA_TOOLS = [QUERY_FMEA_RECORDS_TOOL]


class FmeaToolDispatcher:
    """Execute only explicitly registered FMEA tools."""

    def __init__(self, query_service: FmeaQueryService) -> None:
        self._handlers = {
            "query_fmea_records": query_service.query_records,
        }

    def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        handler = self._handlers.get(name)
        if handler is None:
            raise ValueError(f"不允許的工具：{name}")
        return handler(**arguments)
