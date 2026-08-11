from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Mapping, Any
from .common import RSFInvariantError
from .contracts import FailureSeverity, ReliabilityAssuranceState, ReliabilityDisposition

class FailureDomainType(str, Enum):
    COMPONENT = "COMPONENT"
    SERVICE = "SERVICE"
    PROVIDER = "PROVIDER"
    DEPENDENCY = "DEPENDENCY"
    HOST = "HOST"
    CLUSTER = "CLUSTER"
    STORAGE = "STORAGE"
    NETWORK = "NETWORK"
    UNKNOWN = "UNKNOWN"

@dataclass(frozen=True)
class ReliabilityInvariant:
    invariant_id: str
    description: str
    severity: FailureSeverity
    evaluator: Callable[[Mapping[str, Any]], bool]
    required_for_continue: bool = True

@dataclass(frozen=True)
class InvariantObservation:
    invariant_id: str
    passed: bool
    severity: FailureSeverity
    evidence: str

@dataclass(frozen=True)
class FailureDomainAssessment:
    domain_id: str
    domain_type: FailureDomainType
    state: ReliabilityAssuranceState
    disposition: ReliabilityDisposition
    observations: tuple[InvariantObservation, ...]
    isolated: bool

class ReliabilityInvariantFailureDomainEngine:
    @staticmethod
    def evaluate(
        domain_id: str,
        domain_type: FailureDomainType,
        invariants: tuple[ReliabilityInvariant, ...],
        facts: Mapping[str, Any],
    ) -> FailureDomainAssessment:
        if not domain_id.strip():
            raise RSFInvariantError("failure domain id is required")
        observations = []
        critical_failure = False
        any_failure = False
        for invariant in invariants:
            try:
                passed = bool(invariant.evaluator(facts))
                evidence = "evaluation returned true" if passed else "evaluation returned false"
            except Exception as exc:
                passed = False
                evidence = f"evaluation raised {type(exc).__name__}: {exc}"
            observations.append(InvariantObservation(invariant.invariant_id, passed, invariant.severity, evidence))
            if not passed:
                any_failure = True
                if invariant.required_for_continue or invariant.severity is FailureSeverity.CRITICAL:
                    critical_failure = True

        if critical_failure:
            state = ReliabilityAssuranceState.FAULTED
            disposition = ReliabilityDisposition.FAIL_CLOSED
            isolated = True
        elif any_failure:
            state = ReliabilityAssuranceState.DEGRADED
            disposition = ReliabilityDisposition.DEGRADED_CONTINUE
            isolated = False
        else:
            state = ReliabilityAssuranceState.HEALTHY
            disposition = ReliabilityDisposition.CONTINUE
            isolated = False

        return FailureDomainAssessment(domain_id, domain_type, state, disposition, tuple(observations), isolated)

    @staticmethod
    def enforce(assessment: FailureDomainAssessment) -> None:
        if assessment.disposition is ReliabilityDisposition.FAIL_CLOSED:
            raise RSFInvariantError(
                f"reliability fail-closed: domain={assessment.domain_id} type={assessment.domain_type.value}"
            )
