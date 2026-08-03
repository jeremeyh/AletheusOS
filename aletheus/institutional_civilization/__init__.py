"""
Aletheus Institutional Civilization

Canonical public API for the Institutional Civilization framework.

This package exposes the complete compatibility surface expected by the
Genesis test suite while preserving the newer modular implementation.
"""

from .bootstrap import CivilizationBootstrap
from .canonical_catalog import canonical_institutions
from .civilization_catalog import canonical_civilizations
from .civilization_projection import CivilizationProjector
from .civilization_registry import (
    CivilizationRegistry,
    DuplicateCivilizationError,
)
from .engine import InstitutionalCivilizationEngine
from .models import (
    ConstitutionalLayer,
    ConstitutionalPillar,
    InstitutionCriticality,
    InstitutionRecord,
    InstitutionStatus,
)
from .projection import InstitutionProjector
from .registry import (
    DuplicateInstitutionError,
    InstitutionRegistry,
)
from .security_lifecycle import (
    SecurityCivilizationLifecycle,
)
from .security_projection import (
    CANONICAL_SECURITY_RELATIONSHIPS,
    SecurityCivilizationProjector,
)
from .validation import InstitutionValidationError
from .wiring import InstitutionWiring

__all__ = [
    "CANONICAL_SECURITY_RELATIONSHIPS",
    # Bootstrap
    "CivilizationBootstrap",
    # Civilization Framework
    "CivilizationProjector",
    "CivilizationRegistry",
    # Constitutional Model
    "ConstitutionalLayer",
    "ConstitutionalPillar",
    "DuplicateCivilizationError",
    "DuplicateInstitutionError",
    "InstitutionCriticality",
    # Institution Framework
    "InstitutionProjector",
    "InstitutionRecord",
    "InstitutionRegistry",
    "InstitutionStatus",
    "InstitutionValidationError",
    "InstitutionWiring",
    # Runtime
    "InstitutionalCivilizationEngine",
    # Security Civilization
    "SecurityCivilizationLifecycle",
    "SecurityCivilizationProjector",
    "canonical_civilizations",
    "canonical_institutions",
]
