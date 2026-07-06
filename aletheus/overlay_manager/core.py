from __future__ import annotations

from .localization import overlay_localization_service
from .models import OverlayDefinition
from .registry import OverlayRegistry
from .resolver import OverlayResolver
from .storage import overlay_storage
from .themes import overlay_theme_service
from .validation import overlay_validator


class OverlayManager:
    GENESIS = "21.5"
    VERSION = "0.1.0"

    def __init__(self):
        self.registry = OverlayRegistry()
        self.resolver = OverlayResolver(self.registry)
        self.storage = overlay_storage
        self._bootstrapped = False

    def register(self, definition: OverlayDefinition):
        existing = self.registry.list_application(
            definition.application
        )

        validation = overlay_validator.validate(
            definition,
            existing=existing,
        )

        if not validation["valid"]:
            raise ValueError(validation["errors"])

        registered = self.registry.register(definition)
        return registered.to_dict()

    def bootstrap_cardhawk(self):
        if self._bootstrapped:
            return self.statistics()

        definitions = [
            OverlayDefinition(
                overlay_id="cardhawk.visual",
                application="cardhawk",
                foundation_engine="foundation.visual",
                display_name="Hawk A•Eye™",
                description="Visual card intelligence and image recognition.",
                category="Card Intelligence",
                icon="hawk-eye.svg",
                color="gold",
            ),
            OverlayDefinition(
                overlay_id="cardhawk.marketplace",
                application="cardhawk",
                foundation_engine="foundation.marketplace",
                display_name="Marketplace Intelligence™",
                description="Pricing, sales, liquidity, and market analysis.",
                category="Market Intelligence",
                icon="marketplace.svg",
                color="gold",
            ),
            OverlayDefinition(
                overlay_id="cardhawk.forecast",
                application="cardhawk",
                foundation_engine="foundation.forecast",
                display_name="SOAR™",
                description="Long-term forecasting and projection intelligence.",
                category="Forecast Intelligence",
                icon="soar.svg",
                color="gold",
            ),
            OverlayDefinition(
                overlay_id="cardhawk.monitoring",
                application="cardhawk",
                foundation_engine="foundation.monitoring",
                display_name="PERCH™",
                description="Watchlists and continuous monitoring.",
                category="Monitoring",
                icon="perch.svg",
                color="gold",
            ),
            OverlayDefinition(
                overlay_id="cardhawk.acquisition",
                application="cardhawk",
                foundation_engine="foundation.acquisition",
                display_name="TALON™",
                description="Acquisition and execution intelligence.",
                category="Acquisition",
                icon="talon.svg",
                color="gold",
            ),
            OverlayDefinition(
                overlay_id="cardhawk.risk",
                application="cardhawk",
                foundation_engine="foundation.risk",
                display_name="DEF™",
                description="Defensive and risk analysis.",
                category="Risk Intelligence",
                icon="def.svg",
                color="gold",
            ),
            OverlayDefinition(
                overlay_id="cardhawk.portfolio",
                application="cardhawk",
                foundation_engine="foundation.portfolio",
                display_name="ROOST™",
                description="Portfolio and collection management intelligence.",
                category="Portfolio",
                icon="roost.svg",
                color="gold",
            ),
            OverlayDefinition(
                overlay_id="cardhawk.opportunity",
                application="cardhawk",
                foundation_engine="foundation.opportunity",
                display_name="FALCON™",
                description="Opportunity discovery and acquisition targeting.",
                category="Opportunity",
                icon="falcon.svg",
                color="gold",
            ),
            OverlayDefinition(
                overlay_id="cardhawk.action",
                application="cardhawk",
                foundation_engine="foundation.action",
                display_name="STRIKE™",
                description="Action intelligence for buy, sell, hold, and review recommendations.",
                category="Action Intelligence",
                icon="strike.svg",
                color="gold",
            ),
            OverlayDefinition(
                overlay_id="cardhawk.evaluation",
                application="cardhawk",
                foundation_engine="foundation.evaluation",
                display_name="THORᵡ™",
                description="Constitutional evaluation and Relix grading intelligence.",
                category="Evaluation",
                icon="thorx.svg",
                color="gold",
            ),
        ]

        for definition in definitions:
            self.register(definition)

        self._bootstrapped = True
        return self.statistics()

    def resolve(self, application: str, value: str):
        return self.resolver.resolve(application, value)

    def presentation(
        self,
        application: str,
        foundation_engine: str,
        locale: str = "en-US",
    ):
        definition = self.resolver.presentation(
            application,
            foundation_engine,
        )

        return overlay_localization_service.localize(
            definition,
            locale=locale,
        )

    def theme(self, application: str):
        return overlay_theme_service.theme(application)

    def health(self):
        stats = self.registry.statistics()

        return {
            "name": "Overlay Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            "bootstrapped": self._bootstrapped,
            **stats,
        }

    def statistics(self):
        return {
            "name": "Overlay Manager",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            **self.registry.statistics(),
        }


overlay_manager = OverlayManager()
