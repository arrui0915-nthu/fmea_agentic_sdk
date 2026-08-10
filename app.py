"""Streamlit UI for the FMEA Agentic SDK workflow."""

from __future__ import annotations

from datetime import datetime
from html import escape
import uuid

import streamlit as st
from openai import OpenAI

from src.config import ConfigurationError, load_settings
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
from src.ui_stream import WorkflowUiStream
from src.workflow import build_workflow


st.set_page_config(page_title="FMEA 智慧顧問", page_icon="🔎", layout="wide")

st.markdown(
    """
    <style>
        .stAppViewContainer > .main .block-container {
            max-width: 960px;
            padding-top: 2.5rem;
            padding-bottom: 4rem;
        }
        [data-testid="stHeader"] {
            background: transparent;
        }
        section[data-testid="stSidebar"] {
            border-right: 1px solid color-mix(in srgb, var(--text-color) 12%, transparent);
        }
        [data-testid="stChatMessage"] {
            border: 1px solid color-mix(in srgb, var(--text-color) 10%, transparent);
            border-radius: 18px;
            padding: 0.4rem 0.75rem;
            margin-bottom: 0.75rem;
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
    </style>
    """,
    unsafe_allow_html=True,
)


def _initialise() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = uuid.uuid4().hex
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
    if st.button("🗑️ 清除對話", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = uuid.uuid4().hex
        del st.session_state.workflow
        st.rerun()


def _update_stage_status(stage_status, event: dict) -> None:
    if event.get("type") != "stage":
        return
    label = event.get("label") or event.get("module")
    phase = event.get("phase")
    if phase == "start":
        stage_status.update(label=f"{label}…", state="running", expanded=False)
    elif phase == "finish":
        stage_status.update(label=f"{label}完成", state="complete", expanded=False)
    elif phase == "abort":
        stage_status.update(label=f"{label}失敗", state="error", expanded=False)


def _render_chat_page() -> None:
    st.title("FMEA 智慧顧問")
    st.caption("從可用的製程知識庫中搜尋相關 FMEA 資訊，整理成清楚、精簡的回答。")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_message = st.chat_input("請輸入 FMEA 問題")
    if not user_message:
        return

    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        stage_status = st.status("正在準備…", expanded=False)

        def answer_deltas(ui_stream: WorkflowUiStream):
            for event in ui_stream:
                if event.kind == "stage":
                    _update_stage_status(stage_status, event.payload)
                else:
                    yield event.payload

        try:
            ui_stream = WorkflowUiStream(
                st.session_state.workflow,
                user_message,
                st.session_state.session_id,
            )
            streamed_message = st.write_stream(answer_deltas(ui_stream))
            result = ui_stream.result
            final_message = result.final_message or "沒有可顯示的回答。"
            stage_status.update(label="處理完成", state="complete", expanded=False)
            if not streamed_message:
                st.markdown(final_message)
        except Exception as exc:
            stage_status.update(label="處理失敗", state="error", expanded=True)
            final_message = f"處理失敗：{exc}"
            st.error(final_message)

    st.session_state.messages.append(
        {"role": "assistant", "content": final_message}
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


chat_tab, preview_tab = st.tabs(("FMEA 智慧顧問", "從聊天建立 FMEA"))
with chat_tab:
    _render_chat_page()
with preview_tab:
    _render_preview_page()
