"""Action module that executes allow-listed FMEA tool calls."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from agentic_sdk import ContextEntry, ContextEntryType, ModuleOutput, WorkflowState
from agentic_sdk.llm import OpenAIChatResponse, chat_stream, require_model, resolve_openai_client
from agentic_sdk.memory.in_context import build_module_messages

from src.fmea_tools import FmeaToolDispatcher


ChatRunner = Callable[..., OpenAIChatResponse]


class FmeaToolAction:
    """Ask the model for tool calls, execute them, then ask for a final answer."""

    name = "action"
    gen_ai_system = "openai_compatible"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        system_prompt: str,
        tools: list[dict[str, Any]],
        dispatcher: FmeaToolDispatcher,
        available_processes: list[str] | None = None,
        client: Any | None = None,
        chat_runner: ChatRunner = chat_stream,
    ) -> None:
        self._temperature = temperature
        self._system_prompt = system_prompt
        self._model = require_model(model, self.__class__.__name__)
        self._client = client or resolve_openai_client(
            self.__class__.__name__,
            api_key=api_key,
            base_url=base_url,
        )
        self._tools = list(tools)
        self._dispatcher = dispatcher
        self._available_processes = sorted(
            str(process).strip().upper()
            for process in (available_processes or [])
            if str(process).strip()
        )
        self._chat_runner = chat_runner

    @property
    def gen_ai_request_model(self) -> str:
        return self._model

    def __call__(self, state: WorkflowState) -> ModuleOutput:
        if _needs_process_clarification(state):
            content = _process_clarification_message(
                state.lookup("available_processes") or self._available_processes
            )
            state.emit_token_delta(
                self.name,
                content,
                metadata={"model": self._model, "structured": False},
            )
            state.last_action_error = None
            state.last_action_result = {
                "content": content,
                "model": self._model,
                "tool_calls": [],
                "tool_results": [],
            }
            return ModuleOutput(
                next_module=None,
                payload={
                    "latest_final_message": content,
                    "latest_tool_calls": [],
                    "latest_tool_results": [],
                    "_llm_usage": _combined_usage([], self._model),
                },
                context_updates=[
                    ContextEntry(
                        type=ContextEntryType.ACTION_RESULT,
                        content=content,
                        metadata={
                            "ok": True,
                            "model": self._model,
                            "tool_names": [],
                            "needs_process_clarification": True,
                        },
                    )
                ],
            )

        messages = _build_messages(state, self._system_prompt)
        responses: list[OpenAIChatResponse] = []
        try:
            first_response = self._chat_runner(
                self._client,
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                tools=self._tools,
                tool_choice="auto",
            )
            responses.append(first_response)
            tool_calls = _normalize_tool_calls(first_response.tool_calls)

            if not tool_calls:
                content = first_response.content
                state.emit_token_delta(
                    self.name,
                    content,
                    metadata={"model": self._model, "structured": False},
                )
                tool_results: list[dict[str, Any]] = []
            else:
                tool_results = self._execute_tool_calls(tool_calls, state=state)
                messages.append(
                    {
                        "role": "assistant",
                        "content": first_response.content or "",
                        "tool_calls": tool_calls,
                    }
                )
                for result in tool_results:
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": result["tool_call_id"],
                            "content": json.dumps(
                                _tool_result_for_model(result["result"]),
                                ensure_ascii=False,
                                default=str,
                            ),
                        }
                    )
                final_response = self._chat_runner(
                    self._client,
                    model=self._model,
                    messages=messages,
                    temperature=self._temperature,
                    on_delta=lambda delta: state.emit_token_delta(
                        self.name,
                        delta,
                        metadata={"model": self._model, "structured": False},
                    ),
                )
                responses.append(final_response)
                content = final_response.content
        except Exception as exc:
            detail = str(exc)
            state.last_action_error = {
                "type": type(exc).__name__,
                "message": detail,
            }
            return ModuleOutput(
                next_module=None,
                payload={"_llm_usage": _combined_usage(responses, self._model)},
                context_updates=[
                    ContextEntry(
                        type=ContextEntryType.ACTION_RESULT,
                        content=f"error:{type(exc).__name__}",
                        metadata={"ok": False, "error": detail},
                    )
                ],
            )

        response_model = responses[-1].model or self._model
        state.last_action_error = None
        state.last_action_result = {
            "content": content,
            "model": response_model,
            "tool_calls": tool_calls,
            "tool_results": tool_results,
        }
        return ModuleOutput(
            next_module=None,
            payload={
                "latest_final_message": content,
                "latest_tool_calls": tool_calls,
                "latest_tool_results": tool_results,
                "_llm_usage": _combined_usage(responses, response_model),
            },
            context_updates=[
                ContextEntry(
                    type=ContextEntryType.ACTION_RESULT,
                    content=content,
                    metadata={
                        "ok": True,
                        "model": response_model,
                        "tool_names": [
                            call["function"]["name"]
                            for call in tool_calls
                        ],
                    },
                )
            ],
        )

    def _execute_tool_calls(
        self,
        tool_calls: list[dict[str, Any]],
        *,
        state: WorkflowState,
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        machine_action_count = sum(
            str(call["function"]["name"]) == "apply_machine_action"
            for call in tool_calls
        )
        previous_machine_document = _successful_machine_document_id(
            state.last_action_result or {}
        )
        for call in tool_calls:
            name = str(call["function"]["name"])
            raw_arguments = call["function"].get("arguments") or "{}"
            try:
                if name == "apply_machine_action" and machine_action_count > 1:
                    raise ValueError(
                        "multiple apply_machine_action calls in one response are not allowed"
                    )
                arguments = json.loads(raw_arguments)
                if not isinstance(arguments, dict):
                    raise ValueError("tool arguments 必須是 JSON object")
                if name == "apply_machine_action" and previous_machine_document:
                    requested_document = (
                        str(arguments.get("document_id") or "").strip().upper()
                    )
                    if requested_document != previous_machine_document:
                        raise PermissionError(
                            "Reflect retry cannot switch machine_action document_id "
                            f"from {previous_machine_document} to "
                            f"{requested_document or '<missing>'}"
                        )
                result: dict[str, Any] = {
                    "ok": True,
                    "data": self._dispatcher.execute(
                        name,
                        arguments,
                        conversation=_conversation_transcript(state),
                        workflow_id=state.workflow_id,
                        retrieved_document_ids=_retrieval_document_ids(state),
                        perceived_intent=str(
                            state.lookup("perceived_intent") or ""
                        ),
                    ),
                }
            except Exception as exc:
                result = {
                    "ok": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            results.append(
                {
                    "tool_call_id": call["id"],
                    "name": name,
                    "result": result,
                }
            )
        return results


def _conversation_transcript(state: WorkflowState) -> str:
    if state.memory is not None:
        transcript = state.memory.as_text_transcript().strip()
        if transcript:
            return transcript
    return f"user: {state.latest_user_message()}"


def _retrieval_document_ids(state: WorkflowState) -> list[str]:
    value = state.lookup("retrieval_document_ids") or []
    if not isinstance(value, (list, tuple, set)):
        return []
    return [str(document_id) for document_id in value if str(document_id).strip()]


def _tool_result_for_model(result: object) -> object:
    """Keep downloadable artifact content out of the second model request."""

    if not isinstance(result, dict):
        return result
    data = result.get("data")
    if not isinstance(data, dict):
        return result
    artifact = data.get("artifact")
    if not isinstance(artifact, dict) or "content" not in artifact:
        return result

    public_artifact = {
        key: value for key, value in artifact.items() if key != "content"
    }
    public_artifact["content_length"] = len(str(artifact.get("content") or ""))
    return {
        **result,
        "data": {
            **data,
            "artifact": public_artifact,
        },
    }


def _build_messages(
    state: WorkflowState,
    system_prompt: str,
) -> list[dict[str, Any]]:
    retrieved = state.lookup("latest_retrieved_content") or state.lookup("retrieved_snippet") or ""
    perceived_details = state.lookup("perceived_details") or {}
    machine_action_document_ids = _machine_action_document_ids(state)
    correction = state.lookup("reflect_correction")
    correction_context: dict[str, Any] = {}
    if isinstance(correction, dict):
        previous_result = state.last_action_result or {}
        correction_context = {
            "auto_correction_instruction": (
                "上一版回答未通過 Reflect。請依 correction_reason 與 "
                "correction_suggestion 重新產生完整最終答案，只輸出修正版。"
            ),
            "correction_attempt": correction.get("attempt"),
            "correction_reason": correction.get("reason"),
            "correction_suggestion": correction.get("suggestion"),
            "previous_answer": correction.get("previous_answer")
            or previous_result.get("content")
            or "",
            "previous_tool_results": json.dumps(
                previous_result.get("tool_results") or [],
                ensure_ascii=False,
                default=str,
            )[:12000],
        }
        if _has_successful_machine_action(previous_result):
            correction_context["machine_action_retry_instruction"] = (
                "The previous apply_machine_action call succeeded. Any correction "
                "retry for the same document is idempotent; do not select a different "
                "document or emit multiple machine actions."
            )
    return build_module_messages(
        state.memory,
        system_prompt=system_prompt,
        extra_context={
            "perceived_intent": state.lookup("perceived_intent") or "",
            "perceived_summary": state.lookup("perceived_summary") or "",
            "perceived_details": json.dumps(perceived_details, ensure_ascii=False),
            "retrieved_context": retrieved,
            "available_machine_action_document_ids": json.dumps(
                machine_action_document_ids,
                ensure_ascii=False,
            ),
            **correction_context,
        },
        latest_user_message=state.latest_user_message(),
    )


def _machine_action_document_ids(state: WorkflowState) -> list[str]:
    value = state.lookup("retrieval_machine_action_document_ids") or []
    if not isinstance(value, (list, tuple, set)):
        return []
    return [
        str(document_id).strip().upper()
        for document_id in value
        if str(document_id).strip()
    ]


def _has_successful_machine_action(previous_result: dict[str, Any]) -> bool:
    return _successful_machine_document_id(previous_result) is not None


def _successful_machine_document_id(
    previous_result: dict[str, Any],
) -> str | None:
    for tool_result in previous_result.get("tool_results") or []:
        if not isinstance(tool_result, dict):
            continue
        result = tool_result.get("result")
        if (
            tool_result.get("name") == "apply_machine_action"
            and isinstance(result, dict)
            and result.get("ok") is True
        ):
            data = result.get("data")
            if not isinstance(data, dict):
                continue
            document_id = str(data.get("document_id") or "").strip().upper()
            if document_id:
                return document_id
    return None


def _needs_process_clarification(state: WorkflowState) -> bool:
    if bool(state.lookup("needs_process_clarification")):
        return True

    details = state.lookup("perceived_details") or {}
    if not isinstance(details, dict):
        return False
    query_type = str(details.get("query_type") or state.lookup("perceived_intent") or "")
    if query_type not in {"internal_fmea", "structured_fmea", "machine_control"}:
        return False
    processes = details.get("processes") or []
    has_process = isinstance(processes, list) and any(
        str(process).strip() for process in processes
    )
    return not has_process and not bool(details.get("cross_table"))


def _process_clarification_message(processes: object) -> str:
    if isinstance(processes, (list, tuple, set)):
        available = [str(process).strip() for process in processes if str(process).strip()]
    else:
        available = []
    if available:
        return (
            "這類原因會因製程與設備步驟不同而異。請問是在哪一個製程發生？"
            f"目前可查詢：{'、'.join(available)}。"
        )
    return "這類原因會因製程與設備步驟不同而異。請問是在哪一個製程發生？"


def _normalize_tool_calls(raw_calls: object) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    if not raw_calls:
        return normalized
    for index, raw_call in enumerate(raw_calls):
        function = _value(raw_call, "function") or {}
        call_id = str(_value(raw_call, "id") or f"fmea_tool_call_{index}")
        normalized.append(
            {
                "id": call_id,
                "type": str(_value(raw_call, "type") or "function"),
                "function": {
                    "name": str(_value(function, "name") or ""),
                    "arguments": str(_value(function, "arguments") or "{}"),
                },
            }
        )
    return normalized


def _value(source: object, key: str) -> object:
    if isinstance(source, dict):
        return source.get(key)
    return getattr(source, key, None)


def _combined_usage(
    responses: list[OpenAIChatResponse],
    model: str,
) -> dict[str, Any]:
    input_values = [response.input_tokens for response in responses if response.input_tokens is not None]
    output_values = [response.output_tokens for response in responses if response.output_tokens is not None]
    return {
        "model": model,
        "input_tokens": sum(input_values) if input_values else None,
        "output_tokens": sum(output_values) if output_values else None,
    }
