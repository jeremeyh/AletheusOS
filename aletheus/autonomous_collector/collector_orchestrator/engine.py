from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from json import dumps
from typing import Any, ClassVar

from .models import CollectorPolicy, DecisionState, Mission, Opportunity


class Engine:
    """Coordinate bounded, evidence-first collector autonomy."""

    VERSION: ClassVar[str] = "32.16.0"
    CAPABILITY: ClassVar[str] = "Autonomous Collector Orchestrator"

    def evaluate(
        self,
        mission: Mission,
        opportunity: Opportunity,
        policy: CollectorPolicy | None = None,
    ) -> dict[str, Any]:
        active_policy = policy or CollectorPolicy()
        self._validate(mission, opportunity, active_policy)

        blocked_reasons = self._blocked_reasons(
            opportunity,
            active_policy,
        )
        blocked = bool(blocked_reasons)

        value_gap = opportunity.estimated_value - opportunity.asking_price
        value_ratio = max(value_gap, 0.0) / max(
            opportunity.estimated_value,
            1.0,
        )
        budget_fit = 1.0 if opportunity.asking_price <= mission.budget else 0.0
        score = min(
            1.0,
            opportunity.confidence * 0.55 + value_ratio * 0.25 + budget_fit * 0.20,
        )

        payload: dict[str, Any] = {
            "capability": self.CAPABILITY,
            "version": self.VERSION,
            "decision": (
                DecisionState.BLOCKED.value
                if blocked
                else DecisionState.AWAITING_APPROVAL.value
            ),
            "score": round(score, 6),
            "immutableDecisionContract": True,
            "requiresHumanApproval": True,
            "requires_approval": True,
            "executionAuthorized": False,
            "directives": {
                "executionAuthorized": False,
                "nextAction": ("HALT" if blocked else "REQUEST_HUMAN_APPROVAL"),
            },
            "constitutionalControls": {
                "humanAuthority": "REQUIRED",
                "silentPurchase": "PROHIBITED",
                "spartanReview": "REQUIRED_BEFORE_EXECUTION",
                "evidenceFirst": True,
                "immutableProtocol": True,
            },
            "humanAuthority": {
                "status": "PRESERVED",
                "consentRequired": True,
                "revocableBeforeExecution": True,
            },
            "blockedReasons": tuple(blocked_reasons),
            "mission": asdict(mission),
            "opportunity": asdict(opportunity),
            "policy": asdict(active_policy),
        }

        payload["digest"] = sha256(
            dumps(
                payload,
                sort_keys=True,
                separators=(",", ":"),
                default=str,
            ).encode("utf-8")
        ).hexdigest()
        return payload

    @staticmethod
    def _validate(
        mission: Mission,
        opportunity: Opportunity,
        policy: CollectorPolicy,
    ) -> None:
        if not mission.mission_id.strip():
            raise ValueError("mission.mission_id cannot be empty.")
        if not mission.objective.strip():
            raise ValueError("mission.objective cannot be empty.")
        if not opportunity.opportunity_id.strip():
            raise ValueError("opportunity.opportunity_id cannot be empty.")
        if not opportunity.asset_id.strip():
            raise ValueError("opportunity.asset_id cannot be empty.")
        if (
            min(
                mission.budget,
                opportunity.asking_price,
                opportunity.estimated_value,
                policy.max_transaction_value,
                policy.max_daily_commitment,
            )
            < 0
        ):
            raise ValueError("Monetary values cannot be negative.")
        if not 0.0 <= opportunity.confidence <= 1.0:
            raise ValueError("opportunity.confidence must be between 0 and 1.")

    @staticmethod
    def _blocked_reasons(
        opportunity: Opportunity,
        policy: CollectorPolicy,
    ) -> list[str]:
        reasons: list[str] = []
        if policy.allowed_markets and opportunity.market not in policy.allowed_markets:
            reasons.append("MARKET_NOT_ALLOWED")
        if opportunity.asset_id in policy.prohibited_assets:
            reasons.append("ASSET_PROHIBITED")
        if opportunity.asking_price > policy.max_transaction_value:
            reasons.append("TRANSACTION_LIMIT_EXCEEDED")
        if opportunity.asking_price > policy.max_daily_commitment:
            reasons.append("DAILY_COMMITMENT_LIMIT_EXCEEDED")
        return reasons
