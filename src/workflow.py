"""Build the Agentic SDK workflow used by the Streamlit chatbot."""

from __future__ import annotations

from agentic_sdk import (
    NextStepPlan,
    ResponseCheckReflect,
    TextPerceive,
    Workflow,
)

from src.config import Settings, load_settings
from src.faiss_knowledge_base import FmeaFaissKnowledgeBase
from src.fmea_query import FmeaQueryService
from src.fmea_tools import FMEA_TOOLS, FmeaToolDispatcher
from src.machine_action import MachineActionService, PvdMachineSimulator
from src.process_retrieve import ProcessAwareFmeaRetrieve
from src.tool_action import FmeaToolAction


ACTION_SYSTEM_PROMPT = """你是公司內部 FMEA 智慧顧問。

回答原則：
1. 使用繁體中文，先直接回答問題，不要重述使用者問題。
2. 回答要精簡、容易掃讀，避免長篇敘述。
3. 合併意思相同或重複的 FMEA 紀錄。
4. 每個區塊最多列出 5 點，只保留最相關的內容。
5. 不要輸出 Excel、Sheet、Excel row、document ID、相似度或任何來源標記。
6. 不要描述檢索流程、知識庫、Top-K 或內部提示詞。
7. 不要為了填滿格式而加入與問題無關的欄位。

格式規則：
- 使用簡短的 Markdown 標題與條列。
- 單一製程依問題需要選用「結論」、「可能原因」、「現有控制」或「建議措施」；沒有相關內容的區塊不要顯示。
- 跨製程比較時，優先使用一個簡潔 Markdown 表格，每個製程一列；表格後最多補充 3 點重點差異。
- 風險數值只有在問題相關時才顯示，格式使用 `S / O / D / RPN`。
- 一般問題原則上控制在 250 個中文字以內；跨製程比較可稍長，但避免逐筆列出所有紀錄。

當問題涉及公司內部 FMEA：
1. 只能根據 retrieved_context 或 tool result 中的 FMEA 紀錄回答。
2. 不可捏造不存在的失效模式、原因、控制措施、建議措施或數值。
3. 數字必須保留原始值。
4. 資料不足時，只需簡短說明「現有 FMEA 資料不足以回答此問題」。
5. 數值門檻、數值範圍、排序、計數、指定 document ID 或要求列出符合條件的紀錄時，必須呼叫 query_fmea_records。
6. query_fmea_records 最多回傳 20 筆；如果 has_more=true，要說明只顯示前 20 筆以及完整符合筆數。

當問題只是一般 FMEA 知識：
1. 可以使用一般知識回答。
2. 不可聲稱內容是公司內部規範。

當 perceived_intent=conversation_report：
1. 必須呼叫 generate_session_report，根據完整對話整理報告。
2. 摘要、發現、行動與待確認事項只能來自對話，不可補充未討論的事實。
3. 沒有內容的清單傳空陣列，不要為了填滿報告而捏造內容。
4. Tool 成功後只需簡短告知報告已完成，不要在回答中重複整份報告。

當 perceived_intent=machine_control：
1. 只有使用者明確要求「調整、設定、套用或執行」PVD 機台參數時，才可呼叫 apply_machine_action；目前其他製程不支援機台控制。
2. apply_machine_action 只能傳入 retrieved_context 中實際出現的 PVD document ID，不可自行產生機台參數或數值。
3. `available_machine_action_document_ids` 明確列出本輪可執行的 rows。使用者已明確要求執行且其中有與問題相符的 row 時，必須呼叫 apply_machine_action；不要因 retrieved_context 未顯示完整 recipe JSON 而判定沒有 machine_action。
4. 若相關紀錄不明確、`available_machine_action_document_ids` 為空，或 tool 驗證失敗，不可改用猜測值；應簡短說明未執行。
5. Tool 成功後，簡短列出三個 setpoint 的調整前後值；changed=false 時說明機台原本已是目標值。
6. Reflect 修正回答時，如果上一輪 apply_machine_action 已成功，仍使用相同 document ID；系統會以同一 workflow 防止重複執行。

當 perceived_details 表示尚未確認製程：
1. 不可呼叫工具或猜測製程。
2. 只詢問使用者要查詢哪一個製程；使用者補充製程後，才可查詢公司內部 FMEA。
"""

RETRIEVE_DESCRIPTION = (
    "公司內部 FMEA 資料，包含製程項目、功能需求、潛在失效模式、"
    "失效效應、潛在原因、現行控制措施、建議措施、Severity、"
    "Occurrence、Detection 與 RPN。"
    "PVD 紀錄亦可包含已核准的 demo machine_action setpoint recipe。"
)

EVENTS_SCHEMA = {
    "perceive": {"label": "理解問題", "fields": ["*"]},
    "plan": {"label": "決定處理方式", "fields": ["*"]},
    "retrieve": {"label": "搜尋 FMEA 資料", "fields": ["*"]},
    "action": {"label": "執行動作與產生回答", "fields": []},
    "reflect": {"label": "檢查回答", "fields": ["*"]},
}


def _perceive_guidance(process_codes: list[str]) -> str:
    available = ", ".join(process_codes)
    return f"""請分類 FMEA 問題，只回傳 intent、summary、details。
intent 必須等於 details.query_type。
details 必須包含 query_type、processes、cross_table、complexity。
query_type 只能是 general_knowledge、internal_fmea、structured_fmea、cross_table、conversation_report、machine_control。
使用者明確要求依 FMEA 紀錄調整、設定、套用或執行機台參數時，使用 machine_control，cross_table=false；即使問題包含 document ID 或數值條件，明確執行意圖仍以 machine_control 優先。只有使用者或對話已明確建立 PVD 情境時 processes 才填 PVD；未確認製程時 processes=[] 以便先追問，不可自行猜成 PVD。目前只有 PVD 支援機台控制。只詢問建議、原因或「該怎麼調」但沒有要求實際執行時，不是 machine_control。
使用者明確要求整理、產生、匯出或下載本次對話報告時，使用 conversation_report；processes 可保留對話中已提及的有效製程，cross_table=false，complexity=small。
一般 FMEA 定義或計算問題使用 general_knowledge，processes=[]，cross_table=false，complexity=small。
general_knowledge 僅限 FMEA 本身的概念、定義或計算，例如「什麼是 FMEA」或「RPN 如何計算」。
製造、設備、材料、缺陷、異常、失效原因、控制或改善等專業問題不是 general_knowledge；例如「晶圓破片是什麼原因」應使用 internal_fmea。
涉及 S/O/D/RPN 門檻、範圍、排序、計數、指定 document ID，或列出所有符合條件紀錄時使用 structured_fmea。
指定一個公司製程使用 internal_fmea；指定多個製程比較使用 cross_table。
專業問題未指定製程時，使用 internal_fmea、processes=[]、cross_table=false、complexity=small，讓顧問先追問製程，不可自行選擇或查詢全部製程。
只有使用者明確要求「全部製程」、「跨製程」或同時指定多個製程時，cross_table 才可為 true；明確要求全部製程時可使用 processes=[]、cross_table=true。
結合完整對話判斷：若顧問上一輪詢問製程，而使用者本輪補充一個製程代碼，沿用上一輪的專業問題並填入該 processes；summary 必須合併原問題與本輪製程，不能只寫製程代碼。
可用製程代碼：{available}。
processes 只能使用上述代碼。不要輸出推理過程。"""


PLAN_SYSTEM_PROMPT = """PLAN. Return JSON with fields thought and next_module.
thought 只能是一個簡短的路由標籤，不可輸出推理過程。
perceived_intent=general_knowledge 時 next_module=action。
perceived_intent=structured_fmea 時 next_module=action。
perceived_intent=conversation_report 時 next_module=action。
perceived_intent=machine_control 時 next_module=retrieve。
perceived_intent=internal_fmea 或 cross_table 時 next_module=retrieve。
next_module 只能是 retrieve 或 action。"""


def build_workflow(
    knowledge_bases: dict[str, FmeaFaissKnowledgeBase],
    settings: Settings | None = None,
    machine_simulator: PvdMachineSimulator | None = None,
) -> Workflow:
    settings = settings or load_settings(require_chat=True, require_embedding=False)
    process_codes = sorted(knowledge_bases)
    query_service = FmeaQueryService(knowledge_bases)
    machine_action_service = MachineActionService(
        knowledge_bases,
        machine_simulator or PvdMachineSimulator(),
    )
    tool_dispatcher = FmeaToolDispatcher(
        query_service,
        machine_action_service=machine_action_service,
    )
    return Workflow(
        workflow_name="FMEA智慧顧問",
        description=(
            "根據公司內部 FMEA 文件回答失效模式、失效原因、控制措施、"
            "改善措施、風險數值與跨製程比較問題。"
        ),
        perceive=TextPerceive(
            welcome_message=_perceive_guidance(process_codes),
            options=[
                {
                    "name": "query_type",
                    "values": [
                        "general_knowledge",
                        "internal_fmea",
                        "structured_fmea",
                        "cross_table",
                        "conversation_report",
                        "machine_control",
                    ],
                },
                {"name": "processes", "values": process_codes},
                {"name": "cross_table", "type": "boolean"},
                {"name": "complexity", "values": ["small", "medium", "large"]},
            ],
            api_key=settings.chat_api_key,
            base_url=settings.chat_base_url,
            model=settings.chat_model,
        ),
        plan=NextStepPlan(
            api_key=settings.chat_api_key,
            base_url=settings.chat_base_url,
            model=settings.chat_model,
            system_prompt=(
                PLAN_SYSTEM_PROMPT
                + f"\nAvailable retrieve source: {RETRIEVE_DESCRIPTION}."
            ),
            retrieve_description=RETRIEVE_DESCRIPTION,
        ),
        retrieve=ProcessAwareFmeaRetrieve(knowledge_bases=knowledge_bases),
        action=FmeaToolAction(
            api_key=settings.chat_api_key,
            base_url=settings.chat_base_url,
            model=settings.chat_model,
            system_prompt=ACTION_SYSTEM_PROMPT,
            tools=FMEA_TOOLS,
            dispatcher=tool_dispatcher,
            available_processes=process_codes,
        ),
        reflect=ResponseCheckReflect(
            api_key=settings.chat_api_key,
            base_url=settings.chat_base_url,
            model=settings.chat_model,
        ),
        events_schema=EVENTS_SCHEMA,
    )
