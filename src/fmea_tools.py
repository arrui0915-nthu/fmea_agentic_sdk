"""OpenAI tool definitions and the allow-listed FMEA tool dispatcher."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.conversation_report import SessionReportService
from src.fmea_query import FmeaQueryService

if TYPE_CHECKING:
    from src.machine_action import MachineActionService


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

SUMMARIZE_RPN_BY_PROCESS_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "summarize_rpn_by_process",
        "description": (
            "精確計算各製程的平均 RPN，並依平均 RPN 由高到低回傳。"
            "使用全部符合製程的 FMEA 紀錄計算，不受單筆查詢 20 筆上限影響。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "processes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "製程代碼；省略代表計算全部製程。",
                }
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

APPLY_MACHINE_ACTION_TOOL: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "apply_machine_action",
        "description": (
            "套用本輪已檢索到的 PVD FMEA 記錄所定義的機台 setpoints。"
            "只在使用者明確要求調整機台時呼叫；不得自行提供或改寫 setpoint。"
            "同一 workflow 對同一 document_id 的重試具冪等性。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "string",
                    "description": "本輪檢索結果中的 PVD document ID，例如 PVD-0001。",
                }
            },
            "required": ["document_id"],
            "additionalProperties": False,
        },
    },
}

FMEA_TOOLS = [
    QUERY_FMEA_RECORDS_TOOL,
    SUMMARIZE_RPN_BY_PROCESS_TOOL,
    GENERATE_SESSION_REPORT_TOOL,
    APPLY_MACHINE_ACTION_TOOL,
]


class FmeaToolDispatcher:
    """Execute only explicitly registered FMEA tools."""

    def __init__(
        self,
        query_service: FmeaQueryService,
        report_service: SessionReportService | None = None,
        machine_action_service: MachineActionService | None = None,
    ) -> None:
        self._report_service = report_service or SessionReportService()
        self._machine_action_service = machine_action_service
        self._handlers = {
            "query_fmea_records": query_service.query_records,
            "summarize_rpn_by_process": query_service.summarize_rpn_by_process,
            "generate_session_report": self._report_service.generate_session_report,
        }

    def execute(
        self,
        name: str,
        arguments: dict[str, Any],
        *,
        conversation: str = "",
        workflow_id: str = "",
        retrieved_document_ids: list[str] | None = None,
        perceived_intent: str = "",
    ) -> dict[str, Any]:
        if name == "apply_machine_action":
            return self._apply_machine_action(
                arguments,
                workflow_id=workflow_id,
                retrieved_document_ids=retrieved_document_ids,
                perceived_intent=perceived_intent,
            )

        handler = self._handlers.get(name)
        if handler is None:
            raise ValueError(f"不允許的工具：{name}")
        if name == "generate_session_report":
            return handler(**arguments, conversation=conversation)
        return handler(**arguments)

    def _apply_machine_action(
        self,
        arguments: dict[str, Any],
        *,
        workflow_id: str,
        retrieved_document_ids: list[str] | None,
        perceived_intent: str,
    ) -> dict[str, Any]:
        if self._machine_action_service is None:
            raise RuntimeError("machine action service is not configured")
        if perceived_intent != "machine_control":
            raise PermissionError(
                "apply_machine_action requires the machine_control intent"
            )
        if set(arguments) != {"document_id"}:
            raise ValueError("apply_machine_action requires only document_id")

        document_id = arguments.get("document_id")
        if not isinstance(document_id, str) or not document_id.strip():
            raise ValueError("document_id must be a non-empty string")
        normalized_document_id = document_id.strip().upper()
        normalized_workflow_id = str(workflow_id).strip()
        if not normalized_workflow_id:
            raise ValueError("workflow_id is required for machine actions")

        allowed_document_ids = [
            str(candidate).strip().upper()
            for candidate in (retrieved_document_ids or [])
            if str(candidate).strip()
        ]
        return self._machine_action_service.execute(
            normalized_document_id,
            allowed_document_ids=allowed_document_ids,
            idempotency_key=(
                f"{normalized_workflow_id}:apply_machine_action:"
                f"{normalized_document_id}"
            ),
        )
