from __future__ import annotations

from typing import ClassVar

from .models import ExperienceAction, ExperienceSurface, HydrationSource, SurfaceKind


class Engine:
    FIELD_VISION: ClassVar[ExperienceSurface] = ExperienceSurface(
        "field_vision",
        "Field Vision™",
        "Whole-field collectible market intelligence and opportunity awareness.",
        SurfaceKind.ROOM,
        (
            HydrationSource("Gathering Mesh"),
            HydrationSource("Evidence Engine"),
            HydrationSource("Temporal Graph"),
            HydrationSource("Marketplace Intelligence"),
            HydrationSource("Market Saturation Index"),
        ),
        ("A•3ye", "Evidence", "Predictive", "Temporal", "Council"),
        (
            ExperienceAction("open_signal", "Open Signal", "OPEN_SIGNAL"),
            ExperienceAction(
                "move_to_war_room",
                "Move to War Room",
                "OPEN_WAR_ROOM",
                False,
                "war_room",
            ),
        ),
        metadata={
            "regions": (
                "market_heat",
                "momentum",
                "scarcity",
                "msi",
                "auction_velocity",
                "watchlist",
                "a3ye_daily_brief",
                "signals",
            )
        },
    )
    SCOREBOARD: ClassVar[ExperienceSurface] = ExperienceSurface(
        "scoreboard",
        "Scoreboard™",
        "Portfolio performance, allocation, health, liquidity, and governed standing.",
        SurfaceKind.ROOM,
        (
            HydrationSource("Portfolio Engine"),
            HydrationSource("Valuation Determination Engine"),
            HydrationSource("Risk Engine"),
            HydrationSource("Predictive Engine"),
        ),
        ("A•3ye", "THORᵡ", "Predictive", "Memory"),
        (
            ExperienceAction("open_asset", "Open Asset", "OPEN_ASSET"),
            ExperienceAction(
                "rebalance", "Analyze Rebalance", "ANALYZE_REBALANCE", False, "war_room"
            ),
        ),
        metadata={
            "regions": (
                "portfolio_value",
                "gain_loss",
                "allocation",
                "collection_health",
                "liquidity",
                "risk",
                "nuclear_assets",
                "top_movers",
                "hidden_gems",
            )
        },
    )

    def field_vision(self):
        return self.FIELD_VISION

    def scoreboard(self):
        return self.SCOREBOARD
