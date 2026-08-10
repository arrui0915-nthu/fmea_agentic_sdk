"""Process-aware custom Retrieve module for Agentic SDK."""

from __future__ import annotations

from agentic_sdk import ContextEntry, ContextEntryType, ModuleOutput, WorkflowState

from src.faiss_knowledge_base import FmeaFaissKnowledgeBase, RetrievalHit


TOP_K_POLICY = {
    "small": 5,
    "medium": 8,
    "large": 12,
}


class ProcessAwareFmeaRetrieve:
    name = "retrieve"

    def __init__(
        self,
        knowledge_bases: dict[str, FmeaFaissKnowledgeBase],
    ) -> None:
        self.knowledge_bases = {
            process_code.upper(): knowledge_base
            for process_code, knowledge_base in knowledge_bases.items()
        }

    def __call__(self, state: WorkflowState) -> ModuleOutput:
        details = state.lookup("perceived_details") or {}
        if not isinstance(details, dict):
            details = {}
        query_type = str(details.get("query_type") or "internal_fmea")
        requested_processes = details.get("processes") or []
        if not isinstance(requested_processes, list):
            requested_processes = []
        cross_table = bool(details.get("cross_table"))
        complexity = str(details.get("complexity") or "small").lower()
        top_k = TOP_K_POLICY.get(complexity, TOP_K_POLICY["small"])

        if query_type == "general_knowledge":
            return ModuleOutput(
                next_module="action",
                payload={
                    "retrieved_snippet": "",
                    "latest_retrieved_content": "",
                    "retrieval_processes": [],
                    "retrieval_top_k": top_k,
                    "retrieval_hit_count": 0,
                    "retrieval_selected_sources": [],
                },
                context_updates=[],
            )

        if not requested_processes and not cross_table:
            return ModuleOutput(
                next_module="action",
                payload={
                    "needs_process_clarification": True,
                    "_trace_status": "skipped",
                    "_trace_reason": "等待指定製程",
                    "available_processes": sorted(self.knowledge_bases),
                    "retrieved_snippet": "",
                    "latest_retrieved_content": "",
                    "retrieval_processes": [],
                    "retrieval_top_k": top_k,
                    "retrieval_hit_count": 0,
                    "retrieval_selected_sources": [],
                },
                context_updates=[],
            )

        selected_processes = self._select_processes(requested_processes)
        query = str(
            state.lookup("perceived_summary") or state.latest_user_message()
        ).strip()
        hits: list[tuple[str, RetrievalHit]] = []
        for process_code in selected_processes:
            process_hits = self.knowledge_bases[process_code].search(query, top_k=top_k)
            hits.extend((process_code, hit) for hit in process_hits)

        snippet = _format_hits(hits)
        return ModuleOutput(
            next_module="action",
            payload={
                "retrieved_snippet": snippet,
                "latest_retrieved_content": snippet,
                "retrieval_processes": selected_processes,
                "retrieval_top_k": top_k,
                "retrieval_hit_count": len(hits),
                "retrieval_selected_sources": selected_processes,
            },
            context_updates=[
                ContextEntry(
                    type=ContextEntryType.RETRIEVED,
                    content=snippet,
                    metadata={
                        "processes": selected_processes,
                        "top_k": top_k,
                        "hit_count": len(hits),
                        "cross_table": cross_table,
                    },
                )
            ],
        )

    def _select_processes(self, requested_processes: list[object]) -> list[str]:
        if not requested_processes:
            return sorted(self.knowledge_bases)
        selected: list[str] = []
        for process in requested_processes:
            process_code = str(process).strip().upper()
            if process_code in self.knowledge_bases and process_code not in selected:
                selected.append(process_code)
        return selected


def _format_hits(hits: list[tuple[str, RetrievalHit]]) -> str:
    lines = ["Knowledge hits:"]
    if not hits:
        lines.extend(("", "No matching FMEA rows were found."))
        return "\n".join(lines)

    for position, (process_code, hit) in enumerate(hits, start=1):
        metadata = hit.metadata
        lines.extend(
            (
                "",
                f"{position}. [{process_code} / {hit.title}]",
                f"Source: {metadata.get('source_excel', '')}",
                f"Sheet: {metadata.get('source_sheet', '')}",
                f"Excel row: {metadata.get('source_excel_row', '')}",
                f"Score: {hit.score:.4f}",
                "",
                "Content:",
                hit.content,
            )
        )
    return "\n".join(lines)
