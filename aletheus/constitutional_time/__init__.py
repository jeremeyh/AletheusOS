"""AletheusOS TIME™ public interface."""

from .catalog import security_containment_phase_graph
from .engine import (
    InvalidPhaseTransitionError,
    TetraInstitutionalMissionEngine,
)
from .events import (
    TimeEventType,
    canonical_time_event_definitions,
    register_time_event_types,
)
from .graph import (
    DuplicatePhaseError,
    MissionPhaseGraph,
    PhaseCycleError,
    PhaseDependencyError,
)
from .models import (
    MissionPhaseContract,
    MissionPhaseState,
    MissionTemporalState,
    PhaseStatus,
    new_phase_id,
)

__all__ = [
    "DuplicatePhaseError",
    "InvalidPhaseTransitionError",
    "MissionPhaseContract",
    "MissionPhaseGraph",
    "MissionPhaseState",
    "MissionTemporalState",
    "PhaseCycleError",
    "PhaseDependencyError",
    "PhaseStatus",
    "TetraInstitutionalMissionEngine",
    "TimeEventType",
    "canonical_time_event_definitions",
    "new_phase_id",
    "register_time_event_types",
    "security_containment_phase_graph",
]
