from __future__ import annotations

from typing import Any, ClassVar

from .models import MissionSpec


class Engine:
    """Registry and capability broker for bounded mission resources."""

    VERSION: ClassVar[str] = "33.5.0"

    def __init__(self) -> None:
        self._resources: dict[str, frozenset[str]] = {}

    def register(self, resource_id: str, capabilities: set[str]) -> None:
        if not resource_id.strip():
            raise ValueError("resource_id is required.")
        self._resources[resource_id] = frozenset(capabilities)

    def resolve(self, required: set[str]) -> tuple[str, ...]:
        return tuple(
            sorted(
                resource_id
                for resource_id, capabilities in self._resources.items()
                if required.issubset(capabilities)
            )
        )

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        self.register("resource:internal:demo", {"DISCOVERY", "DETAIL"})
        return {
            "missionId": mission.mission_id,
            "resolved": self.resolve({"DISCOVERY"}),
            "capabilityBroker": True,
        }
