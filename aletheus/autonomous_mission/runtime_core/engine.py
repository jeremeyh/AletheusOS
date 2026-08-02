from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from json import dumps
from typing import Any, ClassVar

from .models import MissionSpec, MissionStatus


class Engine:
    """Composition root for persistent, bounded autonomous missions."""

    VERSION: ClassVar[str] = "33.0.0"

    def activate(self, mission: MissionSpec) -> dict[str, Any]:
        if not mission.mission_id.strip() or not mission.objective.strip():
            raise ValueError("Mission identity and objective are required.")
        if mission.budget < 0:
            raise ValueError("Mission budget cannot be negative.")
        payload = {
            "mission": asdict(mission),
            "status": MissionStatus.ACTIVATED.value,
            "persistent": True,
            "humanAuthority": "PRESERVED",
            "executionAuthorized": False,
        }
        payload["digest"] = sha256(dumps(payload, sort_keys=True).encode()).hexdigest()
        return payload

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        return self.activate(mission)
