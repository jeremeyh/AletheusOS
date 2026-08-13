from __future__ import annotations
import hashlib, json
from .model import LifecycleDecision

class LifecycleEvidenceBridge:
    """Produces canonical evidence material for RAF ingestion; it is not RAF authority."""
    @staticmethod
    def canonical_payload(decision: LifecycleDecision) -> bytes:
        raw = {
            "object_id": decision.object_id,
            "policy_id": decision.policy_id,
            "policy_version": decision.policy_version,
            "current_state": decision.current_state.value,
            "proposed_state": decision.proposed_state.value,
            "action": decision.action.value,
            "executable": decision.executable,
            "reason": decision.reason,
            "evaluated_at_iso": decision.evaluated_at_iso,
            "authority_ref": decision.authority_ref,
            "evidence": dict(decision.evidence),
        }
        return json.dumps(raw, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

    @classmethod
    def digest(cls, decision: LifecycleDecision) -> str:
        return "sha256:" + hashlib.sha256(cls.canonical_payload(decision)).hexdigest()


# PASS_3A5J_EV04_EVIDENCE_QUALITY
from dataclasses import dataclass as _pass3a5j_dataclass

@_pass3a5j_dataclass(frozen=True)
class EvidenceQualityCharacterization:
    """Bounded evidence-quality characterization."""
    confidence: float
    method: str = "explicit"
    rationale: str = ""

    def __post_init__(self):
        if not 0.0 <= float(self.confidence) <= 1.0:
            raise ValueError("confidence must be bounded to [0.0, 1.0]")

def characterize_evidence_quality(confidence: float, *, method: str = "explicit", rationale: str = "") -> EvidenceQualityCharacterization:
    return EvidenceQualityCharacterization(
        confidence=float(confidence),
        method=method,
        rationale=rationale,
    )
