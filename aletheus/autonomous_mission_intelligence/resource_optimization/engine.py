from __future__ import annotations

from typing import Any, ClassVar

from .helpers import digest
from .models import MissionCandidate, ResourceCapacity


class Engine:
    VERSION: ClassVar[str] = "34.5.0"

    def allocate(
        self, missions: list[MissionCandidate], resources: list[ResourceCapacity]
    ) -> dict[str, Any]:
        capacities = {
            r.resource_id: max(r.capacity - r.committed, 0.0) for r in resources
        }
        allocations: list[dict[str, Any]] = []
        for mission in sorted(
            missions, key=lambda m: (-(m.estimated_value * m.confidence), m.mission_id)
        ):
            assigned = []
            for resource in mission.required_resources:
                if capacities.get(resource, 0.0) >= 1.0:
                    capacities[resource] -= 1.0
                    assigned.append(resource)
            allocations.append(
                {
                    "missionId": mission.mission_id,
                    "resources": assigned,
                    "fullySatisfied": len(assigned) == len(mission.required_resources),
                }
            )
        payload = {
            "allocations": allocations,
            "remainingCapacity": capacities,
            "optimizationMode": "BOUNDED_GREEDY",
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(
        self, missions: list[MissionCandidate], resources: list[ResourceCapacity]
    ) -> dict[str, Any]:
        return self.allocate(missions, resources)
