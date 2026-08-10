from dataclasses import dataclass
from typing import Callable

from src.ui_stream import WorkflowUiStream


@dataclass
class FakeResult:
    final_message: str


class FakeSdkStream:
    def __init__(self, callback: Callable[[dict], None]) -> None:
        self._callback = callback
        self.result = FakeResult(final_message="完整回答")

    def __iter__(self):
        self._callback(
            {
                "type": "stage",
                "phase": "start",
                "module": "perceive",
                "visit_count": 1,
                "visit_id": "workflow:perceive:1",
                "label": "分析問題",
            }
        )
        self._callback({"type": "token_delta", "module": "action", "content": "完整"})
        self._callback(
            {
                "type": "stage",
                "phase": "finish",
                "module": "perceive",
                "visit_count": 1,
                "visit_id": "workflow:perceive:1",
                "label": "分析問題",
                "fields": [{"field": "intent", "value": "internal_fmea"}],
                "next_module": "action",
            }
        )
        self._callback({"type": "token_delta", "module": "action", "content": "回答"})
        return
        yield  # pragma: no cover - keeps this method an iterator


class FakeWorkflow:
    def stream(self, message: str, **kwargs) -> FakeSdkStream:
        assert message == "測試問題"
        assert kwargs["session_id"] == "session-1"
        assert kwargs["yield_action_deltas"] is False
        return FakeSdkStream(kwargs["event_callback"])


def test_ui_stream_forwards_stage_events_and_text_deltas() -> None:
    stream = WorkflowUiStream(FakeWorkflow(), "測試問題", "session-1")

    events = list(stream)

    assert [event.kind for event in events] == ["stage", "text", "stage", "text"]
    assert events[0].payload["phase"] == "start"
    assert events[0].payload["module"] == "perceive"
    assert events[1].payload == "完整"
    assert events[2].payload["phase"] == "finish"
    assert events[2].payload["fields"] == [
        {"field": "intent", "value": "internal_fmea"}
    ]
    assert events[2].payload["next_module"] == "action"
    assert events[3].payload == "回答"
    assert stream.result.final_message == "完整回答"
    assert stream.trace["status"] == "complete"
    assert stream.trace["stages"][0]["status"] == "complete"
    assert all(stage["status"] == "skipped" for stage in stream.trace["stages"][1:])
