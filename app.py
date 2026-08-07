"""Streamlit UI for the FMEA Agentic SDK workflow."""

from __future__ import annotations

import uuid

import streamlit as st
from openai import OpenAI

from src.config import ConfigurationError, load_settings
from src.faiss_knowledge_base import (
    KnowledgeBaseNotBuiltError,
    load_existing_knowledge_bases,
)
from src.workflow import build_workflow


st.set_page_config(page_title="FMEA 智慧顧問", page_icon="🔎", layout="wide")


def _initialise() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = uuid.uuid4().hex
    if "knowledge_bases" in st.session_state and "workflow" in st.session_state:
        return

    settings = load_settings(require_chat=True, require_embedding=True)
    embedding_client = OpenAI(
        api_key=settings.embedding_api_key,
        base_url=settings.embedding_base_url,
    )
    st.session_state.knowledge_bases = load_existing_knowledge_bases(
        markdown_dir=settings.markdown_dir,
        index_dir=settings.index_dir,
        embedding_client=embedding_client,
        embedding_model=str(settings.embedding_model),
    )
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
    st.subheader("已載入知識庫")
    for process_code, knowledge_base in st.session_state.knowledge_bases.items():
        st.write(f"- {process_code}：{len(knowledge_base.documents)} rows")
    if st.button("清除對話", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = uuid.uuid4().hex
        del st.session_state.workflow
        st.rerun()


st.title("FMEA 智慧顧問")
st.caption("使用 Agentic SDK 選擇製程知識庫，並將相關 FMEA rows 整理成精簡回答。")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_message = st.chat_input("請輸入 FMEA 問題")
if user_message:
    st.session_state.messages.append({"role": "user", "content": user_message})
    with st.chat_message("user"):
        st.markdown(user_message)

    with st.chat_message("assistant"):
        stage_status = st.status("Agent 執行中", expanded=True)

        def on_event(event: dict) -> None:
            if event.get("type") != "stage":
                return
            label = event.get("label") or event.get("module")
            phase = event.get("phase")
            if phase == "start":
                stage_status.write(f"⏳ {label}")
            elif phase == "finish":
                stage_status.write(f"✅ {label}")
            elif phase == "abort":
                stage_status.write(f"❌ {label}")

        try:
            result = st.session_state.workflow.run(
                user_message,
                session_id=st.session_state.session_id,
                event_callback=on_event,
            )
            final_message = result.final_message or "沒有可顯示的回答。"
            stage_status.update(
                label="處理完成",
                state="complete",
                expanded=False,
            )
            st.markdown(final_message)
        except Exception as exc:
            stage_status.update(
                label="處理失敗",
                state="error",
                expanded=True,
            )
            final_message = f"處理失敗：{exc}"
            st.error(final_message)

    st.session_state.messages.append(
        {"role": "assistant", "content": final_message}
    )
