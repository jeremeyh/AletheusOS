from __future__ import annotations

from typing import Any, ClassVar

from .models import MissionSpec


class Engine:
    """Composition root coordinating the Genesis 33 mission runtime."""

    VERSION: ClassVar[str] = "33.18.0"

    COMPONENTS: ClassVar[tuple[str, ...]] = (
        "MISSION_SPECIFICATION",
        "LIFECYCLE_STATE_MACHINE",
        "DURABLE_SCHEDULER",
        "MISSION_RESOURCE_PROTOCOL",
        "RESOURCE_REGISTRY",
        "ADAPTIVE_POLLING",
        "EXECUTION_LEASES",
        "OBSERVATION_NORMALIZATION",
        "TEMPORAL_ENTITY_GRAPH",
        "RELISTING_INTELLIGENCE",
        "MISSION_MEMORY",
        "EVIDENCE_CHRONICLE",
        "DECISION_PACKAGE",
        "PRE_EXECUTION_GUARD",
        "AUTHORIZATION_GRANTS",
        "SPARTAN_SECURITY",
        "OUTCOME_FEEDBACK",
    )

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        if not mission.mission_id.strip():
            raise ValueError("mission_id is required.")
        return {
            "missionId": mission.mission_id,
            "status": "AWAITING_HUMAN_AUTHORIZATION",
            "components": self.COMPONENTS,
            "persistentMission": True,
            "immutableDecisionContract": True,
            "humanAuthority": "PRESERVED",
            "silentConsequentialExecution": "PROHIBITED",
            "spartanSecurity": "REQUIRED",
            "executionAuthorized": False,
        }
