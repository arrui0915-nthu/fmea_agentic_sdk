"""One persistent FAISS knowledge base per FMEA Markdown file."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import faiss
import numpy as np

from src.my_splitter import FmeaDocument, load_all_documents


MANIFEST_VERSION = 1


@dataclass(frozen=True)
class RetrievalHit:
    title: str
    content: str
    score: float
    metadata: dict[str, Any]


class KnowledgeBaseError(RuntimeError):
    """Base error for persistent knowledge-base operations."""


class KnowledgeBaseNotBuiltError(KnowledgeBaseError):
    """Raised when an index is absent or stale and automatic build is disabled."""


class FmeaFaissKnowledgeBase:
    def __init__(
        self,
        process_code: str,
        documents: list[FmeaDocument],
        index_dir: Path,
        embedding_client: Any,
        embedding_model: str,
    ) -> None:
        self.process_code = process_code.upper()
        self.documents = list(documents)
        self.index_root = Path(index_dir)
        self.storage_dir = self.index_root / self.process_code
        self.index_path = self.storage_dir / "index.faiss"
        self.metadata_path = self.storage_dir / "metadata.json"
        self.embedding_client = embedding_client
        self.embedding_model = embedding_model
        self.index: Any | None = None

    @property
    def vector_count(self) -> int:
        return int(self.index.ntotal) if self.index is not None else 0

    def _content_hash(self) -> str:
        payload = {
            "embedding_model": self.embedding_model,
            "documents": [
                {
                    "document_id": document.document_id,
                    "content": document.content,
                    # machine_action is execution metadata and is deliberately
                    # excluded from the embedding identity. Changing a trusted
                    # demo recipe must not require sending FMEA text back to the
                    # embedding endpoint or alter semantic similarity.
                    "metadata": {
                        key: value
                        for key, value in document.metadata.items()
                        if key != "machine_action"
                    },
                }
                for document in self.documents
            ],
        }
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _read_current_index(self) -> Any | None:
        if not self.index_path.is_file() or not self.metadata_path.is_file():
            return None
        try:
            manifest = json.loads(self.metadata_path.read_text(encoding="utf-8"))
            if manifest.get("manifest_version") != MANIFEST_VERSION:
                return None
            if manifest.get("process_code") != self.process_code:
                return None
            if manifest.get("embedding_model") != self.embedding_model:
                return None
            if manifest.get("content_hash") != self._content_hash():
                return None
            if manifest.get("vector_count") != len(self.documents):
                return None
            index = faiss.read_index(str(self.index_path))
            if int(index.ntotal) != len(self.documents):
                return None
            return index
        except (OSError, ValueError, TypeError, json.JSONDecodeError, RuntimeError):
            return None

    def load_existing(self) -> None:
        """Load a current index without ever calling the embedding endpoint."""

        index = self._read_current_index()
        if index is None:
            raise KnowledgeBaseNotBuiltError(
                f"{self.process_code} 索引不存在或 Markdown 已變更；"
                "請先執行 python build_indexes.py"
            )
        self.index = index

    def build_or_load(self) -> None:
        """Load a current index, otherwise embed all rows and rebuild it."""

        index = self._read_current_index()
        if index is not None:
            self.index = index
            return
        if not self.documents:
            raise KnowledgeBaseError(f"{self.process_code} 沒有可建立索引的 documents")

        response = self.embedding_client.embeddings.create(
            input=[document.content for document in self.documents],
            model=self.embedding_model,
        )
        response_data = sorted(
            response.data,
            key=lambda item: int(getattr(item, "index", 0)),
        )
        vectors = np.asarray(
            [item.embedding for item in response_data],
            dtype="float32",
        )
        if vectors.ndim != 2 or vectors.shape[0] != len(self.documents):
            raise KnowledgeBaseError(
                f"{self.process_code} embedding 數量或維度不正確"
            )
        if vectors.shape[1] == 0:
            raise KnowledgeBaseError(f"{self.process_code} embedding 維度不可為 0")

        faiss.normalize_L2(vectors)
        index = faiss.IndexFlatIP(int(vectors.shape[1]))
        index.add(vectors)

        self.storage_dir.mkdir(parents=True, exist_ok=True)
        temporary_index = self.storage_dir / "index.faiss.tmp"
        temporary_metadata = self.storage_dir / "metadata.json.tmp"
        faiss.write_index(index, str(temporary_index))
        manifest = {
            "manifest_version": MANIFEST_VERSION,
            "process_code": self.process_code,
            "embedding_model": self.embedding_model,
            "content_hash": self._content_hash(),
            "vector_count": len(self.documents),
            "dimension": int(vectors.shape[1]),
            "documents": [
                {
                    "document_id": document.document_id,
                    "content": document.content,
                    "metadata": document.metadata,
                }
                for document in self.documents
            ],
        }
        temporary_metadata.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary_index.replace(self.index_path)
        temporary_metadata.replace(self.metadata_path)
        self.index = index

    def search(self, query: str, top_k: int = 5) -> list[RetrievalHit]:
        if self.index is None:
            raise KnowledgeBaseError(f"{self.process_code} 索引尚未載入")
        query = query.strip()
        if not query or top_k <= 0 or not self.documents:
            return []

        response = self.embedding_client.embeddings.create(
            input=[query],
            model=self.embedding_model,
        )
        query_vector = np.asarray(
            [response.data[0].embedding],
            dtype="float32",
        )
        if query_vector.shape[1] != int(self.index.d):
            raise KnowledgeBaseError(
                f"{self.process_code} query embedding 維度與索引不一致"
            )
        faiss.normalize_L2(query_vector)
        count = min(int(top_k), len(self.documents), int(self.index.ntotal))
        scores, indices = self.index.search(query_vector, count)

        hits: list[RetrievalHit] = []
        for score, document_index in zip(scores[0], indices[0], strict=True):
            if document_index < 0:
                continue
            document = self.documents[int(document_index)]
            hits.append(
                RetrievalHit(
                    title=document.document_id,
                    content=document.content,
                    score=float(score),
                    metadata=dict(document.metadata),
                )
            )
        return sorted(hits, key=lambda hit: hit.score, reverse=True)


def _knowledge_bases(
    markdown_dir: Path,
    index_dir: Path,
    embedding_client: Any,
    embedding_model: str,
) -> dict[str, FmeaFaissKnowledgeBase]:
    return {
        process_code: FmeaFaissKnowledgeBase(
            process_code=process_code,
            documents=documents,
            index_dir=index_dir,
            embedding_client=embedding_client,
            embedding_model=embedding_model,
        )
        for process_code, documents in load_all_documents(markdown_dir).items()
    }


def build_all_knowledge_bases(
    markdown_dir: Path,
    index_dir: Path,
    embedding_client: Any,
    embedding_model: str,
) -> dict[str, FmeaFaissKnowledgeBase]:
    knowledge_bases = _knowledge_bases(
        markdown_dir,
        index_dir,
        embedding_client,
        embedding_model,
    )
    for knowledge_base in knowledge_bases.values():
        knowledge_base.build_or_load()
    return knowledge_bases


def load_existing_knowledge_bases(
    markdown_dir: Path,
    index_dir: Path,
    embedding_client: Any,
    embedding_model: str,
) -> dict[str, FmeaFaissKnowledgeBase]:
    """Load every current index without triggering any embedding requests."""

    knowledge_bases = _knowledge_bases(
        markdown_dir,
        index_dir,
        embedding_client,
        embedding_model,
    )
    for knowledge_base in knowledge_bases.values():
        knowledge_base.load_existing()
    return knowledge_bases
