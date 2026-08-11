from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from .common import RSFValidationError, utc_now_iso

class ReliabilityAssuranceState(str, Enum):
    UNKNOWN = "UNKNOWN"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    RECOVERING = "RECOVERING"
    FAULTED = "FAULTED"
    OFFLINE = "OFFLINE"

class ReliabilityDisposition(str, Enum):
    CONTINUE = "CONTINUE"
    DEGRADED_CONTINUE = "DEGRADED_CONTINUE"
    RECOVER = "RECOVER"
    FAIL_CLOSED = "FAIL_CLOSED"
    ABSTAIN = "ABSTAIN"

class FailureSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass(frozen=True)
class EvidenceRequirement:
    requirement_id: str
    description: str
    mandatory: bool = True

@dataclass(frozen=True)
class AuthorityBoundary:
    rsf_may_measure_reliability: bool = True
    rsf_may_issue_release_certificate: bool = False
    raf_may_consume_rsf_evidence: bool = True
    raf_may_rewrite_rsf_evidence: bool = False
    mammoth_may_issue_assurance_decision: bool = False

@dataclass(frozen=True)
class RSFAssuranceContract:
    schema_version: str
    standard: str
    component_id: str
    current_state: ReliabilityAssuranceState
    disposition: ReliabilityDisposition
    failure_domain: str
    evaluated_at_iso: str
    evidence_requirements: tuple[EvidenceRequirement, ...]
    authority_boundary: AuthorityBoundary

class RSFContractEngine:
    STANDARD = "ALETHEUSOS-RSF-CANONICAL-CONTRACT"

    @classmethod
    def evaluate_contract(
        cls,
        component_id: str,
        state: ReliabilityAssuranceState,
        *,
        failure_domain: str = "UNSPECIFIED",
    ) -> RSFAssuranceContract:
        if not component_id.strip():
            raise RSFValidationError("component_id is required")
        if state is ReliabilityAssuranceState.HEALTHY:
            disposition = ReliabilityDisposition.CONTINUE
        elif state is ReliabilityAssuranceState.DEGRADED:
            disposition = ReliabilityDisposition.DEGRADED_CONTINUE
        elif state is ReliabilityAssuranceState.RECOVERING:
            disposition = ReliabilityDisposition.RECOVER
        elif state in (ReliabilityAssuranceState.FAULTED, ReliabilityAssuranceState.OFFLINE):
            disposition = ReliabilityDisposition.FAIL_CLOSED
        else:
            disposition = ReliabilityDisposition.ABSTAIN

        requirements = (
            EvidenceRequirement("RSF-EV-001", "State conclusion must be traceable to observations."),
            EvidenceRequirement("RSF-EV-002", "Failure-domain conclusion must identify affected boundary."),
            EvidenceRequirement("RSF-EV-003", "Recovery claims require post-recovery verification."),
            EvidenceRequirement("RSF-EV-004", "Release certification authority remains external to RSF."),
        )
        return RSFAssuranceContract(
            schema_version="1.0.0",
            standard=cls.STANDARD,
            component_id=component_id,
            current_state=state,
            disposition=disposition,
            failure_domain=failure_domain,
            evaluated_at_iso=utc_now_iso(),
            evidence_requirements=requirements,
            authority_boundary=AuthorityBoundary(),
        )
