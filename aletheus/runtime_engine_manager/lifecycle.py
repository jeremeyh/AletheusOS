from __future__ import annotations

from datetime import UTC, datetime

from .models import RuntimeEngineState


class RuntimeEngineLifecycle:
    GENESIS = "16.4"
    VERSION = "0.1.0"

    def __init__(self):
        self._states: dict[str, RuntimeEngineState] = {}

    def register(self, engine_id: str, metadata: dict | None = None):
        state = RuntimeEngineState(
            engine_id=engine_id,
            status="registered",
            enabled=True,
            last_action="register",
            metadata=metadata or {},
        )

        self._states[engine_id] = state
        return state.to_dict()

    def start(self, engine_id: str):
        state = self._states[engine_id]
        state.status = "online"
        state.enabled = True
        state.last_action = "start"
        state.updated_at = datetime.now(UTC).isoformat()
        return state.to_dict()

    def stop(self, engine_id: str):
        state = self._states[engine_id]
        state.status = "offline"
        state.last_action = "stop"
        state.updated_at = datetime.now(UTC).isoformat()
        return state.to_dict()

    def enable(self, engine_id: str):
        state = self._states[engine_id]
        state.enabled = True
        state.last_action = "enable"
        state.updated_at = datetime.now(UTC).isoformat()
        return state.to_dict()

    def disable(self, engine_id: str):
        state = self._states[engine_id]
        state.enabled = False
        state.last_action = "disable"
        state.updated_at = datetime.now(UTC).isoformat()
        return state.to_dict()

    def state(self, engine_id: str):
        return self._states.get(engine_id)

    def list(self):
        return [
            state.to_dict()
            for state in self._states.values()
        ]

    def count(self):
        return len(self._states)
