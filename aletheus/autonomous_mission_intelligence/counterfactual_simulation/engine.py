from __future__ import annotations

from typing import Any, ClassVar

from .helpers import digest


class Engine:
    VERSION: ClassVar[str] = "34.10.0"

    def simulate(self, scenarios: list[dict[str, float]]) -> dict[str, Any]:
        evaluated = []
        for index, scenario in enumerate(scenarios):
            value = scenario.get("value", 0.0)
            probability = max(0.0, min(1.0, scenario.get("probability", 0.0)))
            cost = max(0.0, scenario.get("cost", 0.0))
            risk = max(0.0, min(1.0, scenario.get("risk", 0.0)))
            utility = value * probability - cost - abs(value) * risk
            evaluated.append({"scenario": index, "expectedUtility": round(utility, 6)})
        evaluated.sort(key=lambda item: (-item["expectedUtility"], item["scenario"]))
        payload = {
            "scenarios": evaluated,
            "preferredScenario": evaluated[0]["scenario"] if evaluated else None,
            "executionAuthorized": False,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, scenarios: list[dict[str, float]]) -> dict[str, Any]:
        return self.simulate(scenarios)
