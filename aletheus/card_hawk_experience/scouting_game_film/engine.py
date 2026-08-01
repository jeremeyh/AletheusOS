from __future__ import annotations

from typing import ClassVar

from .models import ExperienceAction, ExperienceSurface, HydrationSource, SurfaceKind


class Engine:
    SCOUTING_REPORT: ClassVar[ExperienceSurface] = ExperienceSurface(
        "scouting_report",
        "Scouting Report™",
        "Deep asset intelligence, evidence, history, valuation, scarcity, provenance, and alternatives.",
        SurfaceKind.ROOM,
        (
            HydrationSource("Evidence Engine"),
            HydrationSource("Collectibles Evidence Graph"),
            HydrationSource("Valuation Determination Engine"),
            HydrationSource("Marketplace Intelligence"),
            HydrationSource("Predictive Engine"),
        ),
        ("A•3ye", "THORᵡ", "Evidence", "Knowledge", "Predictive", "Truth"),
        (
            ExperienceAction("compare", "Compare", "OPEN_MATCHUP"),
            ExperienceAction("watch", "Add to Watchlist", "ADD_WATCHLIST"),
            ExperienceAction(
                "war_room", "Move to War Room", "OPEN_WAR_ROOM", False, "war_room"
            ),
        ),
        metadata={
            "regions": (
                "overview",
                "timeline",
                "population",
                "sales",
                "comps",
                "rarity",
                "authenticity",
                "provenance",
                "market_trend",
                "alternatives",
                "a3ye_summary",
            )
        },
    )
    GAME_FILM: ClassVar[ExperienceSurface] = ExperienceSurface(
        "game_film",
        "Game Film™",
        "Historical market replay and counterfactual review across assets, portfolios, and decisions.",
        SurfaceKind.ROOM,
        (
            HydrationSource("Temporal Graph"),
            HydrationSource("Marketplace History"),
            HydrationSource("Portfolio History"),
            HydrationSource("Memory Engine"),
            HydrationSource("Predictive Engine"),
        ),
        ("A•3ye", "Temporal", "Predictive", "Memory", "Reason"),
        (
            ExperienceAction("scrub_timeline", "Scrub Timeline", "SCRUB_TIMELINE"),
            ExperienceAction("replay_decision", "Replay Decision", "REPLAY_DECISION"),
            ExperienceAction("run_what_if", "Run What-If", "RUN_COUNTERFACTUAL"),
        ),
        metadata={
            "regions": (
                "timeline",
                "price_history",
                "population_history",
                "market_events",
                "user_decisions",
                "missed_opportunities",
                "wins",
                "counterfactuals",
            )
        },
    )

    def scouting_report(self):
        return self.SCOUTING_REPORT

    def game_film(self):
        return self.GAME_FILM
