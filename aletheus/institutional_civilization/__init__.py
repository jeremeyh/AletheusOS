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
    # Bootstrap
    "CivilizationBootstrap",

    # Civilization Framework
    "CivilizationProjector",
    "CivilizationRegistry",
    "DuplicateCivilizationError",
    "canonical_civilizations",

    # Institution Framework
    "InstitutionProjector",
    "InstitutionRegistry",
    "InstitutionRecord",
    "InstitutionStatus",
    "InstitutionCriticality",
    "DuplicateInstitutionError",
    "InstitutionValidationError",
    "canonical_institutions",

    # Constitutional Model
    "ConstitutionalLayer",
    "ConstitutionalPillar",

    # Security Civilization
    "SecurityCivilizationLifecycle",
    "SecurityCivilizationProjector",
    "CANONICAL_SECURITY_RELATIONSHIPS",

    # Runtime
    "InstitutionalCivilizationEngine",
    "InstitutionWiring",
]
