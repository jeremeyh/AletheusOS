"""AletheusOS Constitutional Mission Framework."""

from .catalog import (
    SECURITY_CONTAINMENT_CONTRACT,
    create_security_containment_mission,
)
from .engine import (
    ConstitutionalMissionEngine,
    InvalidMissionTransitionError,
)
from .events import (
    MissionEventType,
    canonical_mission_event_definitions,
    register_mission_event_types,
)
from .models import (
    ConstitutionalMission,
    MissionContract,
    MissionCriticality,
    MissionStatus,
    new_mission_id,
)
from .registry import (
    ConstitutionalMissionRegistry,
    DuplicateMissionError,
)
from .validation import (
    MissionValidationError,
    MissionValidationIssue,
    validate_contract,
    validate_mission,
)

__all__ = [
    "ConstitutionalMission",
    "ConstitutionalMissionEngine",
    "ConstitutionalMissionRegistry",
    "DuplicateMissionError",
    "InvalidMissionTransitionError",
    "MissionContract",
    "MissionCriticality",
    "MissionEventType",
    "MissionStatus",
    "MissionValidationError",
    "MissionValidationIssue",
    "SECURITY_CONTAINMENT_CONTRACT",
    "canonical_mission_event_definitions",
    "create_security_containment_mission",
    "new_mission_id",
    "register_mission_event_types",
    "validate_contract",
    "validate_mission",
]
