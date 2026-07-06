from __future__ import annotations

from .models import new_certification_id, new_decision_trace_id, new_ledger_id


class LedgerCertificationService:
    GENESIS = "19.4"
    VERSION = "0.1.0"

    def create_ids(
        self,
        decision_trace_id: str | None = None,
        certification_id: str | None = None,
        ledger_id: str | None = None,
    ):
        return {
            "ledger_id": ledger_id or new_ledger_id(),
            "decision_trace_id": decision_trace_id or new_decision_trace_id(),
            "certification_id": certification_id or new_certification_id(),
        }


ledger_certification_service = LedgerCertificationService()
