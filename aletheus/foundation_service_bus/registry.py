from __future__ import annotations

from .models import (
    FoundationCapability,
    FoundationExecutionPlan,
    FoundationExecutionStage,
)


def appraisal_plan() -> FoundationExecutionPlan:
    return FoundationExecutionPlan(
        plan_id="plan.appraisal.collection.v1",
        capability_id="appraisal",
        name="APPRAISERᵡ™ Collection Appraisal Plan",
        engine_id="foundation.appraiserx",
        constitutional_articles=[
            "Principle X",
            "Evidence Before Conclusion",
            "Applications Request Capabilities",
            "Canonical Intelligence Objects",
            "Proof Before Promotion",
        ],
        expected_outputs=[
            "market_value",
            "private_sale_value",
            "replacement_value",
            "insurance_estimate",
            "collection_premium",
            "constitutional_value",
            "confidence",
            "reasoning",
        ],
        stages=[
            FoundationExecutionStage(
                1, "intent", "Resolve Intent", "foundation.intent"
            ),
            FoundationExecutionStage(
                2, "identity", "Resolve Identity", "identity_engine"
            ),
            FoundationExecutionStage(
                3, "capability", "Verify Capability", "capability_engine"
            ),
            FoundationExecutionStage(
                4, "observation", "Collect Observations", "foundation.observation"
            ),
            FoundationExecutionStage(
                5, "evidence", "Weigh Evidence", "foundation.evidence"
            ),
            FoundationExecutionStage(
                6, "marketplace", "Analyze Marketplace", "foundation.marketplace"
            ),
            FoundationExecutionStage(
                7, "portfolio", "Analyze Portfolio", "foundation.portfolio"
            ),
            FoundationExecutionStage(
                8, "forecast", "Forecast Value", "foundation.forecast"
            ),
            FoundationExecutionStage(
                9, "thorx", "THORᵡ Evaluation", "foundation.evaluation"
            ),
            FoundationExecutionStage(
                10, "council", "Council Review", "foundation.council"
            ),
            FoundationExecutionStage(
                11, "appraiserx", "Generate Appraisal", "foundation.appraiserx"
            ),
        ],
    )


class FoundationServiceRegistry:
    GENESIS = "32.1"
    VERSION = "1.0.0"

    def __init__(self) -> None:
        self._capabilities: dict[str, FoundationCapability] = {}
        self._aliases: dict[str, str] = {}
        self.bootstrap_defaults()

    def register(self, capability: FoundationCapability) -> None:
        self._capabilities[capability.capability_id] = capability
        for alias in capability.aliases:
            self._aliases[alias.lower()] = capability.capability_id

    def get(self, requested: str) -> FoundationCapability | None:
        key = requested.lower().strip()
        if key in self._capabilities:
            return self._capabilities[key]
        alias = self._aliases.get(key)
        return self._capabilities.get(alias) if alias else None

    def list(self) -> list[FoundationCapability]:
        return sorted(self._capabilities.values(), key=lambda item: item.capability_id)

    def bootstrap_defaults(self) -> None:
        self._capabilities.clear()
        self._aliases.clear()

        for capability in [
            FoundationCapability(
                capability_id="appraisal",
                name="APPRAISERᵡ™",
                engine_id="foundation.appraiserx",
                description="Constitutional valuation intelligence for collectible assets and portfolios.",
                aliases=[
                    "appraiser",
                    "appraiserx",
                    "valuation",
                    "collection appraisal",
                    "portfolio appraisal",
                ],
                constitutional_articles=[
                    "Evidence Before Conclusion",
                    "Canonical Intelligence Objects",
                ],
                execution_plan=appraisal_plan(),
            ),
            FoundationCapability(
                capability_id="evidence",
                name="Evidence Engine™",
                engine_id="foundation.evidence",
                description="Evidence quality, reliability, weighting, and trust evaluation.",
                aliases=["evidence", "proof", "trust", "verification"],
                constitutional_articles=["Evidence Before Conclusion"],
            ),
            FoundationCapability(
                capability_id="evaluation",
                name="THORᵡ™",
                engine_id="foundation.evaluation",
                description="Strategic desirability, risk, and acquisition quality evaluation.",
                aliases=["thor", "thorx", "evaluate", "score", "grade"],
                constitutional_articles=["Truth Before Intelligence", "Explainability"],
            ),
            FoundationCapability(
                capability_id="marketplace",
                name="Marketplace Intelligence™",
                engine_id="foundation.marketplace",
                description="Market value, comps, liquidity, and pricing intelligence.",
                aliases=["market", "pricing", "comps", "sales"],
                constitutional_articles=["Evidence Before Conclusion"],
            ),
            FoundationCapability(
                capability_id="council",
                name="Council™",
                engine_id="foundation.council",
                description="Consensus review and multi-engine deliberation.",
                aliases=["consensus", "review", "vote"],
                constitutional_articles=["Collective Intelligence"],
            ),
        ]:
            self.register(capability)

    def statistics(self) -> dict:
        return {
            "name": "Foundation Service Registry",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "capabilities": len(self._capabilities),
            "aliases": len(self._aliases),
            "capability_ids": sorted(self._capabilities.keys()),
        }


foundation_service_registry = FoundationServiceRegistry()
