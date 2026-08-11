from datetime import datetime

import pytest

from src.conversation_report import SessionReportService
from src.fmea_tools import FMEA_TOOLS, FmeaToolDispatcher


class FakeQueryService:
    def query_records(self, **kwargs):
        return {"records": [], "arguments": kwargs}


def test_report_contains_summary_sections_and_full_escaped_transcript() -> None:
    service = SessionReportService(now=lambda: datetime(2026, 8, 11, 14, 30, 5))

    result = service.generate_session_report(
        title="PVD <風險> 報告",
        objective="整理本次討論",
        processes=["PVD"],
        executive_summary="找到 3 項高風險紀錄。",
        key_findings=["最高 RPN 為 200"],
        action_items=["確認改善措施負責人"],
        open_questions=["改善後 Detection 是否重評"],
        conversation="user: <script>alert(1)</script>\nassistant: 根據 FMEA…",
    )

    artifact = result["artifact"]
    assert artifact["filename"] == "fmea_conversation_report_20260811_143005.html"
    assert artifact["mime_type"] == "text/html"
    html = artifact["content"]
    assert "PVD &lt;風險&gt; 報告" in html
    assert "找到 3 項高風險紀錄" in html
    assert "最高 RPN 為 200" in html
    assert "確認改善措施負責人" in html
    assert "完整對話紀錄" in html
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in html
    assert "<script>alert(1)</script>" not in html


def test_report_requires_title_and_summary() -> None:
    service = SessionReportService()

    with pytest.raises(ValueError, match="title"):
        service.generate_session_report(title="", executive_summary="摘要")
    with pytest.raises(ValueError, match="executive_summary"):
        service.generate_session_report(title="報告", executive_summary="")


def test_dispatcher_exposes_report_tool_and_injects_conversation() -> None:
    report_service = SessionReportService(now=lambda: datetime(2026, 8, 11, 15, 0, 0))
    dispatcher = FmeaToolDispatcher(
        FakeQueryService(),  # type: ignore[arg-type]
        report_service=report_service,
    )
    tool_names = [tool["function"]["name"] for tool in FMEA_TOOLS]

    result = dispatcher.execute(
        "generate_session_report",
        {
            "title": "本次對話報告",
            "objective": "整理對話",
            "processes": [],
            "executive_summary": "測試摘要",
            "key_findings": [],
            "action_items": [],
            "open_questions": [],
        },
        conversation="user: 測試對話",
    )

    assert tool_names == ["query_fmea_records", "generate_session_report"]
    assert "user: 測試對話" in result["artifact"]["content"]
