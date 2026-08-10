from types import SimpleNamespace

from src.agent_trace import AgentTraceRecorder


def test_trace_records_safe_stage_details_timings_and_usage() -> None:
    times = iter([10.0, 10.1, 10.35, 10.5])
    recorder = AgentTraceRecorder(clock=lambda: next(times))

    start_event = recorder.record_stage(
        {
            "type": "stage",
            "phase": "start",
            "module": "retrieve",
            "label": "搜尋 FMEA 資料",
            "module_class": "ProcessAwareFmeaRetrieve",
            "visit_count": 1,
            "visit_id": "workflow:retrieve:1",
            "state": object(),
        }
    )
    output = SimpleNamespace(
        payload={
            "retrieved_snippet": "must not be exposed",
            "_llm_usage": {
                "model": "test-model",
                "input_tokens": 12,
                "output_tokens": 3,
            },
        },
        context_updates=[
            SimpleNamespace(
                content="full private context",
                metadata={
                    "processes": ["PVD"],
                    "top_k": 5,
                    "hit_count": 4,
                    "private_key": "must not be exposed",
                },
            )
        ],
    )
    finish_event = recorder.record_stage(
        {
            "type": "stage",
            "phase": "finish",
            "module": "retrieve",
            "label": "搜尋 FMEA 資料",
            "module_class": "ProcessAwareFmeaRetrieve",
            "visit_count": 1,
            "visit_id": "workflow:retrieve:1",
            "fields": [{"field": "query", "value": "PVD failure"}],
            "output": output,
            "next_module": "action",
            "state": object(),
        }
    )
    recorder.finish()

    assert start_event["status"] == "running"
    assert "state" not in start_event
    assert "output" not in finish_event
    assert finish_event["duration_ms"] == 250
    assert finish_event["summary"] == {
        "processes": ["PVD"],
        "top_k": 5,
        "hit_count": 4,
    }
    assert finish_event["usage"] == {
        "model": "test-model",
        "input_tokens": 12,
        "output_tokens": 3,
    }
    assert recorder.snapshot["status"] == "complete"
    assert recorder.snapshot["duration_ms"] == 500
    assert recorder.snapshot["input_tokens"] == 12
    assert recorder.snapshot["output_tokens"] == 3


def test_trace_marks_unvisited_stages_skipped_and_running_stage_failed() -> None:
    times = iter([1.0, 1.1, 1.2])
    recorder = AgentTraceRecorder(clock=lambda: next(times))
    recorder.record_stage(
        {
            "phase": "start",
            "module": "perceive",
            "label": "理解問題",
            "visit_id": "workflow:perceive:1",
        }
    )

    recorder.finish(failed=True, reason="API unavailable")

    trace = recorder.snapshot
    assert trace["status"] == "error"
    assert trace["stages"][0]["status"] == "error"
    assert trace["stages"][0]["reason"] == "API unavailable"
    assert all(stage["status"] == "skipped" for stage in trace["stages"][1:])


def test_trace_honors_explicit_skipped_disposition_from_finished_module() -> None:
    times = iter([1.0, 1.1, 1.2, 1.3])
    recorder = AgentTraceRecorder(clock=lambda: next(times))
    recorder.record_stage(
        {
            "phase": "start",
            "module": "retrieve",
            "visit_id": "workflow:retrieve:1",
        }
    )

    event = recorder.record_stage(
        {
            "phase": "finish",
            "module": "retrieve",
            "visit_id": "workflow:retrieve:1",
            "output": SimpleNamespace(
                payload={
                    "_trace_status": "skipped",
                    "_trace_reason": "等待指定製程",
                },
                context_updates=[],
            ),
        }
    )

    assert event["status"] == "skipped"
    assert event["duration_ms"] is None
    assert event["reason"] == "等待指定製程"
    assert recorder.snapshot["stages"][2]["status"] == "skipped"


def test_trace_deduplicates_structured_fields_from_output_summary() -> None:
    times = iter([1.0, 1.1, 1.2, 1.3])
    recorder = AgentTraceRecorder(clock=lambda: next(times))
    recorder.record_stage(
        {
            "phase": "start",
            "module": "reflect",
            "visit_id": "workflow:reflect:1",
        }
    )

    event = recorder.record_stage(
        {
            "phase": "finish",
            "module": "reflect",
            "visit_id": "workflow:reflect:1",
            "fields": [
                {"field": "verdict", "value": "pass"},
                {"field": "reason", "value": "回答有資料支持"},
                {"field": "suggestion", "value": ""},
            ],
            "output": SimpleNamespace(
                payload={},
                context_updates=[
                    SimpleNamespace(
                        metadata={
                            "verdict": "pass",
                            "reason": "回答有資料支持",
                            "suggestion": "",
                            "strategy": "fmea_auto_correct",
                            "correction_count": 0,
                        }
                    )
                ],
            ),
        }
    )

    assert event["fields"] == [
        {"field": "verdict", "value": "pass"},
        {"field": "reason", "value": "回答有資料支持"},
        {"field": "suggestion", "value": ""},
    ]
    assert event["summary"] == {
        "strategy": "fmea_auto_correct",
        "correction_count": 0,
    }


def test_trace_preserves_repeated_reflect_attempts() -> None:
    current = 0.0

    def clock() -> float:
        nonlocal current
        current += 0.1
        return current

    recorder = AgentTraceRecorder(clock=clock)
    for visit, verdict, will_retry in ((1, "fail", True), (2, "pass", False)):
        visit_id = f"workflow:reflect:{visit}"
        recorder.record_stage(
            {
                "phase": "start",
                "module": "reflect",
                "label": "檢查回答",
                "visit_count": visit,
                "visit_id": visit_id,
            }
        )
        recorder.record_stage(
            {
                "phase": "finish",
                "module": "reflect",
                "label": "檢查回答",
                "visit_count": visit,
                "visit_id": visit_id,
                "output": SimpleNamespace(
                    payload={},
                    context_updates=[
                        SimpleNamespace(
                            metadata={
                                "verdict": verdict,
                                "reason": f"result={verdict}",
                                "will_retry": will_retry,
                            }
                        )
                    ],
                ),
            }
        )

    recorder.finish()

    reflect_stage = recorder.snapshot["stages"][-1]
    assert reflect_stage["visit_count"] == 2
    assert [attempt["summary"]["verdict"] for attempt in reflect_stage["attempts"]] == [
        "fail",
        "pass",
    ]
