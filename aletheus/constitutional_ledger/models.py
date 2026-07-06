from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


def _timestamp():
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class LedgerEntry:
    ledger_id: str
    decision_trace_id: str
    certification_id: str
    application: str
    relix_profile: str
    recommendation: str
    confidence: float
    principle_x_decision: str
    certified: bool = True
    application_version: str = ""
    evidence: list[dict[str, Any]] = field(default_factory=list)
    council_opinions: list[dict[str, Any]] = field(default_factory=list)
    consensus: dict[str, Any] = field(default_factory=dict)
    thorx_grade: dict[str, Any] = field(default_factory=dict)
    policies_applied: list[dict[str, Any]] = field(default_factory=list)
    enforcement_actions: list[dict[str, Any]] = field(default_factory=list)
    runtime_version: str = ""
    genesis_version: str = "19.4"
    constitution_version: str = "0.1.0"
    signature: str | None = None
    content_hash: str | None = None
    timestamp: str = field(default_factory=_timestamp)

    def to_dict(self):
        return {
            "ledger_id": self.ledger_id,
            "decision_trace_id": self.decision_trace_id,
            "certification_id": self.certification_id,
            "timestamp": self.timestamp,
            "application": self.application,
            "application_version": self.application_version,
            "relix_profile": self.relix_profile,
            "evidence": self.evidence,
            "council_opinions": self.council_opinions,
            "consensus": self.consensus,
            "thorx_grade": self.thorx_grade,
            "recommendation": self.recommendation,
            "confidence": self.confidence,
            "policies_applied": self.policies_applied,
            "enforcement_actions": self.enforcement_actions,
            "principle_x_decision": self.principle_x_decision,
            "runtime_version": self.runtime_version,
            "genesis_version": self.genesis_version,
            "constitution_version": self.constitution_version,
            "certified": self.certified,
            "signature": self.signature,
            "content_hash": self.content_hash,
        }


def new_ledger_id():
    return f"LEDGER-{uuid4().hex[:12].upper()}"


def new_decision_trace_id():
    return f"TRACE-{uuid4().hex[:12].upper()}"


def new_certification_id():
    return f"CERT-{uuid4().hex[:12].upper()}"
