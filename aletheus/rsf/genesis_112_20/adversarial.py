from __future__ import annotations
from dataclasses import dataclass
from .contracts import ReliabilityAssuranceState
from .invariants import (
    ReliabilityInvariant, ReliabilityInvariantFailureDomainEngine,
    FailureDomainType
)
from .contracts import FailureSeverity
from .bridge import RAFEvidenceConsumerBoundary

@dataclass(frozen=True)
class AdversarialResult:
    vector: str
    passed: bool
    evidence: str

class WholeSystemReliabilityAdversarialValidation:
    @staticmethod
    def run() -> tuple[AdversarialResult, ...]:
        results = []

        inv = ReliabilityInvariant(
            "ADV-FAULT-001", "dependency must be available",
            FailureSeverity.CRITICAL, lambda facts: bool(facts.get("dependency_available"))
        )
        assessment = ReliabilityInvariantFailureDomainEngine.evaluate(
            "adv-domain", FailureDomainType.DEPENDENCY, (inv,), {"dependency_available": False}
        )
        results.append(AdversarialResult(
            "DEPENDENCY_LOSS_FAILS_CLOSED",
            assessment.state is ReliabilityAssuranceState.FAULTED and assessment.isolated,
            assessment.disposition.value
        ))

        try:
            RAFEvidenceConsumerBoundary.sign_release_from_rsf()
        except Exception:
            results.append(AdversarialResult("RSF_CANNOT_SIGN_RELEASE", True, "authority refusal observed"))
        else:
            results.append(AdversarialResult("RSF_CANNOT_SIGN_RELEASE", False, "authority leak"))

        results.append(AdversarialResult(
            "MALFORMED_EVIDENCE_REJECTED",
            not RAFEvidenceConsumerBoundary.validate_for_consumption(
                type("E", (), {"standard":"bad", "payload_digest":"bad"})()
            ),
            "invalid bridge envelope rejected"
        ))
        return tuple(results)
