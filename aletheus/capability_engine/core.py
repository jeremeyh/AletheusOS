from __future__ import annotations

from .decisions import decision_engine
from .grants import grant_manager
from .models import Capability
from .profiles import foundation_profiles
from .registry import CapabilityRegistry
from .resolver import capability_resolver


class CapabilityEngine:

    GENESIS = "21.6"
    VERSION = "1.0.0"

    def __init__(self):
        self.registry = CapabilityRegistry()
        self.profiles = foundation_profiles
        self.grants = grant_manager
        self.resolver = capability_resolver
        self.decisions = decision_engine

        self._bootstrap()

    def _bootstrap(self):
        """
        Register canonical Foundation capabilities.
        """

        self.registry.register_capability(
            Capability(
                capability_id="foundation.visual",
                name="Visual Intelligence",
                namespace="foundation",
                category="intelligence",
                description="Foundation visual intelligence engine.",
            )
        )

        self.registry.register_capability(
            Capability(
                capability_id="foundation.marketplace",
                name="Marketplace Intelligence",
                namespace="foundation",
                category="intelligence",
                description="Marketplace valuation engine.",
            )
        )

        self.registry.register_capability(
            Capability(
                capability_id="foundation.forecast",
                name="Forecast Intelligence",
                namespace="foundation",
                category="intelligence",
                description="Forecast and prediction engine.",
            )
        )

    def evaluate(
        self,
        identity_id: str,
        capability_id: str,
        intent: str = "",
        context: dict | None = None,
    ):
        return self.decisions.evaluate(
            identity_id=identity_id,
            capability_id=capability_id,
            intent=intent,
            context=context,
        )

    def health(self):
        return {
            "name": "Capability Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
            "registry": self.registry.statistics(),
            "profiles": self.profiles.statistics(),
            "grants": self.grants.statistics(),
            "resolver": self.resolver.health(),
            "decision_engine": self.decisions.health(),
        }


capability_engine = CapabilityEngine()
