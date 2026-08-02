from __future__ import annotations

from typing import Any, ClassVar

from .models import MissionSpec, MissionStatus


class Engine:
    """Deterministic mission lifecycle state machine with guarded transitions."""

    VERSION: ClassVar[str] = "33.2.0"

    TRANSITIONS: ClassVar[dict[MissionStatus, frozenset[MissionStatus]]] = {
        MissionStatus.DRAFT: frozenset(
            {MissionStatus.VALIDATED, MissionStatus.CANCELLED}
        ),
        MissionStatus.VALIDATED: frozenset(
            {MissionStatus.ACTIVATED, MissionStatus.CANCELLED}
        ),
        MissionStatus.ACTIVATED: frozenset(
            {MissionStatus.SCHEDULED, MissionStatus.PAUSED}
        ),
        MissionStatus.SCHEDULED: frozenset(
            {MissionStatus.OBSERVING, MissionStatus.PAUSED}
        ),
        MissionStatus.OBSERVING: frozenset(
            {MissionStatus.EVALUATING, MissionStatus.PAUSED}
        ),
        MissionStatus.EVALUATING: frozenset(
            {
                MissionStatus.AWAITING_AUTHORIZATION,
                MissionStatus.SCHEDULED,
                MissionStatus.COMPLETED,
                MissionStatus.FAILED,
            }
        ),
        MissionStatus.AWAITING_AUTHORIZATION: frozenset(
            {
                MissionStatus.EXECUTING,
                MissionStatus.PAUSED,
                MissionStatus.CANCELLED,
            }
        ),
        MissionStatus.EXECUTING: frozenset(
            {
                MissionStatus.COMPLETED,
                MissionStatus.FAILED,
                MissionStatus.PAUSED,
            }
        ),
        MissionStatus.PAUSED: frozenset(
            {
                MissionStatus.ACTIVATED,
                MissionStatus.CANCELLED,
                MissionStatus.EXPIRED,
            }
        ),
        MissionStatus.FAILED: frozenset(
            {MissionStatus.SCHEDULED, MissionStatus.CANCELLED}
        ),
    }

    def transition(
        self,
        current: MissionStatus,
        requested: MissionStatus,
    ) -> dict[str, Any]:
        allowed = self.TRANSITIONS.get(current, frozenset())
        if requested not in allowed:
            raise ValueError(f"Illegal mission transition: {current} -> {requested}")
        return {
            "previous": current.value,
            "current": requested.value,
            "transitionAuthorized": True,
        }

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        result = self.transition(MissionStatus.DRAFT, MissionStatus.VALIDATED)
        result["missionId"] = mission.mission_id
        return result
