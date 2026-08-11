"""OpenAI tool definitions and the allow-listed FMEA tool dispatcher."""

from __future__ import annotations

from typing import Any

from src.conversation_report import SessionReportService
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

GENERATE_SESSION_REPORT_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "generate_session_report",
        "description": (
            "當使用者明確要求整理、產生或下載本次對話報告時使用。"
            "根據完整對話整理摘要、發現、行動與待確認事項，並產生含完整對話附錄的 HTML 報告。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "精簡的繁體中文報告標題。"},
                "objective": {"type": "string", "description": "本次對話的主要目的。"},
                "processes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "本次對話實際涉及的製程代碼。",
                },
                "executive_summary": {
                    "type": "string",
                    "description": "忠於對話內容的管理摘要，不可加入未討論的事實。",
                },
                "key_findings": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "本次對話的重要發現；沒有則傳空陣列。",
                },
                "action_items": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "對話中形成的建議或待辦；沒有則傳空陣列。",
                },
                "open_questions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "尚待確認的事項；沒有則傳空陣列。",
                },
            },
            "required": [
                "title",
                "objective",
                "processes",
                "executive_summary",
                "key_findings",
                "action_items",
                "open_questions",
            ],
            "additionalProperties": False,
        },
    },
}

FMEA_TOOLS = [QUERY_FMEA_RECORDS_TOOL, GENERATE_SESSION_REPORT_TOOL]


class FmeaToolDispatcher:
    """Execute only explicitly registered FMEA tools."""

    def __init__(
        self,
        query_service: FmeaQueryService,
        report_service: SessionReportService | None = None,
    ) -> None:
        self._report_service = report_service or SessionReportService()
        self._handlers = {
            "query_fmea_records": query_service.query_records,
            "generate_session_report": self._report_service.generate_session_report,
        }

    def execute(
        self,
        name: str,
        arguments: dict[str, Any],
        *,
        conversation: str = "",
    ) -> dict[str, Any]:
        handler = self._handlers.get(name)
        if handler is None:
            raise ValueError(f"不允許的工具：{name}")
        if name == "generate_session_report":
            return handler(**arguments, conversation=conversation)
        return handler(**arguments)
