from __future__ import annotations

from typing import Any, ClassVar

from .models import ExperienceAction, ExperienceSurface, HydrationSource, SurfaceKind


class Engine:
    SURFACE: ClassVar[ExperienceSurface] = ExperienceSurface(
        "war_room",
        "War Room™",
        "High-consequence acquisition decision workspace for purchases, offers, and trades before marketplace commitment.",
        SurfaceKind.ROOM,
        (
            HydrationSource("THORᵡ"),
            HydrationSource("Council"),
            HydrationSource("A•3ye"),
            HydrationSource("Evidence Engine"),
            HydrationSource("Predictive Engine"),
            HydrationSource("Temporal Graph"),
            HydrationSource("Marketplace Intelligence"),
            HydrationSource("Portfolio Engine"),
        ),
        ("A•3ye", "THORᵡ", "Council", "Evidence", "Predictive", "Temporal", "Reason"),
        (
            ExperienceAction(
                "simulate_purchase", "Simulate Purchase", "SIMULATE_PURCHASE"
            ),
            ExperienceAction("simulate_offer", "Simulate Offer", "SIMULATE_OFFER"),
            ExperienceAction("simulate_trade", "Simulate Trade", "SIMULATE_TRADE"),
            ExperienceAction("convene_council", "Convene Council", "CONVENE_COUNCIL"),
            ExperienceAction(
                "commit_marketplace",
                "Commit to Marketplace",
                "COMMIT_MARKETPLACE",
                True,
                "marketplace",
            ),
            ExperienceAction("pass", "Pass", "PASS_OPPORTUNITY", True),
        ),
        metadata={
            "decisionTypes": ("PURCHASE", "OFFER", "TRADE"),
            "marketplaceExecutionBoundary": True,
            "regions": (
                "evidence",
                "comparables",
                "seller_buyer_intelligence",
                "opportunity_cost",
                "alternative_assets",
                "risk",
                "future_projection",
                "council_deliberation",
                "thorx_determination",
                "a3ye_summary",
            ),
        },
    )

    def surface(self):
        return self.SURFACE

    def analyze(self, decision_type: str, amount: float) -> dict[str, Any]:
        normalized = decision_type.upper()
        if normalized not in {"PURCHASE", "OFFER", "TRADE"}:
            raise ValueError("Unsupported War Room decision type")
        return {
            "decisionType": normalized,
            "amount": amount,
            "status": "ANALYSIS_REQUIRED",
            "requiredStages": (
                "EVIDENCE",
                "COMPARABLES",
                "RISK",
                "COUNCIL",
                "THORX",
                "A3YE_SUMMARY",
            ),
            "marketplaceCommitAllowed": False,
        }
