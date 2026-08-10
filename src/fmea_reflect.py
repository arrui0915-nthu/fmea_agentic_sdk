"""FMEA-specific Reflect module with one bounded automatic correction pass."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from typing import Any

from agentic_sdk import ContextEntry, ContextEntryType, ModuleOutput, WorkflowState
from agentic_sdk.llm import (
    OpenAIChatResponse,
    chat_stream_json,
    require_model,
    resolve_openai_client,
)


REFLECT_SYSTEM_PROMPT = """你是 FMEA 回答的品質檢查器，只輸出 JSON。

請檢查目前回答是否：
1. 直接回答使用者的問題，沒有遺漏必要條件。
2. 公司內部 FMEA 事實、數字與結論都有 retrieved_context 或 tool_results 支持。
3. 沒有捏造失效模式、原因、控制、措施、S/O/D/RPN 或符合筆數。
4. 數值條件、排序、計數與 has_more 說明正確。
5. 資料不足時有明確說明，不把一般知識冒充為公司內部資料。

只在存在會影響正確性的具體問題時判定 fail，不要因措辭或排版偏好判定失敗。
回傳欄位：
- verdict: pass 或 fail
- reason: 一句簡短、可驗證的原因，不要輸出推理過程
- suggestion: fail 時提供一句具體修正指示；pass 時為空字串
"""


ReflectJsonRunner = Callable[..., OpenAIChatResponse]


class FmeaAutoCorrectReflect:
    """Validate the latest answer and route once back to Action when needed."""

    name = "reflect"
    gen_ai_system = "openai_compatible"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        max_corrections: int = 1,
        client: Any | None = None,
        chat_runner: ReflectJsonRunner = chat_stream_json,
    ) -> None:
        if max_corrections < 0:
            raise ValueError("max_corrections 不可小於 0")
        self._model = require_model(model, self.__class__.__name__)
        self._max_corrections = int(max_corrections)
        self._client = client or resolve_openai_client(
            self.__class__.__name__, api_key=api_key, base_url=base_url
        )
        self._chat_runner = chat_runner

    @property
    def gen_ai_request_model(self) -> str:
        return self._model

    def __call__(self, state: WorkflowState) -> ModuleOutput:
        correction_count = _non_negative_int(
            state.lookup("reflect_correction_count")
        )
        answer = str((state.last_action_result or {}).get("content") or "").strip()
        action_error = state.last_action_error

        try:
            response = self._chat_runner(
                self._client,
                model=self._model,
                system=REFLECT_SYSTEM_PROMPT,
                user=json.dumps(
                    _review_context(state, answer=answer, action_error=action_error),
                    ensure_ascii=False,
                    default=str,
                ),
                on_delta=lambda content: state.emit_token_delta(
                    self.name,
                    content,
                    metadata={"model": self._model, "structured": True},
                ),
                structured_fields=state.structured_fields_for(self.name),
                on_field=lambda field, value: state.emit_structured_field(
                    self.name,
                    field,
                    value,
                    metadata={"model": self._model, "structured": True},
                ),
            )
            parsed = response.as_json()
            verdict = str(parsed.get("verdict") or "").strip().lower()
            reason = str(parsed.get("reason") or "").strip()
            suggestion = str(parsed.get("suggestion") or "").strip()
            if verdict not in {"pass", "fail"}:
                verdict = "fail" if action_error or not answer else "pass"
                reason = reason or "Reflect 回傳格式不完整，已使用安全判定"
            usage: dict[str, Any] | None = {
                "model": response.model or self._model,
                "input_tokens": response.input_tokens,
                "output_tokens": response.output_tokens,
            }
        except Exception as exc:
            # A validator outage must not create a retry loop for an otherwise
            # successful answer. Action failures still receive one recovery pass.
            verdict = "fail" if action_error or not answer else "pass"
            reason = f"Reflect 暫時無法使用：{exc}"
            suggestion = "重新產生回答並避免沿用失敗結果" if verdict == "fail" else ""
            usage = None

        should_retry = verdict == "fail" and correction_count < self._max_corrections
        correction_exhausted = verdict == "fail" and not should_retry
        next_count = correction_count + 1 if should_retry else correction_count
        correction = (
            {
                "attempt": next_count,
                "reason": reason or "回答未通過品質檢查",
                "suggestion": suggestion or "依據現有證據重新產生正確答案",
                "previous_answer": answer,
            }
            if should_retry
            else None
        )

        metadata = {
            "verdict": verdict,
            "reason": reason or ("回答符合證據" if verdict == "pass" else "回答未通過品質檢查"),
            "strategy": "fmea_auto_correct",
            "correction_count": next_count,
            "max_corrections": self._max_corrections,
            "will_retry": should_retry,
            "correction_exhausted": correction_exhausted,
        }
        if suggestion:
            metadata["suggestion"] = suggestion

        payload: dict[str, Any] = {
            "reflect_verdict": verdict,
            "reflect_correction_count": next_count,
            "reflect_correction": correction,
            "reflect_correction_exhausted": correction_exhausted,
        }
        if usage is not None:
            payload["_llm_usage"] = usage

        return ModuleOutput(
            next_module="action" if should_retry else None,
            payload=payload,
            context_updates=[
                ContextEntry(
                    type=ContextEntryType.REFLECTION,
                    content=f"verdict={verdict} reason={metadata['reason']}",
                    metadata=metadata,
                )
            ],
        )


def _review_context(
    state: WorkflowState,
    *,
    answer: str,
    action_error: Mapping[str, Any] | None,
) -> dict[str, Any]:
    details = state.lookup("perceived_details") or {}
    retrieved = str(
        state.lookup("latest_retrieved_content")
        or state.lookup("retrieved_snippet")
        or ""
    )
    action_result = state.last_action_result or {}
    tool_results = action_result.get("tool_results") or []
    return {
        "user_question": state.latest_user_message(),
        "perceived_intent": state.lookup("perceived_intent") or "",
        "perceived_details": details,
        "answer": answer,
        "action_error": dict(action_error or {}),
        "retrieved_context": _bounded(retrieved, 12000),
        "tool_results": _bounded(
            json.dumps(tool_results, ensure_ascii=False, default=str),
            12000,
        ),
        "instruction": "只檢查答案，不要回答原始問題。",
    }


def _bounded(value: str, limit: int) -> str:
    return value if len(value) <= limit else value[: limit - 1] + "…"


def _non_negative_int(value: object) -> int:
    try:
        return max(0, int(value))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0
