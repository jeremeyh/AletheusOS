from __future__ import annotations

from datetime import UTC, datetime

from .models import BrainState


class BrainStateManager:
    GENESIS = "6.1"
    VERSION = "0.1.0"

    VALID_STATES = {
        "idle",
        "online",
        "thinking",
        "reasoning",
        "learning",
        "planning",
        "predicting",
        "observing",
        "communicating",
        "recovering",
        "synchronizing",
        "dreaming",
        "protected",
    }

    def __init__(self):
        self.current = BrainState("idle")
        self.history: list[BrainState] = [self.current]

    def set(self, name: str) -> BrainState:
        if name not in self.VALID_STATES:
            raise ValueError(f"Invalid brain state: {name}")

        self.current = BrainState(
            name=name,
            active=True,
            changed_at=datetime.now(UTC).isoformat(),
        )
        self.history.append(self.current)
        return self.current

    def get(self) -> BrainState:
        return self.current

    def health(self) -> dict:
        return {
            "name": "Brain State Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "current_state": self.current.name,
            "state_changes": len(self.history),
        }

    def statistics(self) -> dict:
        return {
            "name": "Brain State Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "current_state": self.current.name,
            "state_changes": len(self.history),
            "valid_states": sorted(self.VALID_STATES),
        }


brain_state_manager = BrainStateManager()
