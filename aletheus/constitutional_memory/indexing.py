from __future__ import annotations

from uuid import uuid4

from .models import MemoryRecord


def new_memory_id():
    return f"MEM-{uuid4().hex[:12].upper()}"


class ConstitutionalMemoryIndexer:
    GENESIS = "19.5"
    VERSION = "0.1.0"

    def from_ledger_entry(
        self,
        entry: dict,
        *,
        tags: list[str] | None = None,
        keywords: list[str] | None = None,
        entities: list[str] | None = None,
        precedent_weight: str = "LOW",
    ):
        return MemoryRecord(
            memory_id=new_memory_id(),
            ledger_id=entry["ledger_id"],
            decision_trace_id=entry["decision_trace_id"],
            certification_id=entry["certification_id"],
            application=entry["application"],
            relix_profile=entry["relix_profile"],
            recommendation=entry["recommendation"],
            confidence=float(entry["confidence"]),
            precedent_weight=precedent_weight,
            tags=tags or [],
            keywords=keywords or [],
            entities=entities or [],
            metadata={
                "thorx_grade": entry.get("thorx_grade", {}),
                "consensus": entry.get("consensus", {}),
                "principle_x_decision": entry.get("principle_x_decision"),
            },
        )


constitutional_memory_indexer = ConstitutionalMemoryIndexer()
