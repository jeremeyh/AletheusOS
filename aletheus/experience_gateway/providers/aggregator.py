from __future__ import annotations

from time import perf_counter
from typing import Any

from aletheus.time_utils import utc_now_iso

from .contracts import (
    HealthProbeResult,
    ProviderRegistry,
    RegisteredHealthProbe,
)


class LiveProviderAggregator:
    def __init__(
        self,
        registry: ProviderRegistry,
    ) -> None:
        self._registry = registry

    def health_payload(self) -> dict[str, Any]:
        registered = self._registry.health_probes()
        checked_at = utc_now_iso()

        results = tuple(
            self._execute_probe(probe)
            for probe in registered
        )

        total_checks = len(results)

        passing_checks = sum(
            result.state == "healthy"
            for result in results
        )

        warning_count = sum(
            result.state in {
                "degraded",
                "unknown",
            }
            for result in results
        )

        required_failures = [
            result
            for probe, result in zip(
                registered,
                results,
                strict=True,
            )
            if (
                probe.required
                and result.state
                in {
                    "unavailable",
                    "unknown",
                }
            )
        ]

        state = self._aggregate_health_state(
            results=results,
            required_failure_count=len(
                required_failures
            ),
        )

        return {
            "state": state,
            "summary": self._summary(
                state=state,
                total_checks=total_checks,
                passing_checks=passing_checks,
                required_failure_count=len(
                    required_failures
                ),
            ),
            "passing_checks": passing_checks,
            "total_checks": total_checks,
            "warning_count": warning_count,
            "confidence": self._confidence(
                results
            ),
            "checks": [
                {
                    "id": result.id,
                    "name": result.name,
                    "state": result.state,
                    "detail": result.detail,
                    "latency_ms": result.latency_ms,
                    "checked_at": checked_at,
                    "metadata": result.metadata,
                }
                for result in results
            ],
        }

    def mission_payload(
        self,
    ) -> list[dict[str, Any]]:
        missions: list[dict[str, Any]] = []

        for registered in (
            self._registry.mission_sources()
        ):
            try:
                source_missions = registered.source()
            except Exception as error:
                missions.append(
                    {
                        "id": (
                            f"{registered.id}-source-failure"
                        ),
                        "name": registered.name,
                        "description": (
                            "Mission source failed: "
                            f"{type(error).__name__}: "
                            f"{error}"
                        ),
                        "state": "blocked",
                        "progress": 0,
                        "confidence": 1.0,
                    }
                )
                continue

            for mission in source_missions:
                missions.append(
                    self._normalize_mission(
                        source_id=registered.id,
                        mission=mission,
                    )
                )

        return missions

    @staticmethod
    def _execute_probe(
        registered: RegisteredHealthProbe,
    ) -> HealthProbeResult:
        started_at = perf_counter()

        try:
            result = registered.probe()
        except Exception as error:
            elapsed_ms = round(
                (perf_counter() - started_at)
                * 1000
            )

            return HealthProbeResult(
                id=registered.id,
                name=registered.name,
                state="unavailable",
                detail=(
                    f"{type(error).__name__}: {error}"
                ),
                latency_ms=elapsed_ms,
                metadata={
                    "required": registered.required,
                    "failureType": type(
                        error
                    ).__name__,
                },
            )

        elapsed_ms = round(
            (perf_counter() - started_at)
            * 1000
        )

        return HealthProbeResult(
            id=result.id or registered.id,
            name=result.name or registered.name,
            state=result.state,
            detail=result.detail,
            latency_ms=(
                result.latency_ms
                if result.latency_ms is not None
                else elapsed_ms
            ),
            metadata={
                "required": registered.required,
                **result.metadata,
            },
        )

    @staticmethod
    def _aggregate_health_state(
        *,
        results: tuple[
            HealthProbeResult,
            ...,
        ],
        required_failure_count: int,
    ) -> str:
        if not results:
            return "unknown"

        if required_failure_count > 0:
            return "unavailable"

        if any(
            result.state
            in {
                "degraded",
                "unavailable",
                "unknown",
            }
            for result in results
        ):
            return "degraded"

        return "healthy"

    @staticmethod
    def _summary(
        *,
        state: str,
        total_checks: int,
        passing_checks: int,
        required_failure_count: int,
    ) -> str:
        if total_checks == 0:
            return (
                "No live runtime health providers "
                "are currently registered."
            )

        if state == "healthy":
            return (
                f"All {total_checks} registered runtime "
                "providers are healthy."
            )

        if state == "unavailable":
            return (
                f"{required_failure_count} required runtime "
                "provider(s) are unavailable."
            )

        return (
            f"{passing_checks} of {total_checks} registered "
            "runtime providers are healthy."
        )

    @staticmethod
    def _confidence(
        results: tuple[
            HealthProbeResult,
            ...,
        ],
    ) -> float:
        if not results:
            return 0.2

        observable = sum(
            result.state != "unknown"
            for result in results
        )

        return round(
            0.5 + (
                observable
                / len(results)
            ) * 0.49,
            2,
        )

    @staticmethod
    def _normalize_mission(
        *,
        source_id: str,
        mission: dict[str, Any],
    ) -> dict[str, Any]:
        raw_id = str(
            mission.get(
                "id",
                "unnamed",
            )
        ).strip()

        state = mission.get(
            "state",
            "planned",
        )

        if state not in {
            "planned",
            "active",
            "blocked",
            "complete",
        }:
            state = "planned"

        progress = max(
            0,
            min(
                100,
                int(
                    mission.get(
                        "progress",
                        0,
                    )
                ),
            ),
        )

        return {
            "id": f"{source_id}:{raw_id}",
            "name": str(
                mission.get(
                    "name",
                    raw_id,
                )
            ),
            "description": str(
                mission.get(
                    "description",
                    "",
                )
            ),
            "state": state,
            "progress": progress,
            "confidence": float(
                mission.get(
                    "confidence",
                    0.8,
                )
            ),
        }
