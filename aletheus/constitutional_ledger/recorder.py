from __future__ import annotations

from .certification import ledger_certification_service
from .models import LedgerEntry
from .registry import ConstitutionalLedgerRegistry


class ConstitutionalLedgerRecorder:
    GENESIS = "19.4"
    VERSION = "0.1.0"

    def __init__(self, registry: ConstitutionalLedgerRegistry):
        self.registry = registry

    def record(
        self,
        *,
        application: str,
        relix_profile: str,
        recommendation: str,
        confidence: float,
        principle_x_decision: str,
        decision_trace_id: str | None = None,
        certification_id: str | None = None,
        application_version: str = "",
        evidence: list[dict] | None = None,
        council_opinions: list[dict] | None = None,
        consensus: dict | None = None,
        thorx_grade: dict | None = None,
        policies_applied: list[dict] | None = None,
        enforcement_actions: list[dict] | None = None,
        runtime_version: str = "",
        constitution_version: str = "0.1.0",
    ):
        ids = ledger_certification_service.create_ids(
            decision_trace_id=decision_trace_id,
            certification_id=certification_id,
        )

        entry = LedgerEntry(
            ledger_id=ids["ledger_id"],
            decision_trace_id=ids["decision_trace_id"],
            certification_id=ids["certification_id"],
            application=application,
            application_version=application_version,
            relix_profile=relix_profile,
            evidence=evidence or [],
            council_opinions=council_opinions or [],
            consensus=consensus or {},
            thorx_grade=thorx_grade or {},
            recommendation=recommendation,
            confidence=confidence,
            policies_applied=policies_applied or [],
            enforcement_actions=enforcement_actions or [],
            principle_x_decision=principle_x_decision,
            runtime_version=runtime_version,
            constitution_version=constitution_version,
        )

        self.registry.append(entry)

        return entry.to_dict()
