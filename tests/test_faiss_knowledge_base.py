from pathlib import Path

from src.faiss_knowledge_base import FmeaFaissKnowledgeBase
from src.my_splitter import FmeaDocument


def _knowledge_base(document: FmeaDocument) -> FmeaFaissKnowledgeBase:
    return FmeaFaissKnowledgeBase(
        process_code="PVD",
        documents=[document],
        index_dir=Path("unused-index-dir"),
        embedding_client=object(),
        embedding_model="test-embedding-model",
    )


def test_machine_action_does_not_change_embedding_content_hash() -> None:
    metadata = {
        "document_id": "PVD-0001",
        "process_code": "PVD",
        "potential_failure_mode": "鍍膜厚度不均",
    }
    content = "## PVD-0001\n\n- potential_failure_mode: 鍍膜厚度不均"
    without_action = FmeaDocument(
        document_id="PVD-0001",
        content=content,
        metadata=metadata,
    )
    with_action = FmeaDocument(
        document_id="PVD-0001",
        content=content,
        metadata={
            **metadata,
            "machine_action": (
                '{"machine_id":"PVD-DEMO-01","setpoints":'
                '{"button_1":10,"button_2":20,"button_3":30}}'
            ),
        },
    )

    assert _knowledge_base(without_action)._content_hash() == (
        _knowledge_base(with_action)._content_hash()
    )
