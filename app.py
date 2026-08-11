"""Streamlit UI for the FMEA Agentic SDK workflow."""

from __future__ import annotations

from datetime import datetime
from html import escape
import json
import uuid

import streamlit as st
from openai import OpenAI

from src.config import ConfigurationError, load_settings
from src.demo_questions import SAMPLE_QUESTIONS
from src.faiss_knowledge_base import (
    KnowledgeBaseNotBuiltError,
    load_existing_knowledge_bases,
)
from src.fmea_preview import (
    build_preview_workflow,
    decode_chat_log,
    display_fmea_rows,
    duplicate_rows_for_display,
)
from src.machine_action import (
    PvdMachineSimulator,
    SETPOINT_IDS,
    SETPOINT_MAX,
    SETPOINT_MIN,
)
from src.ui_stream import WorkflowUiStream
from src.workflow import build_workflow


st.set_page_config(page_title="FMEA 智慧顧問", page_icon="🔎", layout="centered")

st.markdown(
    """
    <style>
        [data-testid="stAppViewContainer"] .main .block-container,
        [data-testid="stMainBlockContainer"] {
            width: 100%;
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 5rem;
        }
        [data-testid="stHeader"] {
            background: transparent;
        }
        section[data-testid="stSidebar"] {
            border-right: 1px solid color-mix(in srgb, var(--text-color) 12%, transparent);
        }
        [data-testid="stChatMessage"] {
            align-items: flex-start;
            gap: 0.75rem;
            padding: 0.9rem 0;
            margin-bottom: 0.25rem;
            background: transparent;
        }
        [data-testid="stChatMessage"] > div:last-child,
        [data-testid="stChatMessageContent"] {
            min-width: 0;
            overflow-wrap: anywhere;
        }
        [data-testid="stChatMessageContent"] h1 {
            margin: 1.25rem 0 0.55rem;
            font-size: 1.6rem;
            line-height: 1.3;
        }
        [data-testid="stChatMessageContent"] h2 {
            margin: 1.15rem 0 0.5rem;
            font-size: 1.4rem;
            line-height: 1.35;
        }
        [data-testid="stChatMessageContent"] h3 {
            margin: 1rem 0 0.45rem;
            font-size: 1.2rem;
            line-height: 1.4;
        }
        [data-testid="stChatMessage"] table {
            display: block;
            max-width: 100%;
            overflow-x: auto;
            white-space: nowrap;
        }
        [data-testid="stBottomBlockContainer"],
        [data-testid="stChatInput"] {
            width: 100%;
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        .kb-list {
            display: flex;
            flex-direction: column;
            gap: 0.55rem;
            margin: 1rem 0 1.5rem;
        }
        .kb-item {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            padding: 0.65rem 0.75rem;
            border: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent);
            border-radius: 12px;
            background: color-mix(in srgb, var(--secondary-background-color) 88%, transparent);
            font-weight: 600;
        }
        .kb-dot {
            width: 0.55rem;
            height: 0.55rem;
            flex: 0 0 0.55rem;
            border-radius: 999px;
            background: #22c55e;
            box-shadow: 0 0 0 3px color-mix(in srgb, #22c55e 18%, transparent);
        }
        .kb-ready {
            margin-left: auto;
            color: #16a34a;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }
        .trace-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 0.45rem;
            margin: 0.35rem 0 0.9rem;
        }
        .trace-card {
            min-width: 0;
            padding: 0.65rem 0.45rem;
            border: 1px solid color-mix(in srgb, var(--text-color) 12%, transparent);
            border-radius: 10px;
            background: color-mix(in srgb, var(--secondary-background-color) 75%, transparent);
            text-align: center;
        }
        .trace-card.complete { border-color: color-mix(in srgb, #22c55e 45%, transparent); }
        .trace-card.running { border-color: #3b82f6; box-shadow: 0 0 0 2px color-mix(in srgb, #3b82f6 14%, transparent); }
        .trace-card.error { border-color: #ef4444; }
        .trace-card.skipped, .trace-card.pending { opacity: 0.48; }
        .trace-icon { display: block; font-size: 1rem; line-height: 1; margin-bottom: 0.35rem; }
        .trace-label { display: block; font-size: 0.76rem; font-weight: 700; line-height: 1.25; }
        .trace-time { display: block; margin-top: 0.25rem; color: color-mix(in srgb, var(--text-color) 58%, transparent); font-size: 0.66rem; }
        .trace-detail {
            padding: 0.5rem 0.65rem;
            margin: 0.4rem 0;
            border-left: 3px solid color-mix(in srgb, #3b82f6 65%, transparent);
            background: color-mix(in srgb, var(--secondary-background-color) 62%, transparent);
            border-radius: 0 8px 8px 0;
        }
        .trace-detail-title { font-weight: 700; font-size: 0.82rem; }
        .trace-detail-text { margin-top: 0.2rem; font-size: 0.76rem; line-height: 1.45; }
        @media (max-width: 640px) {
            [data-testid="stAppViewContainer"] .main .block-container,
            [data-testid="stMainBlockContainer"] {
                padding-top: 1rem;
                padding-left: 0.75rem;
                padding-right: 0.75rem;
            }
            [data-testid="stChatMessage"] {
                gap: 0.5rem;
                padding: 0.7rem 0;
            }
            .trace-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def _clear_conversation_state() -> None:
    st.session_state.messages = []
    st.session_state.session_id = uuid.uuid4().hex
    st.session_state.pop("workflow", None)
    st.session_state.pop("preview_chat_text", None)
    st.session_state.pop("preview_chat_file", None)
    st.session_state.pop("preview_result", None)


def _initialise() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = uuid.uuid4().hex
    if "machine_simulator" not in st.session_state:
        st.session_state.machine_simulator = PvdMachineSimulator()
    settings = load_settings(require_chat=True, require_embedding=True)
    st.session_state.settings = settings
    if "embedding_client" not in st.session_state:
        st.session_state.embedding_client = OpenAI(
            api_key=settings.embedding_api_key,
            base_url=settings.embedding_base_url,
        )
    if "knowledge_bases" not in st.session_state:
        st.session_state.knowledge_bases = load_existing_knowledge_bases(
            markdown_dir=settings.markdown_dir,
            index_dir=settings.index_dir,
            embedding_client=st.session_state.embedding_client,
            embedding_model=str(settings.embedding_model),
        )
    if "workflow" not in st.session_state:
        st.session_state.workflow = build_workflow(
            st.session_state.knowledge_bases,
            settings=settings,
            machine_simulator=st.session_state.machine_simulator,
        )


try:
    _initialise()
except ConfigurationError as exc:
    st.error(str(exc))
    st.stop()
except KnowledgeBaseNotBuiltError:
    st.error("尚未建立知識庫，請先執行：\n\n`python build_indexes.py`")
    st.stop()
except Exception as exc:
    st.error(f"載入知識庫失敗：{exc}")
    st.stop()


with st.sidebar:
    active_page = st.radio(
        "功能",
        ("💬 FMEA 智慧顧問", "📄 從聊天建立 FMEA", "⚙️ PVD 模擬機台"),
        key="active_page",
    )
    st.divider()
    st.subheader("Knowledge bases")
    st.caption("目前可供 Agent 檢索的製程知識庫")
    knowledge_base_items = "".join(
        (
            '<div class="kb-item">'
            '<span class="kb-dot"></span>'
            f"<span>{escape(process_code)}</span>"
            '<span class="kb-ready">Available</span>'
            "</div>"
        )
        for process_code in sorted(st.session_state.knowledge_bases)
    )
    st.markdown(
        f'<div class="kb-list">{knowledge_base_items}</div>',
        unsafe_allow_html=True,
    )
    st.button(
        "🗑️ 清除對話",
        use_container_width=True,
        on_click=_clear_conversation_state,
    )


def _update_stage_status(stage_status, event: dict) -> None:
    if event.get("type") != "stage":
        return
    label = event.get("label") or event.get("module")
    phase = event.get("phase")
    if phase == "start":
        stage_status.update(label=f"{label}…", state="running", expanded=False)
    elif phase == "finish":
        outcome = event.get("status")
        suffix = "略過" if outcome == "skipped" else "完成"
        stage_status.update(label=f"{label}{suffix}", state="complete", expanded=False)
    elif phase == "abort":
        stage_status.update(label=f"{label}失敗", state="error", expanded=False)


_TRACE_STATUS = {
    "pending": ("○", "等待"),
    "running": ("●", "執行中"),
    "complete": ("✓", "完成"),
    "skipped": ("–", "略過"),
    "error": ("!", "失敗"),
}

_TRACE_FIELD_LABELS = {
    "intent": "問題類型",
    "summary": "問題摘要",
    "details.query_type": "查詢類型",
    "details.processes": "製程",
    "details.cross_table": "跨製程",
    "details.complexity": "複雜度",
    "thought": "路由決策",
    "next_module": "選擇模組",
    "verdict": "檢查結果",
    "reason": "檢查說明",
    "suggestion": "修正建議",
    "correction_count": "已修正次數",
    "max_corrections": "修正上限",
    "will_retry": "自動重試",
    "correction_exhausted": "已達重試上限",
}

_TRACE_SUMMARY_LABELS = {
    "processes": "檢索製程",
    "top_k": "每製程 Top K",
    "hit_count": "命中筆數",
    "cross_table": "跨製程",
    "candidate_count": "候選筆數",
    "accepted_count": "採用筆數",
    "duplicate_count": "重複筆數",
    "threshold": "相似度門檻",
    "ok": "執行結果",
    "model": "模型",
    "tool_names": "呼叫工具",
    "needs_process_clarification": "需要確認製程",
    "verdict": "檢查結果",
    "reason": "檢查說明",
    "strategy": "檢查策略",
    "suggestion": "修正建議",
}


def _format_trace_duration(milliseconds: object) -> str:
    if not isinstance(milliseconds, (int, float)):
        return "—"
    if milliseconds < 1000:
        return f"{int(milliseconds)} ms"
    return f"{milliseconds / 1000:.2f} s"


def _format_trace_value(value: object) -> str:
    if isinstance(value, bool):
        return "是" if value else "否"
    if value is None:
        return "—"
    if isinstance(value, list):
        return "、".join(_format_trace_value(item) for item in value) or "—"
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, separators=(", ", ": "))
    return str(value)


def _trace_details(stage: dict) -> list[tuple[str, str]]:
    details: list[tuple[str, str]] = []
    visit_count = int(stage.get("visit_count") or 0)
    if visit_count > 1:
        details.append(("執行次數", str(visit_count)))

    attempts = stage.get("attempts")
    if isinstance(attempts, list) and len(attempts) > 1:
        for attempt in attempts:
            if not isinstance(attempt, dict):
                continue
            number = int(attempt.get("visit_count") or 0)
            summary = attempt.get("summary")
            if not isinstance(summary, dict):
                summary = {}
            verdict = summary.get("verdict") or attempt.get("status") or "—"
            reason = summary.get("reason") or attempt.get("reason")
            retry = "；觸發自動修正" if summary.get("will_retry") else ""
            text = str(verdict)
            if reason:
                text += f"；{reason}"
            details.append((f"第 {number} 次", text + retry))

    fields = stage.get("fields")
    if isinstance(fields, list):
        field_names = {
            str(item.get("field"))
            for item in fields
            if isinstance(item, dict)
        }
        for item in fields:
            if not isinstance(item, dict):
                continue
            field = str(item.get("field") or "")
            if field == "details" and any(name.startswith("details.") for name in field_names):
                continue
            if field == "suggestion" and not str(item.get("value") or "").strip():
                continue
            label = _TRACE_FIELD_LABELS.get(field, field)
            details.append((label, _format_trace_value(item.get("value"))))

    summary = stage.get("summary")
    if isinstance(summary, dict):
        for key, value in summary.items():
            details.append(
                (_TRACE_SUMMARY_LABELS.get(str(key), str(key)), _format_trace_value(value))
            )

    next_module = stage.get("next_module")
    if next_module:
        details.append(("下一階段", str(next_module)))
    if stage.get("reason"):
        details.append(("失敗原因", str(stage["reason"])))
    return details


def _render_agent_trace(trace: object) -> None:
    if not isinstance(trace, dict):
        return
    stages = trace.get("stages")
    if not isinstance(stages, list):
        return

    executions = sum(
        int(stage.get("visit_count") or 0)
        for stage in stages
        if isinstance(stage, dict) and stage.get("status") in {"running", "complete", "error"}
    )
    total_tokens = int(trace.get("input_tokens") or 0) + int(trace.get("output_tokens") or 0)
    duration = _format_trace_duration(trace.get("duration_ms"))
    status_icon = "⚠️" if trace.get("status") == "error" else "🧭"
    metrics = f"{executions} 次模組執行"
    if trace.get("duration_ms") is not None:
        metrics += f" · {duration}"
    if total_tokens:
        metrics += f" · {total_tokens:,} tokens"

    with st.expander(
        f"{status_icon} Agent 執行軌跡 · {metrics}",
        expanded=trace.get("status") == "running",
    ):
        cards: list[str] = []
        for raw_stage in stages:
            if not isinstance(raw_stage, dict):
                continue
            status = str(raw_stage.get("status") or "pending")
            icon, status_label = _TRACE_STATUS.get(status, ("○", status))
            visit_count = int(raw_stage.get("visit_count") or 0)
            if visit_count > 1:
                status_label += f" ×{visit_count}"
            stage_duration = _format_trace_duration(raw_stage.get("duration_ms"))
            cards.append(
                f'<div class="trace-card {escape(status)}">'
                f'<span class="trace-icon">{escape(icon)}</span>'
                f'<span class="trace-label">{escape(str(raw_stage.get("label") or raw_stage.get("module") or ""))}</span>'
                f'<span class="trace-time">{escape(status_label)} · {escape(stage_duration)}</span>'
                "</div>"
            )
        st.markdown(
            '<div class="trace-grid">' + "".join(cards) + "</div>",
            unsafe_allow_html=True,
        )

        for raw_stage in stages:
            if not isinstance(raw_stage, dict) or raw_stage.get("status") in {"pending", "skipped"}:
                continue
            details = _trace_details(raw_stage)
            if not details:
                continue
            detail_text = " · ".join(
                f"<strong>{escape(label)}</strong>: {escape(value)}"
                for label, value in details
            )
            st.markdown(
                '<div class="trace-detail">'
                f'<div class="trace-detail-title">{escape(str(raw_stage.get("label") or raw_stage.get("module")))}</div>'
                f'<div class="trace-detail-text">{detail_text}</div>'
                "</div>",
                unsafe_allow_html=True,
            )


def _render_agent_trace_in(placeholder, trace: object) -> None:
    with placeholder.container():
        _render_agent_trace(trace)


def _report_artifacts(entities: object) -> list[dict[str, str]]:
    if not isinstance(entities, dict):
        return []
    tool_results = entities.get("latest_tool_results")
    if not isinstance(tool_results, list):
        return []
    artifacts: list[dict[str, str]] = []
    for tool_result in tool_results:
        if not isinstance(tool_result, dict) or tool_result.get("name") != "generate_session_report":
            continue
        result = tool_result.get("result")
        if not isinstance(result, dict) or result.get("ok") is not True:
            continue
        data = result.get("data")
        artifact = data.get("artifact") if isinstance(data, dict) else None
        if not isinstance(artifact, dict):
            continue
        filename = str(artifact.get("filename") or "conversation_report.html")
        content = artifact.get("content")
        if not isinstance(content, str) or not content:
            continue
        artifacts.append(
            {
                "filename": filename,
                "mime_type": str(artifact.get("mime_type") or "text/html"),
                "content": content,
            }
        )
    return artifacts


def _render_report_artifacts(
    artifacts: object,
    *,
    key_prefix: str,
) -> None:
    if not isinstance(artifacts, list):
        return
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict) or not artifact.get("content"):
            continue
        st.download_button(
            "⬇️ 下載本次對話摘要報告",
            data=artifact["content"],
            file_name=str(artifact.get("filename") or "conversation_report.html"),
            mime=str(artifact.get("mime_type") or "text/html"),
            type="primary",
            key=f"{key_prefix}-report-{index}",
        )


def _render_chat_page() -> None:
    st.title("FMEA 智慧顧問")
    st.caption("從可用的製程知識庫中搜尋相關 FMEA 資訊，整理成清楚、精簡的回答。")

    sample_message = None
    with st.expander("範例問題", expanded=not st.session_state.messages):
        question_columns = st.columns(2)
        for index, question in enumerate(SAMPLE_QUESTIONS):
            if question_columns[index % 2].button(
                question,
                key=f"sample-question-{index}",
                use_container_width=True,
            ):
                sample_message = question

    for message_index, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                _render_report_artifacts(
                    message.get("artifacts"),
                    key_prefix=f"history-{message_index}",
                )
                _render_agent_trace(message.get("trace"))

    typed_message = st.chat_input("請輸入 FMEA 問題")
    user_message = sample_message or typed_message
    if not user_message:
        return

    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        answer_placeholder = st.empty()
        trace_placeholder = st.empty()
        ui_stream = None
        final_trace = None
        final_artifacts: list[dict[str, str]] = []

        try:
            ui_stream = WorkflowUiStream(
                st.session_state.workflow,
                user_message,
                st.session_state.session_id,
            )
            _render_agent_trace_in(trace_placeholder, ui_stream.trace)
            streamed_chunks: list[str] = []
            for event in ui_stream:
                if event.kind == "stage":
                    if (
                        isinstance(event.payload, dict)
                        and event.payload.get("module") == "action"
                        and event.payload.get("phase") == "start"
                        and int(event.payload.get("visit_count") or 0) > 1
                    ):
                        streamed_chunks.clear()
                        answer_placeholder.info("Reflect 發現問題，正在自動修正回答…")
                    _render_agent_trace_in(trace_placeholder, ui_stream.trace)
                    continue
                streamed_chunks.append(str(event.payload))
                answer_placeholder.markdown("".join(streamed_chunks) + " ▌")

            result = ui_stream.result
            final_message = result.final_message or "沒有可顯示的回答。"
            final_trace = ui_stream.trace
            final_artifacts = _report_artifacts(result.entities)
            answer_placeholder.markdown(final_message)
            _render_agent_trace_in(trace_placeholder, final_trace)
            _render_report_artifacts(
                final_artifacts,
                key_prefix=f"current-{len(st.session_state.messages)}",
            )
        except Exception as exc:
            final_message = f"處理失敗：{exc}"
            final_trace = ui_stream.trace if ui_stream is not None else None
            answer_placeholder.error(final_message)
            _render_agent_trace_in(trace_placeholder, final_trace)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_message,
            "trace": final_trace,
            "artifacts": final_artifacts,
        }
    )


def _preview_input() -> tuple[str | None, str | None]:
    source = st.radio(
        "聊天紀錄來源",
        ("直接貼上", "上傳 TXT / MD"),
        horizontal=True,
        key="preview_input_source",
    )
    if source == "直接貼上":
        return st.text_area(
            "聊天紀錄",
            height=260,
            placeholder="貼上會議、客服或工程討論紀錄…",
            key="preview_chat_text",
        ), None

    uploaded = st.file_uploader(
        "上傳 UTF-8 聊天紀錄",
        type=("txt", "md"),
        key="preview_chat_file",
    )
    if uploaded is None:
        return None, None
    try:
        return decode_chat_log(uploaded.getvalue()), None
    except ValueError as exc:
        return None, str(exc)


def _render_preview_result() -> None:
    preview_result = st.session_state.get("preview_result")
    if not isinstance(preview_result, dict):
        return

    candidate_rows = preview_result.get("candidate_rows") or []
    preview_rows = preview_result.get("preview_rows") or []
    duplicate_rows = preview_result.get("duplicate_rows") or []
    reflect_verdict = preview_result.get("reflect_verdict")

    if reflect_verdict == "fail":
        st.error("Preview 驗證失敗，未提供下載檔案。")
        return
    if not candidate_rows:
        st.warning("聊天紀錄中沒有足夠資訊可整理成 FMEA row。")
        return

    if preview_rows:
        st.subheader(f"可加入的新 FMEA rows（{len(preview_rows)}）")
        st.dataframe(
            display_fmea_rows(preview_rows),
            use_container_width=True,
            hide_index=True,
        )
        workbook_bytes = preview_result.get("preview_xlsx_bytes")
        if isinstance(workbook_bytes, bytes) and workbook_bytes:
            st.download_button(
                "下載 FMEA Preview (.xlsx)",
                data=workbook_bytes,
                file_name=preview_result["download_filename"],
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
            )
    else:
        st.info("所有候選 rows 都與既有 FMEA 過度相似，沒有建立下載檔案。")

    if duplicate_rows:
        with st.expander(f"已排除的相似 rows（{len(duplicate_rows)}）", expanded=False):
            st.dataframe(
                duplicate_rows_for_display(duplicate_rows),
                use_container_width=True,
                hide_index=True,
            )


def _render_preview_page() -> None:
    st.title("從聊天建立 FMEA")
    st.caption("將聊天紀錄整理成 FMEA Preview；只讀取既有索引，不會更新知識庫。")

    conversation, input_error = _preview_input()
    process_codes = sorted(st.session_state.knowledge_bases)
    selected_processes = st.multiselect(
        "相似度比對製程",
        process_codes,
        default=process_codes,
        key="preview_processes",
    )
    threshold = st.slider(
        "重複判定門檻（cosine similarity）",
        min_value=0.70,
        max_value=0.99,
        value=0.85,
        step=0.01,
        key="preview_similarity_threshold",
    )
    st.caption("分數大於或等於門檻的候選 row 不會加入下載檔案。")

    if input_error:
        st.error(input_error)

    if st.button("產生 FMEA Preview", type="primary", disabled=bool(input_error)):
        st.session_state.pop("preview_result", None)
        if not conversation or not conversation.strip():
            st.error("請貼上或上傳聊天紀錄。")
        elif not selected_processes:
            st.error("請至少選擇一個相似度比對製程。")
        else:
            stage_status = st.status("正在準備…", expanded=False)
            try:
                workflow = build_preview_workflow(
                    st.session_state.knowledge_bases,
                    selected_processes=selected_processes,
                    threshold=threshold,
                    settings=st.session_state.settings,
                    embedding_client=st.session_state.embedding_client,
                )
                preview_session_id = uuid.uuid4().hex
                result = workflow.run(
                    conversation,
                    session_id=preview_session_id,
                    event_callback=lambda event: _update_stage_status(
                        stage_status, event
                    ),
                )
                if result.aborted:
                    raise RuntimeError(result.abort_reason or "Preview workflow 已中止")
                st.session_state.preview_result = {
                    **result.entities,
                    "download_filename": (
                        "fmea_preview_"
                        + datetime.now().strftime("%Y%m%d_%H%M%S")
                        + ".xlsx"
                    ),
                }
                stage_status.update(
                    label="Preview 產生完成", state="complete", expanded=False
                )
            except Exception as exc:
                stage_status.update(
                    label="Preview 產生失敗", state="error", expanded=True
                )
                st.error(f"Preview 產生失敗：{exc}")

    _render_preview_result()


def _normalise_machine_setpoints(snapshot: dict) -> dict[str, int]:
    raw_setpoints = snapshot.get("setpoints")
    if not isinstance(raw_setpoints, dict):
        raw_setpoints = {}

    setpoints: dict[str, int] = {}
    for setpoint_id in SETPOINT_IDS:
        try:
            value = int(raw_setpoints.get(setpoint_id, SETPOINT_MIN))
        except (TypeError, ValueError):
            value = SETPOINT_MIN
        setpoints[setpoint_id] = max(
            SETPOINT_MIN,
            min(SETPOINT_MAX, value),
        )
    return setpoints


def _sync_machine_widgets(snapshot: dict) -> None:
    setpoints = _normalise_machine_setpoints(snapshot)
    revision = snapshot.get("revision")
    history = snapshot.get("history")
    marker = (
        ("revision", revision)
        if revision is not None
        else (
            "state",
            len(history) if isinstance(history, (list, tuple)) else None,
            tuple(setpoints.items()),
        )
    )
    force_sync = bool(st.session_state.pop("machine_widget_sync_pending", False))
    if not force_sync and st.session_state.get("machine_widget_state_marker") == marker:
        return

    for setpoint_id, value in setpoints.items():
        st.session_state[f"machine_widget_{setpoint_id}"] = value
    st.session_state.machine_widget_state_marker = marker


def _machine_history_rows(history: object) -> list[dict[str, object]]:
    if not isinstance(history, (list, tuple)):
        return []

    rows: list[dict[str, object]] = []
    for raw_record in reversed(history[-10:]):
        if not isinstance(raw_record, dict):
            rows.append({"紀錄": str(raw_record)})
            continue
        record: dict[str, object] = {}
        for key, value in raw_record.items():
            if isinstance(value, (dict, list, tuple)):
                record[str(key)] = json.dumps(
                    value,
                    ensure_ascii=False,
                    separators=(", ", ": "),
                )
            else:
                record[str(key)] = value
        rows.append(record)
    return rows


def _render_machine_page() -> None:
    st.title("⚙️ PVD 模擬機台")
    st.caption("模擬三個數值 setpoint；Agent 與本頁操作會更新同一台機台。")

    simulator = st.session_state.machine_simulator
    snapshot = simulator.snapshot()
    if not isinstance(snapshot, dict):
        st.error("無法讀取模擬機台狀態。")
        return

    _sync_machine_widgets(snapshot)
    setpoints = _normalise_machine_setpoints(snapshot)
    machine_id = snapshot.get("machine_id")
    revision = snapshot.get("revision")
    status_text = f"機台：{machine_id}" if machine_id else "PVD demo machine"
    if revision is not None:
        status_text += f" · Revision {revision}"
    st.caption(status_text)

    st.subheader("目前機台值")
    current_columns = st.columns(len(SETPOINT_IDS))
    for column, setpoint_id in zip(current_columns, SETPOINT_IDS):
        column.metric(setpoint_id, setpoints[setpoint_id])

    notice = st.session_state.pop("machine_action_notice", None)
    if notice:
        st.success(str(notice))

    st.subheader("手動調整")
    input_columns = st.columns(len(SETPOINT_IDS))
    for column, setpoint_id in zip(input_columns, SETPOINT_IDS):
        column.number_input(
            setpoint_id,
            min_value=SETPOINT_MIN,
            max_value=SETPOINT_MAX,
            step=1,
            key=f"machine_widget_{setpoint_id}",
        )

    apply_column, reset_column = st.columns(2)
    if apply_column.button("手動套用", type="primary", use_container_width=True):
        requested_setpoints = {
            setpoint_id: int(st.session_state[f"machine_widget_{setpoint_id}"])
            for setpoint_id in SETPOINT_IDS
        }
        try:
            simulator.apply_manual(requested_setpoints)
            st.session_state.machine_widget_sync_pending = True
            st.session_state.machine_action_notice = "已套用三個 setpoint。"
            st.rerun()
        except Exception as exc:
            st.error(f"套用失敗：{exc}")

    if reset_column.button("重設機台", use_container_width=True):
        try:
            simulator.reset()
            st.session_state.machine_widget_sync_pending = True
            st.session_state.machine_action_notice = "機台已重設。"
            st.rerun()
        except Exception as exc:
            st.error(f"重設失敗：{exc}")

    st.subheader("最近執行紀錄")
    history_rows = _machine_history_rows(snapshot.get("history"))
    if history_rows:
        st.dataframe(history_rows, use_container_width=True, hide_index=True)
    else:
        st.info("尚無執行紀錄。")


if active_page == "💬 FMEA 智慧顧問":
    _render_chat_page()
elif active_page == "📄 從聊天建立 FMEA":
    _render_preview_page()
else:
    _render_machine_page()
