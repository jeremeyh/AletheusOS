from __future__ import annotations

from typing import Any, ClassVar

from .models import AuthorizationGrant, MissionSpec


class Engine:
    """Final constitutional and policy guard immediately before execution."""

    VERSION: ClassVar[str] = "33.14.0"

    def authorize(
        self,
        mission: MissionSpec,
        amount: float,
        grant: AuthorizationGrant | None,
        now: int,
    ) -> dict[str, Any]:
        reasons: list[str] = []
        if amount < 0:
            reasons.append("NEGATIVE_AMOUNT")
        if mission.budget and amount > mission.budget:
            reasons.append("MISSION_BUDGET_EXCEEDED")
        if grant is None:
            reasons.append("AUTHORIZATION_GRANT_REQUIRED")
        elif not grant.mfa_verified:
            reasons.append("MFA_NOT_VERIFIED")
        elif not grant.issued_at <= now <= grant.expires_at:
            reasons.append("GRANT_EXPIRED_OR_NOT_ACTIVE")
        elif "EXECUTE" not in grant.scopes:
            reasons.append("EXECUTION_SCOPE_MISSING")
        return {
            "allowed": not reasons,
            "reasons": tuple(reasons),
            "preExecutionGuard": "PASSED" if not reasons else "BLOCKED",
        }

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        return self.authorize(mission, 0.0, None, 0)
