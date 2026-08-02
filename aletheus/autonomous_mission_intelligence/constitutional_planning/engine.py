from __future__ import annotations

from typing import Any, ClassVar

from .helpers import digest
from .models import StrategyPolicy


class Engine:
    VERSION: ClassVar[str] = "34.9.0"

    def validate(
        self, actions: list[str], policy: StrategyPolicy | None = None
    ) -> dict[str, Any]:
        active_policy = policy or StrategyPolicy()
        prohibited = sorted(
            action for action in actions if action in active_policy.prohibited_actions
        )
        unsupported = sorted(
            action
            for action in actions
            if action not in active_policy.allowed_actions and action not in prohibited
        )
        compliant = not prohibited and not unsupported
        payload = {
            "compliant": compliant,
            "prohibited": prohibited,
            "unsupported": unsupported,
            "principles": list(active_policy.constitutional_principles),
            "humanAuthority": "REQUIRED",
            "executionAuthorized": False,
        }
        payload["digest"] = digest(payload)
        return payload

    def evaluate(self, actions: list[str]) -> dict[str, Any]:
        return self.validate(actions)
