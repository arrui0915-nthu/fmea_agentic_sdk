import json
from typing import Any

from agentic_sdk import WorkflowState
from agentic_sdk.llm import OpenAIChatResponse

from src.tool_action import FmeaToolAction


class FakeDispatcher:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        self.calls.append((name, arguments))
        return {
            "total_matches": 1,
            "returned_count": 1,
            "limit": 20,
            "has_more": False,
            "records": [{"document_id": "TAZMO-0001", "rpn_before": 240}],
        }


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
    state = WorkflowState(user_message="列出 TAZMO RPN 大於 200 的項目")

    output = action(state)

    assert dispatcher.calls == [
        ("query_fmea_records", {"processes": ["TAZMO"], "rpn_min": 200})
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
