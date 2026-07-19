"""AletheusOS Constitutional Cognition Framework™."""

from .convergence import (
    ConstitutionalConvergenceEngine,
)
from .mesh import (
    CognitiveParticipant,
    DuplicateCognitiveParticipantError,
    MultiplicitousIntelligenceMesh,
)
from .models import (
    CognitiveSignal,
    CognitiveSignalType,
    ConstitutionalVirtue,
    ContributionStance,
    ConvergenceResult,
    ConvergenceState,
    EngineContribution,
    MeshExecutionReport,
    VirtueAssessment,
    VirtueContext,
    VirtueFinding,
    new_cognition_id,
)
from .participants import (
    FunctionalCognitiveParticipant,
)
from .virtues import (
    ConstitutionalVirtuesFramework,
)

__all__ = [
    "CognitiveParticipant",
    "CognitiveSignal",
    "CognitiveSignalType",
    "ConstitutionalConvergenceEngine",
    "ConstitutionalVirtue",
    "ConstitutionalVirtuesFramework",
    "ContributionStance",
    "ConvergenceResult",
    "ConvergenceState",
    "DuplicateCognitiveParticipantError",
    "EngineContribution",
    "FunctionalCognitiveParticipant",
    "MeshExecutionReport",
    "MultiplicitousIntelligenceMesh",
    "VirtueAssessment",
    "VirtueContext",
    "VirtueFinding",
    "new_cognition_id",
]
