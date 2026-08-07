from dataclasses import dataclass, field

import pytest
from agentic_sdk import WorkflowState

from src.faiss_knowledge_base import RetrievalHit
from src.process_retrieve import ProcessAwareFmeaRetrieve


@dataclass
class FakeKnowledgeBase:
    process_code: str
    calls: list[tuple[str, int]] = field(default_factory=list)

    def search(self, query: str, top_k: int = 5) -> list[RetrievalHit]:
        self.calls.append((query, top_k))
        return [
            RetrievalHit(
                title=f"{self.process_code}-0001",
                content="FMEA row content",
                score=0.8,
                metadata={
                    "source_excel": f"{self.process_code}_FMEA.xlsx",
                    "source_sheet": self.process_code.lower(),
                    "source_excel_row": 3,
                },
            )
        ]


def _state(processes: list[str], query_type: str = "internal_fmea", complexity: str = "small") -> WorkflowState:
    state = WorkflowState(user_message="查詢失效原因")
    state.entities.update(
        {
            "perceived_summary": "查詢失效原因",
            "perceived_details": {
                "query_type": query_type,
                "processes": processes,
                "cross_table": len(processes) > 1,
                "complexity": complexity,
            },
        }
    )
    return state


@pytest.mark.parametrize(
    "processes, expected",
    [
        (["PVD"], {"PVD"}),
        (["PI"], {"PI"}),
        (["PVD", "PI"], {"PVD", "PI"}),
        ([], {"PVD", "PI", "ECD"}),
    ],
)
def test_retrieve_selects_only_expected_indexes(processes: list[str], expected: set[str]) -> None:
    knowledge_bases = {code: FakeKnowledgeBase(code) for code in ("PVD", "PI", "ECD")}
    output = ProcessAwareFmeaRetrieve(knowledge_bases)(_state(processes))

    called = {code for code, kb in knowledge_bases.items() if kb.calls}
    assert called == expected
    assert output["next_module"] == "action"
    assert output["payload"]["retrieval_hit_count"] == len(expected)
    assert set(output["payload"]["retrieval_selected_sources"]) == expected


def test_general_knowledge_skips_all_indexes() -> None:
    knowledge_bases = {code: FakeKnowledgeBase(code) for code in ("PVD", "PI")}
    output = ProcessAwareFmeaRetrieve(knowledge_bases)(
        _state([], query_type="general_knowledge")
    )

    assert not any(kb.calls for kb in knowledge_bases.values())
    assert output["next_module"] == "action"
    assert output["payload"]["retrieval_hit_count"] == 0


@pytest.mark.parametrize("complexity, top_k", [("small", 5), ("medium", 8), ("large", 12)])
def test_top_k_policy(complexity: str, top_k: int) -> None:
    knowledge_base = FakeKnowledgeBase("PVD")

    ProcessAwareFmeaRetrieve({"PVD": knowledge_base})(
        _state(["PVD"], complexity=complexity)
    )

    assert knowledge_base.calls == [("查詢失效原因", top_k)]
