"""Deterministic HTML report builder for one Agent conversation session."""

from __future__ import annotations

from datetime import datetime
from html import escape
from typing import Callable, Sequence


class SessionReportService:
    """Render model-prepared report sections and the source transcript to HTML."""

    def __init__(self, now: Callable[[], datetime] = datetime.now) -> None:
        self._now = now

    def generate_session_report(
        self,
        *,
        title: str,
        executive_summary: str,
        objective: str = "",
        processes: Sequence[str] | None = None,
        key_findings: Sequence[str] | None = None,
        action_items: Sequence[str] | None = None,
        open_questions: Sequence[str] | None = None,
        conversation: str = "",
    ) -> dict[str, object]:
        resolved_title = _required_text(title, "title")
        resolved_summary = _required_text(executive_summary, "executive_summary")
        generated_at = self._now()
        sections = {
            "processes": _text_list(processes),
            "key_findings": _text_list(key_findings),
            "action_items": _text_list(action_items),
            "open_questions": _text_list(open_questions),
        }
        filename = (
            "fmea_conversation_report_"
            + generated_at.strftime("%Y%m%d_%H%M%S")
            + ".html"
        )
        html = _render_html(
            title=resolved_title,
            generated_at=generated_at,
            objective=str(objective or "").strip(),
            executive_summary=resolved_summary,
            conversation=str(conversation or "").strip(),
            **sections,
        )
        return {
            "artifact": {
                "filename": filename,
                "mime_type": "text/html",
                "content": html,
            },
            "report_title": resolved_title,
            "generated_at": generated_at.isoformat(timespec="seconds"),
            "section_counts": {
                key: len(values) for key, values in sections.items()
            },
        }


def _render_html(
    *,
    title: str,
    generated_at: datetime,
    objective: str,
    executive_summary: str,
    processes: list[str],
    key_findings: list[str],
    action_items: list[str],
    open_questions: list[str],
    conversation: str,
) -> str:
    report_sections = [
        _paragraph_section("對話目的", objective),
        _list_section("涉及製程", processes),
        _paragraph_section("重點摘要", executive_summary),
        _list_section("關鍵發現", key_findings),
        _list_section("建議後續行動", action_items),
        _list_section("待確認事項", open_questions),
    ]
    transcript = conversation or "本次工作階段沒有可用的對話紀錄。"
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>
    :root {{ color-scheme: light; font-family: Inter, "Noto Sans TC", Arial, sans-serif; }}
    body {{ margin: 0; color: #172033; background: #f3f6fb; line-height: 1.7; }}
    main {{ max-width: 900px; margin: 32px auto; padding: 48px; background: white; border-radius: 18px; box-shadow: 0 14px 40px rgba(20, 35, 70, .09); }}
    header {{ padding-bottom: 24px; border-bottom: 3px solid #2563eb; }}
    h1 {{ margin: 0 0 8px; font-size: 2rem; line-height: 1.3; }}
    h2 {{ margin-top: 32px; color: #1d4ed8; font-size: 1.15rem; }}
    .meta {{ color: #64748b; font-size: .9rem; }}
    .summary {{ padding: 18px 20px; background: #eff6ff; border-left: 4px solid #3b82f6; border-radius: 8px; }}
    li {{ margin: 7px 0; }}
    pre {{ padding: 20px; overflow-wrap: anywhere; white-space: pre-wrap; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; font: .88rem/1.65 Consolas, "Noto Sans TC", monospace; }}
    footer {{ margin-top: 40px; color: #64748b; font-size: .8rem; text-align: center; }}
    @media print {{ body {{ background: white; }} main {{ margin: 0; padding: 24px; box-shadow: none; }} }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>{escape(title)}</h1>
      <div class="meta">產生時間：{escape(generated_at.strftime('%Y-%m-%d %H:%M:%S'))}</div>
    </header>
    {''.join(report_sections)}
    <section>
      <h2>完整對話紀錄</h2>
      <pre>{escape(transcript)}</pre>
    </section>
    <footer>由 FMEA 智慧顧問依本次對話自動整理</footer>
  </main>
</body>
</html>
"""


def _paragraph_section(title: str, content: str) -> str:
    if not content:
        return ""
    css_class = ' class="summary"' if title == "重點摘要" else ""
    return (
        f"<section><h2>{escape(title)}</h2>"
        f"<p{css_class}>{escape(content)}</p></section>"
    )


def _list_section(title: str, items: list[str]) -> str:
    if not items:
        return ""
    rendered = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f"<section><h2>{escape(title)}</h2><ul>{rendered}</ul></section>"


def _required_text(value: object, field: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise ValueError(f"{field} 不可為空")
    return text


def _text_list(values: Sequence[str] | None) -> list[str]:
    if values is None:
        return []
    if isinstance(values, (str, bytes)):
        raise ValueError("報告清單欄位必須是 array")
    return [str(value).strip() for value in values if str(value).strip()]
