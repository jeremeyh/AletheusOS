from __future__ import annotations

from collections import defaultdict, deque
from typing import Any, ClassVar

from .helpers import digest
from .models import MissionCandidate


class Engine:
    VERSION: ClassVar[str] = "34.8.0"

    def compile(self, missions: list[MissionCandidate]) -> dict[str, Any]:
        ids = {m.mission_id for m in missions}
        incoming = {m.mission_id: 0 for m in missions}
        outgoing: dict[str, list[str]] = defaultdict(list)
        missing: list[tuple[str, str]] = []
        for mission in missions:
            for dependency in mission.dependencies:
                if dependency not in ids:
                    missing.append((mission.mission_id, dependency))
                    continue
                outgoing[dependency].append(mission.mission_id)
                incoming[mission.mission_id] += 1
        queue = deque(sorted(node for node, degree in incoming.items() if degree == 0))
        order: list[str] = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for child in sorted(outgoing[node]):
                incoming[child] -= 1
                if incoming[child] == 0:
                    queue.append(child)
        cyclic = sorted(node for node, degree in incoming.items() if degree > 0)
        payload = {
            "executionOrder": order,
            "cyclicNodes": cyclic,
            "missingDependencies": missing,
            "valid": not cyclic and not missing,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, missions: list[MissionCandidate]) -> dict[str, Any]:
        return self.compile(missions)
