from __future__ import annotations

from typing import Any, ClassVar

from ..common import (
    MissionSnapshot,
    immutable_contract,
)


class Engine:
    """Exception Resolution Engine capability for bounded autonomous operations."""

    VERSION: ClassVar[str] = "35.5.0"
    CAPABILITY: ClassVar[str] = "Exception Resolution Engine"

    def resolve(
        self,
        mission: MissionSnapshot,
        exception_type: str,
        retry_count: int,
    ) -> dict[str, Any]:
        if retry_count < 0:
            raise ValueError("retry_count cannot be negative")
        normalized = exception_type.strip().upper()
        if normalized in {"RATE_LIMIT", "TRANSIENT_NETWORK"} and retry_count < 3:
            action = "RETRY_WITH_BACKOFF"
        elif normalized in {"AUTHORIZATION", "CONSTITUTIONAL_VIOLATION"}:
            action = "HALT_AND_ESCALATE"
        else:
            action = "QUARANTINE_AND_DIAGNOSE"
        return immutable_contract(
            {
                "capability": self.CAPABILITY,
                "missionId": mission.mission_id,
                "exceptionType": normalized,
                "resolutionAction": action,
                "retryPermitted": action == "RETRY_WITH_BACKOFF",
            },
            mission,
            exception_type,
            retry_count,
        )
