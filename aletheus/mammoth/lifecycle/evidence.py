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
