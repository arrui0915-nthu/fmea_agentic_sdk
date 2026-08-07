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
        self._callback({"type": "stage", "phase": "start", "label": "分析問題"})
        self._callback({"type": "token_delta", "module": "action", "content": "完整"})
        self._callback({"type": "stage", "phase": "finish", "label": "分析問題"})
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

    assert [(event.kind, event.payload) for event in events] == [
        ("stage", {"type": "stage", "phase": "start", "label": "分析問題"}),
        ("text", "完整"),
        ("stage", {"type": "stage", "phase": "finish", "label": "分析問題"}),
        ("text", "回答"),
    ]
    assert stream.result.final_message == "完整回答"
