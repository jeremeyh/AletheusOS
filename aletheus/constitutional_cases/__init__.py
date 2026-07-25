"""AletheusOS Constitutional Case Framework."""

from .catalog import (
    SECURITY_INCIDENT_CASE_CONTRACT,
    create_security_incident_case,
)
from .engine import (
    ConstitutionalCaseEngine,
    InvalidCaseTransitionError,
)
from .events import (
    CaseEventType,
    canonical_case_event_definitions,
    register_case_event_types,
)
from .models import (
    CaseContract,
    CaseCriticality,
    CaseSeverity,
    CaseStatus,
    ConstitutionalCase,
    new_case_id,
)
from .registry import (
    ConstitutionalCaseRegistry,
    DuplicateCaseError,
)
from .validation import (
    CaseValidationError,
    CaseValidationIssue,
    validate_case,
    validate_contract,
)

__all__ = [
    "SECURITY_INCIDENT_CASE_CONTRACT",
    "CaseContract",
    "CaseCriticality",
    "CaseEventType",
    "CaseSeverity",
    "CaseStatus",
    "CaseValidationError",
    "CaseValidationIssue",
    "ConstitutionalCase",
    "ConstitutionalCaseEngine",
    "ConstitutionalCaseRegistry",
    "DuplicateCaseError",
    "InvalidCaseTransitionError",
    "canonical_case_event_definitions",
    "create_security_incident_case",
    "new_case_id",
    "register_case_event_types",
    "validate_case",
    "validate_contract",
]
