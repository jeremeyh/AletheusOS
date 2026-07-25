from __future__ import annotations

from typing import Any

from services.runtime_state import RuntimeState


class FounderState:
    def __init__(self, state: RuntimeState) -> None:
        self.state = state
        self.state.state.setdefault("founder_decisions", [])
        self.state.save()

    def record_decision(self, decision: dict[str, Any]) -> None:
        decisions: list[dict[str, Any]] = self.state.get("founder_decisions", [])
        decisions.append(decision)
        self.state.set("founder_decisions", decisions)

    def recent_decisions(self, limit: int = 25) -> list[dict[str, Any]]:
        return self.state.get("founder_decisions", [])[-limit:]
