"""
Public API for the AletheusOS Application Runtime.
"""

from .core import (
    ApplicationRuntime,
    application_runtime,
)
from .models import (
    ApplicationManifest,
    ApplicationRecord,
    ApplicationStatus,
)
from .proof_application import (
    ConstitutionalProofApplication,
)
from .registry import (
    APPLICATIONS,
    ApplicationNotFoundError,
    ConstitutionalApplicationRegistry,
    DuplicateApplicationError,
    get_application,
    has_application,
    list_applications,
    register_application,
)
from .runtime import (
    ConstitutionalApplicationRuntime,
    InvalidApplicationTransitionError,
)
from .validation import (
    ApplicationValidationError,
    ApplicationValidationIssue,
    validate_manifest,
)

__all__ = [
    "APPLICATIONS",
    "ApplicationManifest",
    "ApplicationNotFoundError",
    "ApplicationRecord",
    "ApplicationRuntime",
    "ApplicationStatus",
    "ApplicationValidationError",
    "ApplicationValidationIssue",
    "ConstitutionalApplicationRegistry",
    "ConstitutionalApplicationRuntime",
    "ConstitutionalProofApplication",
    "DuplicateApplicationError",
    "InvalidApplicationTransitionError",
    "application_runtime",
    "get_application",
    "has_application",
    "list_applications",
    "register_application",
    "validate_manifest",
]
