from __future__ import annotations

from .registry import ConstitutionalLedgerRegistry


class ConstitutionalLedgerSearch:
    GENESIS = "19.4"
    VERSION = "0.1.0"

    def __init__(self, registry: ConstitutionalLedgerRegistry):
        self.registry = registry

    def search(self, query: str):
        query_lower = query.lower()

        results = []

        for entry in self.registry.list():
            text = " ".join(
                [
                    str(entry.get("ledger_id", "")),
                    str(entry.get("decision_trace_id", "")),
                    str(entry.get("certification_id", "")),
                    str(entry.get("application", "")),
                    str(entry.get("relix_profile", "")),
                    str(entry.get("recommendation", "")),
                    str(entry.get("principle_x_decision", "")),
                ]
            ).lower()

            if query_lower in text:
                results.append(entry)

        return results
