"""Public Runtime Surface for AletheusOS."""

from __future__ import annotations

from typing import Any

from .models import (
    PlatformHealth,
    PlatformRuntimeSnapshot,
)


def _count_ledger_events(ledger: Any) -> int:
    """
    Resolve the Ledger event count without exposing its implementation.

    Constitutional Ledger implementations may expose event statistics through
    slightly different bounded interfaces during platform evolution.
    """

    if hasattr(ledger, "event_statistics"):
        statistics = ledger.event_statistics()

        if isinstance(statistics, dict):
            return int(
                statistics.get(
                    "events",
                    statistics.get("event_entries", 0),
                )
            )

    if hasattr(ledger, "statistics"):
        statistics = ledger.statistics()

        if isinstance(statistics, dict):
            return int(
                statistics.get(
                    "event_entries",
                    statistics.get("events", 0),
                )
            )

    if hasattr(ledger, "replay_events"):
        try:
            return len(
                ledger.replay_events()
            )
        except TypeError:
            pass

    return 0


class RuntimeSurface:
    """
    Stable, read-only runtime facade.

    Applications may inspect the constitutional runtime through this class,
    but may not mutate internal engines directly.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        orchestrator,
    ) -> None:
        self._orchestrator = orchestrator

    def health(self) -> PlatformHealth:
        orchestrator_health = (
            self._orchestrator.health()
        )

        components = {
            "orchestrator": orchestrator_health,
            "case_engine": (
                orchestrator_health.get(
                    "case_engine",
                    {},
                )
            ),
            "mission_engine": (
                orchestrator_health.get(
                    "mission_engine",
                    {},
                )
            ),
            "time": orchestrator_health.get(
                "time",
                {},
            ),
            "mission_runtime": (
                orchestrator_health.get(
                    "mission_runtime",
                    {},
                )
            ),
        }

        degraded = any(
            isinstance(component, dict)
            and component.get("status")
            in {
                "degraded",
                "failed",
                "offline",
            }
            for component in components.values()
        )

        status = (
            "degraded"
            if degraded
            else "healthy"
        )

        return PlatformHealth(
            status=status,
            healthy=not degraded,
            components=components,
        )

    def snapshot(
        self,
    ) -> PlatformRuntimeSnapshot:
        orchestrator = self._orchestrator

        case_stats = (
            orchestrator
            .case_engine
            .registry
            .statistics()
        )

        mission_stats = (
            orchestrator
            .mission_engine
            .registry
            .statistics()
        )

        time_health = (
            orchestrator.time.health()
        )

        runtime_health = (
            orchestrator
            .mission_runtime
            .health()
        )

        orchestrator_health = (
            orchestrator.health()
        )

        failures = int(
            orchestrator_health.get(
                "failures",
                0,
            )
        ) + int(
            runtime_health.get(
                "failures",
                0,
            )
        )

        status = (
            "degraded"
            if failures
            else "healthy"
        )

        return PlatformRuntimeSnapshot(
            status=status,
            version=self.VERSION,
            cases=int(
                case_stats.get(
                    "cases",
                    0,
                )
            ),
            missions=int(
                mission_stats.get(
                    "missions",
                    0,
                )
            ),
            time_missions=int(
                time_health.get(
                    "missions",
                    0,
                )
            ),
            time_phases=int(
                time_health.get(
                    "phases",
                    0,
                )
            ),
            mission_executions=int(
                runtime_health.get(
                    "missions_executed",
                    0,
                )
            ),
            phase_executions=int(
                runtime_health.get(
                    "phases_executed",
                    0,
                )
            ),
            domain_events_published=int(
                runtime_health.get(
                    "domain_events_published",
                    0,
                )
            ),
            ledger_events=_count_ledger_events(
                orchestrator.ledger
            ),
            failures=failures,
            details={
                "case_registry": case_stats,
                "mission_registry": mission_stats,
                "time": time_health,
                "mission_runtime": runtime_health,
            },
        )

    def version(self) -> str:
        return self.VERSION

    def status(self) -> str:
        return self.health().status
