"""Bridge Agentic SDK streaming events to a UI-safe iterator."""

from __future__ import annotations

from dataclasses import dataclass
from queue import Queue
from threading import Thread
from typing import Any, Literal

from agentic_sdk import WorkflowResult


@dataclass(frozen=True, slots=True)
class UiStreamEvent:
    """One event consumed by the Streamlit render thread."""

    kind: Literal["stage", "text"]
    payload: dict[str, Any] | str


class WorkflowUiStream:
    """Expose SDK stage events and answer deltas through one ordered queue.

    Agentic SDK runs its stream on a worker thread. The callback therefore only
    enqueues data; all Streamlit rendering remains on Streamlit's main thread.
    """

    def __init__(self, workflow: Any, user_message: str, session_id: str) -> None:
        self._workflow = workflow
        self._user_message = user_message
        self._session_id = session_id
        self._events: Queue[tuple[str, Any]] = Queue()
        self._thread: Thread | None = None
        self._result: WorkflowResult | None = None
        self._error: BaseException | None = None
        self._finished = False

    @property
    def result(self) -> WorkflowResult:
        if not self._finished:
            raise RuntimeError("WorkflowUiStream.result is available after iteration.")
        if self._error is not None:
            raise RuntimeError("WorkflowUiStream did not produce a result.") from self._error
        if self._result is None:
            raise RuntimeError("WorkflowUiStream completed without a result.")
        return self._result

    def __iter__(self) -> WorkflowUiStream:
        self._start()
        return self

    def __next__(self) -> UiStreamEvent:
        self._start()
        if self._finished:
            raise StopIteration

        kind, payload = self._events.get()
        if kind == "done":
            self._result = payload
            self._finished = True
            raise StopIteration
        if kind == "error":
            self._error = payload
            self._finished = True
            raise payload
        return UiStreamEvent(kind=kind, payload=payload)

    def _start(self) -> None:
        if self._thread is not None:
            return
        self._thread = Thread(
            target=self._consume_sdk_stream,
            name="fmea-ui-stream",
            daemon=True,
        )
        self._thread.start()

    def _consume_sdk_stream(self) -> None:
        def enqueue_event(event: dict[str, Any]) -> None:
            if event.get("type") == "stage":
                self._events.put(("stage", event))
                return
            if event.get("type") != "token_delta" or event.get("module") != "action":
                return
            metadata = event.get("metadata")
            if isinstance(metadata, dict) and metadata.get("structured") is True:
                return
            content = event.get("content")
            if content:
                self._events.put(("text", str(content)))

        try:
            sdk_stream = self._workflow.stream(
                self._user_message,
                session_id=self._session_id,
                event_callback=enqueue_event,
                yield_action_deltas=False,
            )
            # Normally Action deltas arrive through enqueue_event, preserving
            # their exact ordering with stage events. The SDK iterator still
            # yields a final fallback when an Action module emits no deltas.
            for delta in sdk_stream:
                if delta:
                    self._events.put(("text", str(delta)))
            self._events.put(("done", sdk_stream.result))
        except BaseException as exc:
            self._events.put(("error", exc))
