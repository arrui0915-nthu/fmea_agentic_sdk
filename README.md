# FMEA RAG Chatbot

這是一個以 Agentic SDK、Azure OpenAI-compatible API、FAISS 與 Streamlit 組成的簡潔 FMEA 問答程式。它直接讀取既有的 `data/markdown/*.md`，不會重新處理 Excel 或改寫 Markdown。

設計原則：

- 一個 Markdown 對應一個獨立 FAISS index。
- 一個 `FMEA_ROW_START` / `FMEA_ROW_END` 區塊對應一個向量 document。
- Top-K 表示每個被選中製程中最相似的 K 個 FMEA rows。
- Agentic SDK Perceive 判斷問題類型與製程，Retrieve 再選擇對應索引。

## Conda 環境

建議不要安裝到 `base`：

```powershell
conda create -n fmea-rag python=3.12 -y
conda activate fmea-rag
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Markdown

將已轉換完成的檔案放在：

```text
data/markdown/
```

例如 `PVD_FMEA.md` 會建立 `data/indexes/PVD/`。每個 row 必須使用：

```markdown
<!-- FMEA_ROW_START id=PVD-0001 -->
...
<!-- FMEA_ROW_END -->
```

## Azure 環境變數

複製 `.env.example` 為 `.env`，填入：

```dotenv
AZURE_CHAT_API_KEY=
AZURE_CHAT_BASE_URL=
AZURE_CHAT_MODEL=

AZURE_EMBEDDING_API_KEY=
AZURE_EMBEDDING_BASE_URL=
AZURE_EMBEDDING_MODEL=

FMEA_MARKDOWN_DIR=./data/markdown
FMEA_INDEX_DIR=./data/indexes
```

`*_BASE_URL` 必須是能直接交給 OpenAI Python client 的相容 base URL；不要再附加 `/chat/completions` 或 `/embeddings`。模型值請填 Azure deployment/model 名稱。

## 建立索引

```powershell
python build_indexes.py
```

文件內容與 embedding model 沒有變更時會直接載入現有索引；Markdown 改變時只重建對應的過期索引。

## 啟動 Chatbot

```powershell
streamlit run app.py
```

Streamlit 啟動時只載入索引，不會自動建立或呼叫大量 embedding API。若索引不存在，請先執行 `python build_indexes.py`。

## 從聊天建立 FMEA Preview

「從聊天建立 FMEA」分頁可貼上聊天內容，或上傳 UTF-8 `.txt`／`.md`，再選擇要比對的製程與相似度門檻。系統會排除與既有資料過度相似的 rows，並提供其餘 rows 的 `.xlsx` 預覽檔。此流程只讀取已載入的 FAISS indexes，不會修改 Excel、Markdown 或索引。

## 索引選擇

- 指定一個製程：只搜尋該製程，每個 index 取自己的 Top-K。
- 指定多個製程：分別搜尋各 index，再合併結果。
- 未指定製程的內部 FMEA 問題：搜尋全部 index，各自取 Top-K。
- 一般 FMEA 知識：跳過 Retrieve，直接由 Action 回答。

## 測試

```powershell
pytest
```
