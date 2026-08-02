from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from typing import Any, ClassVar

from .models import CollectorPolicy, DecisionState, Mission, Opportunity


class Engine:
    """Acquisition Mission Planner capability for bounded, evidence-first collector autonomy."""

    VERSION: ClassVar[str] = "32.3.0"
    CAPABILITY: ClassVar[str] = "Acquisition Mission Planner"

    def evaluate(
        self, mission: Mission, opportunity: Opportunity, policy: CollectorPolicy | None = None
    ) -> dict[str, Any]:
        active_policy = policy or CollectorPolicy()
        if not mission.mission_id.strip() or not mission.objective.strip():
            raise ValueError("Mission identity and objective are required.")
        if min(mission.budget, opportunity.asking_price, opportunity.estimated_value) < 0:
            raise ValueError("Monetary values cannot be negative.")
        if (
            active_policy.allowed_markets
            and opportunity.market not in active_policy.allowed_markets
        ):
            raise ValueError("Opportunity market is not permitted.")
        blocked = (
            opportunity.asking_price > active_policy.max_transaction_value
            or opportunity.asking_price > active_policy.max_daily_commitment
            or opportunity.asset_id in active_policy.prohibited_assets
        )
        value_gap = opportunity.estimated_value - opportunity.asking_price
        score = max(
            0.0,
            min(
                1.0,
                (0.55 * opportunity.confidence)
                + (0.25 if value_gap > 0 else 0.0)
                + (0.20 if opportunity.asking_price <= mission.budget else 0.0),
            ),
        )
        state = DecisionState.BLOCKED if blocked else DecisionState.AWAITING_APPROVAL
        payload = {
            "capability": self.CAPABILITY,
            "version": self.VERSION,
            "immutableDecisionContract": True,
            "decision": {
                "mission_id": mission.mission_id,
                "opportunity_id": opportunity.opportunity_id,
                "state": state.value,
                "score": round(score, 6),
                "requires_approval": True,
                "directives": {
                    "executionAuthorized": False,
                    "nextAction": "HALT" if blocked else "REQUEST_HUMAN_APPROVAL",
                },
            },
            "constitutionalControls": {
                "humanAuthority": "REQUIRED",
                "silentPurchase": "PROHIBITED",
                "spartanReview": "REQUIRED_BEFORE_EXECUTION",
            },
        }
        payload["evidenceDigest"] = sha256(
            repr((asdict(mission), asdict(opportunity), asdict(active_policy), payload)).encode()
        ).hexdigest()
        return payload
