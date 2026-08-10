# R300-AI Agentic-SDK c30 Bug 驗證報告

## 1. 結論

本次只驗證 [R300-AI/Agentic-SDK `c30e449d5cb781fa541311dd31203fdadeedf354`](https://github.com/R300-AI/Agentic-SDK/tree/c30e449d5cb781fa541311dd31203fdadeedf354)，不把 `main` 的後續版本混入結論。

- 環境：Python 3.12.7、`agentic-sdk==0.1.0`。
- 版本證據：安裝套件的 `direct_url.json` 同時記錄 `commit_id` 與 `requested_revision` 為 `c30e449…`。
- SDK：確認 **9 項問題**，其中 6 項由離線 regression tests 穩定重現，3 項由獨立 probe 重現。
- FMEA 應用：確認 **6 項整合問題**；現有測試雖為 `46 passed`，仍未涵蓋模型輸出異常、工具漏呼叫及 fail-open 情境。
- 全程使用 fake client／fake KB，沒有呼叫 Azure/OpenAI、沒有改寫知識庫、沒有建立 Issue 或對外上報。

最高優先處理：`SDK-05`、`SDK-08`、`SDK-09`、`APP-01`、`APP-02`、`APP-04`、`APP-05`。

| 評量需求 | 本次交付 |
| --- | --- |
| 找到開發中工具的問題 | 9 項 SDK 問題、6 項應用整合問題 |
| 提供可重現步驟或紀錄 | 固定 commit、測試命令、失敗案例名稱與 deterministic probe 輸出 |
| Issue／上報 | 依需求不執行；以本地 Markdown 報告留存 |

## 2. SDK 問題總表

| ID | 嚴重度 | 已確認問題 | 重現證據 | 對目前 FMEA app |
| --- | --- | --- | --- | --- |
| SDK-01 | 高 | 傳入同一個 `InContextMemory()` instance 時，session B 會讀到 session A 對話 | B 的 memory 出現 `secret-from-a` | 目前未傳 instance，暫不可達 |
| SDK-02 | 高 | 連續兩次相同 assistant 回答，第二次不寫入 memory | 預期 4 turns，實際 3 turns | **直接可達**；固定製程澄清文字會觸發 |
| SDK-03 | 高 | `TextPerceive` 搭配 persistent memory 會重複寫入 user turn | 預期 2 turns，實際 3 turns | 目前使用 in-context，暫不可達 |
| SDK-04 | 高 | 同 session 併行 `run()` 發生 lost update | 5/5 次只存 2 turns，預期 4 | 重複提交或 server 併行時可達 |
| SDK-05 | 高 | 空白／keepalive stream chunk 可繞過 idle timeout | `TimeoutError` 未發生 | **所有 LLM stage 可達** |
| SDK-06 | 低 | `InMemoryStore.search(top_k=-1)` 接受負數並套用 Python 負切片 | 預期 `ValueError`，實際正常回傳 | app 使用自訂 KB，暫不可達 |
| SDK-07 | 中 | 不同路徑的同名 semantic source 會互相覆寫 | 兩個 `index.md` 都保存為 `saved/index.md` | app 使用自訂 KB，暫不可達 |
| SDK-08 | 高 | `Gates.timeout_sec` 無法限制單一長時間或最後一個 module | timeout 10 ms，執行約 94 ms，仍 `aborted=False` | **LLM／embedding 卡住時可達** |
| SDK-09 | 高 | structured JSON 無法解析時，`TextPerceive` 靜默降級為 `general` | `NOT JSON` 得到 `intent=general, details={}`，且未 abort | **可能跳過內部 FMEA retrieval** |

主要根因位置：

- `agentic_sdk/core/workflow.py:174-182, 305-315, 492-513`
- `agentic_sdk/core/gates.py:15-22`
- `agentic_sdk/llm/openai_compatible.py:22-34, 331-348`
- `agentic_sdk/modules/perceive/text.py:92-121`
- `agentic_sdk/memory/in_memory.py:128-171`
- `agentic_sdk/modules/retrieve/semantic.py:195-209`

## 3. FMEA workflow 應用層問題

| ID | 嚴重度 | 問題與實測結果 | 位置 |
| --- | --- | --- | --- |
| APP-01 | 高 | `structured_fmea` 只靠 prompt 要求工具；`tool_choice="auto"` 下，模型不呼叫工具仍可直接產生數值答案，dispatcher 實際呼叫 0 次 | `src/tool_action.py:102-120` |
| APP-02 | 高 | Perceive 雖判定只查 PVD，但模型工具參數若為 `{}`，scope 未被程式強制注入，QueryService 會查全部製程 | `src/tool_action.py:205-233`、`src/fmea_query.py:150-160` |
| APP-03 | 中高 | Perceive payload 缺 schema 驗證：`cross_table="false"` 被視為 True 並查全部；`processes=["UNKNOWN"]` 又會跳過澄清、最後選到 0 個來源 | `src/process_retrieve.py:30-39, 55-77, 105-113` |
| APP-04 | 高 | FAISS 沒有最低相似度門檻；score `-0.99` 仍算一個 hit，`EvidenceCheckReflect` 因 `hit_count=1` 判定 pass | `src/faiss_knowledge_base.py:193-209`、`src/process_retrieve.py:88-99` |
| APP-05 | 高 | 工具執行失敗會包成 `tool_result.ok=false`，但第二段模型有回答後程式清掉 `last_action_error`；實測 Reflect 仍為 pass | `src/tool_action.py:122-174, 190-200` |
| APP-06 | 中高 | SDK 把 `WorkflowAborted` 回傳成 result，不會丟 exception；聊天頁未檢查 `result.aborted`／`reflect_verdict`，仍顯示「處理完成」 | `app.py:245-252`；Preview 的正確對照在 `app.py:381-382` |

直接影響目前 workflow 的例子：連續兩輪都沒提供有效製程時，UI 會顯示兩次相同澄清，但 `SDK-02` 讓 memory 只保留第一次 assistant 澄清。第三輪若只回答 `PVD`，UI 歷史與模型實際看到的歷史已不一致。

## 4. 可重現紀錄

### 4.1 確認被測版本

```powershell
python -c "import agentic_sdk,importlib.metadata as m; print(agentic_sdk.__file__); print(m.distribution('agentic-sdk').read_text('direct_url.json'))"
```

結果中的 commit：

```text
c30e449d5cb781fa541311dd31203fdadeedf354
```

### 4.2 現有應用測試

```powershell
python -m pytest -q --basetemp "$env:TEMP\fmea-sdk-c30-tests"
```

```text
46 passed in 3.36s
```

### 4.3 六項 SDK regression tests

測試描述的是「安全／正確行為」，因此下面的 failure 代表 bug 被成功重現。`--import-mode=importlib` 搭配上一節的版本檢查，確保匯入 installed c30，而不是 `.research` 內的另一份 checkout。

```powershell
python -m pytest -c NUL --rootdir . --import-mode=importlib `
  -p no:cacheprovider --tb=no -q `
  .research\Agentic-SDK\research_tests\test_core_module_regressions.py
```

```text
FFFFFF [100%]

FAILED test_memory_instance_isolated_by_session
FAILED test_equal_consecutive_answers_are_both_recorded
FAILED test_text_perceive_does_not_duplicate_persistent_conversation_turn
FAILED test_concurrent_same_session_runs_do_not_lose_turns
FAILED test_stream_idle_timeout_counts_empty_provider_chunks
FAILED test_negative_top_k_is_rejected_instead_of_python_negative_slice

6 failed in 2.29s
```

### 4.4 額外離線 probe 紀錄

測試方式：slow Action、非法 JSON stream、同名來源、fake tool call 與 fake retrieval hit；全部不連網。

```text
GATE_TIMEOUT       timeout_ms=10 elapsed_ms=94 aborted=False final='ok'
INVALID_JSON       intent=general details={} aborted=False
SOURCE_COLLISION   targets=['saved/index.md','saved/index.md'] unique_targets=1
STRING_FALSE       selected=['ECD','PVD'] searches={'ECD':1,'PVD':1}
UNKNOWN_PROCESS    clarification=None selected=[]
TOOL_SCOPE         perceived=['PVD'] dispatcher_args={} effective_scope=ALL
TOOL_FAIL_REFLECT  tool_ok=False reflect_verdict=pass
NEGATIVE_HIT       score=-0.99 hit_count=1 reflect_verdict=pass
UI_ABORT_RESULT    aborted=True final_message=''; UI path does not raise
```

正向控制：未知工具 `delete_fmea_record` 會被 allow-list 拒絕；缺少必要環境變數會明確拋出 `ConfigurationError`。

## 5. 建議修正順序

1. **先關閉查詢 fail-open**：`structured_fmea` 必須取得成功的工具結果；general 路徑不要提供內部查詢工具；工具 `processes` 必須由 state 強制限制，只有使用者明確要求跨製程才允許全查。
2. **嚴格驗證 module payload**：用 schema 驗證 `query_type/processes/cross_table/complexity`；非法 JSON、字串 boolean、未知製程應 retry、abort 或重新澄清，不能預設為 general／全部製程。
3. **讓證據檢查真的 fail-closed**：設定經校準的最低 cosine similarity；必要工具任一失敗就保留 `last_action_error`；Reflect 同時檢查 tool results、有效 hit 與分數。
4. **修正 timeout 與 UI 狀態**：SDK 在 module 返回後再次檢查 deadline，並提供 transport timeout／取消機制；app 在顯示完成前檢查 `result.aborted` 與 `reflect_verdict`。
5. **修正 memory 一致性**：instance 需 per-session clone；同回答不能用文字內容去重；同 session 更新需 lock 或版本檢查；persistent entry 必須依 `entry_type` 區分對話 turn。
6. **補回歸測試**：加入「重複澄清」、「structured 但無 tool call」、「PVD scope + 空 tool args」、「`"false"` 字串」、「低相似度」、「tool fail + model 成功文字」及「aborted UI」情境。

## 6. 範圍與限制

- 這是固定 commit 的離線行為驗證，不評估其他 commit 是否已修正。
- 沒有使用真實 LLM 判斷回答品質；所有 bug 都由 deterministic fake 回應或程式控制流重現。
- 本報告即為本次紀錄；依需求未建立 GitHub Issue、PR、外部截圖或上報紀錄。
