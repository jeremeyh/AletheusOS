from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    OperationalEvent,
    immutable_contract,
)


class Engine:
    """SPARTAN Operational Defense capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.16.0"
    CAPABILITY: ClassVar[str] = "SPARTAN Operational Defense"

    def inspect(
        self,
        mission: MissionSnapshot,
        event: OperationalEvent,
    ) -> dict[str, Any]:
        suspicious_types = {
            "MISSION_HIJACK_ATTEMPT",
            "UNAUTHORIZED_POLICY_CHANGE",
            "EVIDENCE_TAMPERING",
            "EXECUTION_GRANT_FORGERY",
        }
        threat = event.event_type.upper() in suspicious_types
        action = "QUARANTINE_AND_REVOKE" if threat else "ALLOW_AND_OBSERVE"
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "threatDetected": threat,
                "defenseAction": action,
                "executionGrantRevoked": threat,
                "conclaveRequired": threat,
            },
            mission,
            event,
        )
