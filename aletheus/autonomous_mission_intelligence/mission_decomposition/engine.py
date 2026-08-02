from __future__ import annotations

from typing import Any, ClassVar

from .helpers import digest
from .models import StrategicObjective


class Engine:
    VERSION: ClassVar[str] = "34.2.0"

    def decompose(
        self, objective: StrategicObjective, phases: tuple[str, ...] = ()
    ) -> dict[str, Any]:
        labels = phases or (
            "DISCOVERY",
            "VALIDATION",
            "DECISION",
            "EXECUTION",
            "FEEDBACK",
        )
        sub_missions = []
        for index, label in enumerate(labels):
            sub_missions.append(
                {
                    "missionId": f"{objective.objective_id}:{index + 1}:{label.lower()}",
                    "parentObjectiveId": objective.objective_id,
                    "purpose": label,
                    "dependsOn": (
                        [] if index == 0 else [sub_missions[index - 1]["missionId"]]
                    ),
                    "executionAuthorized": False,
                }
            )
        payload = {
            "objectiveId": objective.objective_id,
            "subMissions": sub_missions,
            "bounded": True,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, objective: StrategicObjective) -> dict[str, Any]:
        return self.decompose(objective)
