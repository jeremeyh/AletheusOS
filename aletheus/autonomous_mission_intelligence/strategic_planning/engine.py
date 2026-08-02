from __future__ import annotations

from dataclasses import asdict
from typing import Any, ClassVar

from .helpers import digest
from .models import StrategicObjective, StrategyPolicy


class Engine:
    VERSION: ClassVar[str] = "34.1.0"

    def plan(
        self,
        objective: StrategicObjective,
        policy: StrategyPolicy | None = None,
    ) -> dict[str, Any]:
        active_policy = policy or StrategyPolicy()
        milestones = [
            {"id": "discover", "purpose": "Gather admissible evidence"},
            {"id": "evaluate", "purpose": "Compare bounded strategies"},
            {"id": "authorize", "purpose": "Obtain human authorization"},
            {"id": "execute", "purpose": "Delegate to Genesis 33 runtime"},
            {"id": "learn", "purpose": "Record outcome feedback"},
        ]
        payload = {
            "objective": asdict(objective),
            "milestones": milestones,
            "dependencies": [
                ["discover", "evaluate"],
                ["evaluate", "authorize"],
                ["authorize", "execute"],
                ["execute", "learn"],
            ],
            "contingencies": [
                "PAUSE_ON_EVIDENCE_CONFLICT",
                "REPLAN_ON_RESOURCE_LOSS",
                "HALT_ON_SECURITY_VIOLATION",
            ],
            "humanAuthorizationRequired": active_policy.require_human_authorization,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, objective: StrategicObjective) -> dict[str, Any]:
        return self.plan(objective)
