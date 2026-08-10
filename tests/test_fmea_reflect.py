from collections.abc import Iterator
from typing import Any

from agentic_sdk import (
    ContextEntry,
    ContextEntryType,
    ModuleOutput,
    Workflow,
    WorkflowState,
)
from agentic_sdk.llm import OpenAIChatResponse

from src.fmea_reflect import FmeaAutoCorrectReflect


def _responses(*items: OpenAIChatResponse):
    responses: Iterator[OpenAIChatResponse] = iter(items)

    def runner(client: object, **kwargs: Any) -> OpenAIChatResponse:
        response = next(responses)
        if callback := kwargs.get("on_field"):
            for field, value in response.as_json().items():
                callback(field, value)
        return response

    return runner


def _state(answer: str = "錯誤回答") -> WorkflowState:
    state = WorkflowState(user_message="PVD 有幾筆 RPN 大於 100？")
    state.entities.update(
        {
            "perceived_intent": "structured_fmea",
            "perceived_details": {
                "query_type": "structured_fmea",
                "processes": ["PVD"],
            },
        }
    )
    state.last_action_result = {
        "content": answer,
        "tool_results": [{"result": {"data": {"total_matches": 3}}}],
    }
    return state


def test_failed_reflect_routes_back_to_action_with_correction_context() -> None:
    reflect = FmeaAutoCorrectReflect(
        model="test-model",
        client=object(),
        chat_runner=_responses(
            OpenAIChatResponse(
                content=(
                    '{"verdict":"fail","reason":"回答說 2 筆，但工具結果是 3 筆",'
                    '"suggestion":"改為 3 筆"}'
                ),
                model="test-model",
                input_tokens=20,
                output_tokens=8,
            )
        ),
    )

    output = reflect(_state())

    assert output["next_module"] == "action"
    assert output["payload"]["reflect_verdict"] == "fail"
    assert output["payload"]["reflect_correction_count"] == 1
    assert output["payload"]["reflect_correction"] == {
        "attempt": 1,
        "reason": "回答說 2 筆，但工具結果是 3 筆",
        "suggestion": "改為 3 筆",
        "previous_answer": "錯誤回答",
    }
    assert output["context_updates"][0].metadata["will_retry"] is True


def test_reflect_pass_ends_workflow_and_clears_correction() -> None:
    state = _state("正確回答")
    state.entities.update(
        {
            "reflect_correction_count": 1,
            "reflect_correction": {"reason": "上一版筆數錯誤"},
        }
    )
    reflect = FmeaAutoCorrectReflect(
        model="test-model",
        client=object(),
        chat_runner=_responses(
            OpenAIChatResponse(
                content='{"verdict":"pass","reason":"回答與工具結果一致","suggestion":""}',
                model="test-model",
            )
        ),
    )

    output = reflect(state)

    assert output["next_module"] is None
    assert output["payload"]["reflect_verdict"] == "pass"
    assert output["payload"]["reflect_correction"] is None
    assert output["payload"]["reflect_correction_exhausted"] is False


def test_failed_reflect_stops_after_correction_limit() -> None:
    state = _state()
    state.entities.update({"reflect_correction_count": 1})
    reflect = FmeaAutoCorrectReflect(
        model="test-model",
        max_corrections=1,
        client=object(),
        chat_runner=_responses(
            OpenAIChatResponse(
                content='{"verdict":"fail","reason":"仍然不正確","suggestion":""}',
                model="test-model",
            )
        ),
    )

    output = reflect(state)

    assert output["next_module"] is None
    assert output["payload"]["reflect_correction_exhausted"] is True
    assert output["context_updates"][0].metadata["will_retry"] is False


class _DirectPerceive:
    name = "perceive"

    def __call__(self, state: WorkflowState) -> ModuleOutput:
        return ModuleOutput(next_module="action")


class _CorrectingAction:
    name = "action"

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, state: WorkflowState) -> ModuleOutput:
        self.calls += 1
        content = "正確答案：3 筆" if state.lookup("reflect_correction") else "錯誤答案：2 筆"
        state.last_action_error = None
        state.last_action_result = {"content": content, "tool_results": []}
        return ModuleOutput(
            next_module=None,
            payload={"latest_final_message": content},
            context_updates=[
                ContextEntry(
                    type=ContextEntryType.ACTION_RESULT,
                    content=content,
                    metadata={"ok": True},
                )
            ],
        )


def test_sdk_workflow_runs_action_reflect_correction_loop() -> None:
    action = _CorrectingAction()
    reflect = FmeaAutoCorrectReflect(
        model="test-model",
        client=object(),
        chat_runner=_responses(
            OpenAIChatResponse(
                content=(
                    '{"verdict":"fail","reason":"筆數錯誤",'
                    '"suggestion":"依工具結果改為 3 筆"}'
                ),
                model="test-model",
            ),
            OpenAIChatResponse(
                content='{"verdict":"pass","reason":"筆數正確","suggestion":""}',
                model="test-model",
            ),
        ),
    )
    workflow = Workflow(
        workflow_name="auto-correct-test",
        perceive=_DirectPerceive(),
        action=action,
        reflect=reflect,
        events_schema={
            "perceive": {"label": "理解", "fields": []},
            "action": {"label": "回答", "fields": []},
            "reflect": {"label": "檢查", "fields": ["*"]},
        },
    )

    result = workflow.run("測試自動修正")

    assert result.final_message == "正確答案：3 筆"
    assert result.visit_counts == {"perceive": 1, "action": 2, "reflect": 2}
    assert result.entities["reflect_verdict"] == "pass"
    assert result.entities["reflect_correction_count"] == 1
