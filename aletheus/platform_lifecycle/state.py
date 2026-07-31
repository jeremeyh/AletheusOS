from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from aletheus.platform_events import platform_events

from .models import StateTransition


class PlatformState(str, Enum):
    OFFLINE = "OFFLINE"
    ASSEMBLING = "ASSEMBLING"
    BOOTING = "BOOTING"
    ONLINE = "ONLINE"
    DEGRADED = "DEGRADED"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    SHUTDOWN = "SHUTDOWN"


class PlatformStateEngine:
    VALID_STATES = {state.value for state in PlatformState}

    def __init__(self):

        self.current = PlatformState.OFFLINE.value
        self.history: list[StateTransition] = []

    def status(self):

        return self.current

    def transition(self, state: str | PlatformState, reason: str = ""):

        if isinstance(state, PlatformState):
            state = state.value

        if state not in self.VALID_STATES:
            raise ValueError(f"Invalid platform state: {state}")

        previous = self.current

        self.current = state

        transition = StateTransition(
            previous=previous,
            current=state,
            reason=reason,
            timestamp=datetime.now(UTC).isoformat(),
        )

        self.history.append(transition)

        platform_events.publish(
            event_type=f"platform.{state.lower()}",
            source="platform_state",
            payload={
                "previous": previous,
                "current": state,
                "reason": reason,
            },
        )

        return transition.to_dict()

    def snapshot(self):

        return {
            "current": self.current,
            "history": [item.to_dict() for item in self.history],
        }


platform_state = PlatformStateEngine()
