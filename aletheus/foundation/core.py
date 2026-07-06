from __future__ import annotations

from .models import FoundationEngine
from .registry import FoundationEngineRegistry


class AletheusFoundation:
    GENESIS = "16.2"
    VERSION = "0.1.0"

    def __init__(self):
        self.registry = FoundationEngineRegistry()
        self._bootstrapped = False

    def bootstrap_defaults(self):
        if self._bootstrapped:
            return self.statistics()

        defaults = [
            FoundationEngine(
                engine_id="foundation.visual",
                name="Visual Intelligence Engine",
                category="intelligence",
                description="Visual recognition, inspection, and image understanding.",
                aliases=["Hawk A•Eye™"],
            ),
            FoundationEngine(
                engine_id="foundation.marketplace",
                name="Marketplace Intelligence Engine",
                category="intelligence",
                description="Pricing, sales, liquidity, and market analysis.",
                aliases=["Marketplace Intelligence™"],
            ),
            FoundationEngine(
                engine_id="foundation.forecast",
                name="Forecast Intelligence Engine",
                category="intelligence",
                description="Long-term forecasting, projections, and future-state analysis.",
                aliases=["SOAR™"],
            ),
            FoundationEngine(
                engine_id="foundation.monitoring",
                name="Monitoring Intelligence Engine",
                category="intelligence",
                description="Watchlists, alerts, and continuous monitoring.",
                aliases=["PERCH™"],
            ),
            FoundationEngine(
                engine_id="foundation.acquisition",
                name="Acquisition Intelligence Engine",
                category="intelligence",
                description="Acquisition targeting and execution support.",
                aliases=["TALON™"],
            ),
            FoundationEngine(
                engine_id="foundation.risk",
                name="Risk Intelligence Engine",
                category="intelligence",
                description="Defensive analysis, exposure assessment, and risk grading.",
                aliases=["DEF™"],
            ),
            FoundationEngine(
                engine_id="foundation.portfolio",
                name="Portfolio Intelligence Engine",
                category="intelligence",
                description="Portfolio organization, allocation, and asset management intelligence.",
                aliases=["ROOST™"],
            ),
            FoundationEngine(
                engine_id="foundation.opportunity",
                name="Opportunity Intelligence Engine",
                category="intelligence",
                description="Opportunity discovery and acquisition targeting.",
                aliases=["FALCON™"],
            ),
            FoundationEngine(
                engine_id="foundation.action",
                name="Action Intelligence Engine",
                category="intelligence",
                description="Buy, sell, hold, and execution recommendation intelligence.",
                aliases=["STRIKE™"],
            ),
            FoundationEngine(
                engine_id="foundation.evaluation",
                name="Evaluation Intelligence Engine",
                category="intelligence",
                description="Universal constitutional evaluation, grading, recommendation, and enforcement.",
                aliases=["THORᵡ™"],
            ),
        ]

        for engine in defaults:
            self.registry.register(engine)

        self._bootstrapped = True

        return self.statistics()

    def list_engines(self):
        return self.registry.list()

    def health(self):
        return {
            "name": "Aletheus Foundation",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "bootstrapped": self._bootstrapped,
            "registry": self.registry.health(),
        }

    def statistics(self):
        return {
            "name": "Aletheus Foundation",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "engines": self.registry.count(),
            "engine_ids": self.registry.statistics()["engine_ids"],
        }


aletheus_foundation = AletheusFoundation()
