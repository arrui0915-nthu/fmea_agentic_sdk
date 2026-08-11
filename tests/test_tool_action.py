import json
from typing import Any

from agentic_sdk import WorkflowState
from agentic_sdk.llm import OpenAIChatResponse

from src.fmea_tools import FmeaToolDispatcher
from src.tool_action import FmeaToolAction, _build_messages


class FakeDispatcher:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.contexts: list[dict[str, Any]] = []

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
        self.calls.append((name, arguments))
        self.contexts.append(
            {
                "conversation": conversation,
                "workflow_id": workflow_id,
                "retrieved_document_ids": retrieved_document_ids,
                "perceived_intent": perceived_intent,
            }
        )
        return {
            "total_matches": 1,
            "returned_count": 1,
            "limit": 20,
            "has_more": False,
            "records": [{"document_id": "TAZMO-0001", "rpn_before": 240}],
        }


class FakeQueryService:
    def query_records(self, **kwargs: Any) -> dict[str, Any]:
        return {"records": [], "arguments": kwargs}


class FakeMachineActionService:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def execute(
        self,
        document_id: str,
        *,
        allowed_document_ids: list[str],
        idempotency_key: str,
    ) -> dict[str, Any]:
        self.calls.append(
            {
                "document_id": document_id,
                "allowed_document_ids": allowed_document_ids,
                "idempotency_key": idempotency_key,
            }
        )
        return {"document_id": document_id, "changed": True}


def test_action_executes_tool_and_sends_result_back_to_model() -> None:
    dispatcher = FakeDispatcher()
    requests: list[dict[str, Any]] = []
    responses = iter(
        [
            OpenAIChatResponse(
                content="",
                model="test-model",
                input_tokens=10,
                output_tokens=3,
                tool_calls=[
                    {
                        "id": "call-1",
                        "type": "function",
                        "function": {
                            "name": "query_fmea_records",
                            "arguments": '{"processes":["TAZMO"],"rpn_min":200}',
                        },
                    }
                ],
            ),
            OpenAIChatResponse(
                content="找到 1 筆高風險紀錄。",
                model="test-model",
                input_tokens=20,
                output_tokens=8,
            ),
        ]
    )

    def chat_runner(client: object, **kwargs: Any) -> OpenAIChatResponse:
        requests.append(kwargs)
        response = next(responses)
        if callback := kwargs.get("on_delta"):
            callback(response.content)
        return response

    action = FmeaToolAction(
        model="test-model",
        system_prompt="test",
        tools=[{"type": "function"}],
        dispatcher=dispatcher,  # type: ignore[arg-type]
        client=object(),
        chat_runner=chat_runner,
    )
    state = WorkflowState(
        user_message="列出 TAZMO RPN 大於 200 的項目",
        workflow_id="workflow-123",
    )
    state.entities.update(
        {
            "retrieval_document_ids": ["TAZMO-0001"],
            "perceived_intent": "structured_fmea",
            "perceived_details": {
                "query_type": "structured_fmea",
                "processes": ["TAZMO"],
            },
        }
    )

    output = action(state)

    assert dispatcher.calls == [
        ("query_fmea_records", {"processes": ["TAZMO"], "rpn_min": 200})
    ]
    assert dispatcher.contexts == [
        {
            "conversation": "user: 列出 TAZMO RPN 大於 200 的項目",
            "workflow_id": "workflow-123",
            "retrieved_document_ids": ["TAZMO-0001"],
            "perceived_intent": "structured_fmea",
        }
    ]
    assert output["payload"]["latest_final_message"] == "找到 1 筆高風險紀錄。"
    assert output["payload"]["_llm_usage"] == {
        "model": "test-model",
        "input_tokens": 30,
        "output_tokens": 11,
    }
    tool_message = requests[1]["messages"][-1]
    assert tool_message["role"] == "tool"
    assert tool_message["tool_call_id"] == "call-1"
    assert json.loads(tool_message["content"])["data"]["total_matches"] == 1
    assert state.last_action_result is not None
    assert state.last_action_result["content"] == "找到 1 筆高風險紀錄。"


def test_action_still_answers_normally_when_model_does_not_call_a_tool() -> None:
    dispatcher = FakeDispatcher()
    deltas: list[str] = []

    def chat_runner(client: object, **kwargs: Any) -> OpenAIChatResponse:
        return OpenAIChatResponse(
            content="FMEA 是失效模式與效應分析。",
            model="test-model",
            input_tokens=5,
            output_tokens=7,
            tool_calls=[],
        )

    action = FmeaToolAction(
        model="test-model",
        system_prompt="test",
        tools=[{"type": "function"}],
        dispatcher=dispatcher,  # type: ignore[arg-type]
        client=object(),
        chat_runner=chat_runner,
    )
    state = WorkflowState(user_message="什麼是 FMEA？")
    state.set_token_delta_callback(
        lambda module, content, metadata: deltas.append(content)
    )

    output = action(state)

    assert dispatcher.calls == []
    assert output["payload"]["latest_final_message"] == "FMEA 是失效模式與效應分析。"
    assert deltas == ["FMEA 是失效模式與效應分析。"]


def test_action_asks_for_process_without_calling_model_or_tool() -> None:
    dispatcher = FakeDispatcher()
    requests: list[dict[str, Any]] = []
    deltas: list[str] = []

    def chat_runner(client: object, **kwargs: Any) -> OpenAIChatResponse:
        requests.append(kwargs)
        raise AssertionError("clarification must not call the model")

    action = FmeaToolAction(
        model="test-model",
        system_prompt="test",
        tools=[{"type": "function"}],
        dispatcher=dispatcher,  # type: ignore[arg-type]
        available_processes=["PVD", "ECD"],
        client=object(),
        chat_runner=chat_runner,
    )
    state = WorkflowState(user_message="晶圓破片是什麼原因？")
    state.entities.update(
        {
            "perceived_intent": "internal_fmea",
            "perceived_details": {
                "query_type": "internal_fmea",
                "processes": [],
                "cross_table": False,
            },
        }
    )
    state.set_token_delta_callback(
        lambda module, content, metadata: deltas.append(content)
    )

    output = action(state)

    assert requests == []
    assert dispatcher.calls == []
    assert output["payload"]["latest_tool_calls"] == []
    assert output["payload"]["latest_final_message"] == (
        "這類原因會因製程與設備步驟不同而異。請問是在哪一個製程發生？"
        "目前可查詢：ECD、PVD。"
    )
    assert deltas == [output["payload"]["latest_final_message"]]


def test_tool_failure_is_returned_to_model_instead_of_executing_unknown_code() -> None:
    dispatcher = FakeDispatcher()
    requests: list[dict[str, Any]] = []
    responses = iter(
        [
            OpenAIChatResponse(
                content="",
                model="test-model",
                tool_calls=[
                    {
                        "id": "call-1",
                        "type": "function",
                        "function": {
                            "name": "query_fmea_records",
                            "arguments": "not-json",
                        },
                    }
                ],
            ),
            OpenAIChatResponse(content="查詢條件格式錯誤。", model="test-model"),
        ]
    )

    def chat_runner(client: object, **kwargs: Any) -> OpenAIChatResponse:
        requests.append(kwargs)
        return next(responses)

    action = FmeaToolAction(
        model="test-model",
        system_prompt="test",
        tools=[{"type": "function"}],
        dispatcher=dispatcher,  # type: ignore[arg-type]
        client=object(),
        chat_runner=chat_runner,
    )

    output = action(WorkflowState(user_message="查詢"))

    tool_result = json.loads(requests[1]["messages"][-1]["content"])
    assert tool_result["ok"] is False
    assert dispatcher.calls == []
    assert output["payload"]["latest_final_message"] == "查詢條件格式錯誤。"


def test_multiple_machine_actions_are_all_rejected_before_dispatch() -> None:
    dispatcher = FakeDispatcher()
    requests: list[dict[str, Any]] = []
    responses = iter(
        [
            OpenAIChatResponse(
                content="",
                model="test-model",
                tool_calls=[
                    {
                        "id": "machine-1",
                        "type": "function",
                        "function": {
                            "name": "apply_machine_action",
                            "arguments": '{"document_id":"PVD-0001"}',
                        },
                    },
                    {
                        "id": "machine-2",
                        "type": "function",
                        "function": {
                            "name": "apply_machine_action",
                            "arguments": '{"document_id":"PVD-0002"}',
                        },
                    },
                ],
            ),
            OpenAIChatResponse(
                content="一次只能套用一組機台參數。",
                model="test-model",
            ),
        ]
    )

    def chat_runner(client: object, **kwargs: Any) -> OpenAIChatResponse:
        requests.append(kwargs)
        return next(responses)

    action = FmeaToolAction(
        model="test-model",
        system_prompt="test",
        tools=[{"type": "function"}],
        dispatcher=dispatcher,  # type: ignore[arg-type]
        client=object(),
        chat_runner=chat_runner,
    )
    state = WorkflowState(user_message="依照結果調整機台", workflow_id="wf-1")
    state.entities.update(
        {
            "perceived_intent": "machine_control",
            "perceived_details": {
                "query_type": "machine_control",
                "processes": ["PVD"],
            },
            "retrieval_document_ids": ["PVD-0001", "PVD-0002"],
        }
    )

    output = action(state)

    assert dispatcher.calls == []
    tool_results = output["payload"]["latest_tool_results"]
    assert len(tool_results) == 2
    assert all(result["result"]["ok"] is False for result in tool_results)
    assert all(
        "multiple apply_machine_action calls" in result["result"]["error"]
        for result in tool_results
    )
    assert len(requests[1]["messages"]) >= 2


def test_internal_fmea_intent_cannot_execute_machine_action() -> None:
    machine_service = FakeMachineActionService()
    dispatcher = FmeaToolDispatcher(
        FakeQueryService(),  # type: ignore[arg-type]
        machine_action_service=machine_service,  # type: ignore[arg-type]
    )
    requests: list[dict[str, Any]] = []
    responses = iter(
        [
            OpenAIChatResponse(
                content="",
                model="test-model",
                tool_calls=[
                    {
                        "id": "machine-1",
                        "type": "function",
                        "function": {
                            "name": "apply_machine_action",
                            "arguments": '{"document_id":"PVD-0001"}',
                        },
                    }
                ],
            ),
            OpenAIChatResponse(
                content="這是查詢，不會調整機台。",
                model="test-model",
            ),
        ]
    )

    def chat_runner(client: object, **kwargs: Any) -> OpenAIChatResponse:
        requests.append(kwargs)
        return next(responses)

    action = FmeaToolAction(
        model="test-model",
        system_prompt="test",
        tools=[{"type": "function"}],
        dispatcher=dispatcher,
        client=object(),
        chat_runner=chat_runner,
    )
    state = WorkflowState(user_message="查詢 PVD-0001", workflow_id="wf-1")
    state.entities.update(
        {
            "perceived_intent": "internal_fmea",
            "perceived_details": {
                "query_type": "internal_fmea",
                "processes": ["PVD"],
            },
            "retrieval_document_ids": ["PVD-0001"],
        }
    )

    output = action(state)

    assert machine_service.calls == []
    tool_result = output["payload"]["latest_tool_results"][0]["result"]
    assert tool_result["ok"] is False
    assert "machine_control" in tool_result["error"]
    assert "machine_control" in requests[1]["messages"][-1]["content"]


def test_action_messages_include_reflect_correction_feedback() -> None:
    state = WorkflowState(user_message="查詢高風險項目")
    state.entities.update(
        {
            "reflect_correction": {
                "attempt": 1,
                "reason": "回答筆數與工具結果不一致",
                "suggestion": "使用 total_matches 的正確數值",
                "previous_answer": "共有 2 筆",
            },
            "perceived_intent": "structured_fmea",
        }
    )
    state.last_action_result = {
        "content": "共有 2 筆",
        "tool_results": [{"result": {"data": {"total_matches": 3}}}],
    }

    messages = _build_messages(state, "system")

    system_message = messages[0]["content"]
    assert "上一版回答未通過 Reflect" in system_message
    assert "回答筆數與工具結果不一致" in system_message
    assert "使用 total_matches 的正確數值" in system_message
    assert "共有 2 筆" in system_message
    assert "total_matches" in system_message


def test_action_messages_include_executable_machine_document_ids() -> None:
    state = WorkflowState(user_message="請直接調整 PVD 機台")
    state.entities.update(
        {
            "perceived_intent": "machine_control",
            "retrieval_machine_action_document_ids": [
                "PVD-0008",
                "PVD-0009",
            ],
        }
    )

    messages = _build_messages(state, "system")

    system_message = messages[0]["content"]
    assert "available_machine_action_document_ids" in system_message
    assert "PVD-0008" in system_message


def test_reflect_retry_is_told_successful_machine_action_is_idempotent() -> None:
    state = WorkflowState(user_message="依照 PVD-0001 再確認一次")
    state.entities.update(
        {
            "reflect_correction": {
                "attempt": 1,
                "reason": "回答缺少執行摘要",
                "suggestion": "回報執行結果",
            },
            "perceived_intent": "machine_control",
        }
    )
    state.last_action_result = {
        "content": "已執行",
        "tool_results": [
            {
                "name": "apply_machine_action",
                "result": {"ok": True, "data": {"document_id": "PVD-0001"}},
            }
        ],
    }

    messages = _build_messages(state, "system")

    system_message = messages[0]["content"]
    assert "previous apply_machine_action call succeeded" in system_message
    assert "idempotent" in system_message


def test_reflect_retry_cannot_switch_to_a_different_machine_document() -> None:
    dispatcher = FakeDispatcher()
    responses = iter(
        [
            OpenAIChatResponse(
                content="",
                model="test-model",
                tool_calls=[
                    {
                        "id": "machine-retry",
                        "type": "function",
                        "function": {
                            "name": "apply_machine_action",
                            "arguments": '{"document_id":"PVD-0002"}',
                        },
                    }
                ],
            ),
            OpenAIChatResponse(
                content="未切換至其他機台設定。",
                model="test-model",
            ),
        ]
    )

    action = FmeaToolAction(
        model="test-model",
        system_prompt="test",
        tools=[{"type": "function"}],
        dispatcher=dispatcher,  # type: ignore[arg-type]
        client=object(),
        chat_runner=lambda client, **kwargs: next(responses),
    )
    state = WorkflowState(
        user_message="修正上一個回答",
        workflow_id="workflow-1",
    )
    state.entities.update(
        {
            "perceived_intent": "machine_control",
            "perceived_details": {
                "query_type": "machine_control",
                "processes": ["PVD"],
            },
            "retrieval_document_ids": ["PVD-0001", "PVD-0002"],
            "reflect_correction": {"attempt": 1, "reason": "回答需要修正"},
        }
    )
    state.last_action_result = {
        "content": "已執行 PVD-0001",
        "tool_results": [
            {
                "name": "apply_machine_action",
                "result": {
                    "ok": True,
                    "data": {"document_id": "PVD-0001"},
                },
            }
        ],
    }

    output = action(state)

    assert dispatcher.calls == []
    tool_result = output["payload"]["latest_tool_results"][0]["result"]
    assert tool_result["ok"] is False
    assert "cannot switch" in tool_result["error"]


class FakeReportDispatcher:
    def __init__(self) -> None:
        self.conversation = ""

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
        assert name == "generate_session_report"
        assert arguments["title"] == "PVD 對話報告"
        self.conversation = conversation
        return {
            "artifact": {
                "filename": "report.html",
                "mime_type": "text/html",
                "content": "<html>download me</html>",
            }
        }


def test_action_generates_report_from_session_transcript_without_resending_artifact() -> None:
    from agentic_sdk.memory.in_context import InContextMemory

    dispatcher = FakeReportDispatcher()
    requests: list[dict[str, Any]] = []
    responses = iter(
        [
            OpenAIChatResponse(
                content="",
                model="test-model",
                tool_calls=[
                    {
                        "id": "report-call",
                        "type": "function",
                        "function": {
                            "name": "generate_session_report",
                            "arguments": json.dumps(
                                {
                                    "title": "PVD 對話報告",
                                    "objective": "整理討論",
                                    "processes": ["PVD"],
                                    "executive_summary": "找到高風險項目。",
                                    "key_findings": [],
                                    "action_items": [],
                                    "open_questions": [],
                                },
                                ensure_ascii=False,
                            ),
                        },
                    }
                ],
            ),
            OpenAIChatResponse(
                content="報告已完成，可下載 HTML 檔案。",
                model="test-model",
            ),
        ]
    )

    def chat_runner(client: object, **kwargs: Any) -> OpenAIChatResponse:
        requests.append(kwargs)
        return next(responses)

    memory = InContextMemory()
    memory.append_message("user", "PVD 有哪些高風險項目？")
    memory.append_message("assistant", "最高 RPN 為 200。")
    memory.append_message("user", "幫我產生本次對話報告")
    state = WorkflowState(
        user_message="幫我產生本次對話報告",
        memory=memory,
    )
    action = FmeaToolAction(
        model="test-model",
        system_prompt="test",
        tools=[{"type": "function"}],
        dispatcher=dispatcher,  # type: ignore[arg-type]
        client=object(),
        chat_runner=chat_runner,
    )

    output = action(state)

    assert "PVD 有哪些高風險項目" in dispatcher.conversation
    assert "最高 RPN 為 200" in dispatcher.conversation
    raw_artifact = output["payload"]["latest_tool_results"][0]["result"]["data"]["artifact"]
    assert raw_artifact["content"] == "<html>download me</html>"
    model_tool_result = json.loads(requests[1]["messages"][-1]["content"])
    model_artifact = model_tool_result["data"]["artifact"]
    assert "content" not in model_artifact
    assert model_artifact["content_length"] == len("<html>download me</html>")
