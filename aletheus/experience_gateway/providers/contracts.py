from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from threading import RLock
from typing import Any, Literal


ProbeState = Literal[
    "healthy",
    "degraded",
    "unavailable",
    "unknown",
]

MissionState = Literal[
    "planned",
    "active",
    "blocked",
    "complete",
]


@dataclass(frozen=True, slots=True)
class HealthProbeResult:
    id: str
    name: str
    state: ProbeState
    detail: str
    latency_ms: int | None = None
    metadata: dict[str, Any] = field(
        default_factory=dict
    )


HealthProbe = Callable[[], HealthProbeResult]
MissionSource = Callable[
    [],
    Iterable[dict[str, Any]],
]


@dataclass(frozen=True, slots=True)
class RegisteredHealthProbe:
    id: str
    name: str
    probe: HealthProbe
    required: bool = False


@dataclass(frozen=True, slots=True)
class RegisteredMissionSource:
    id: str
    name: str
    source: MissionSource


class ProviderRegistry:
    """Thread-safe registry for bounded experience providers."""

    def __init__(self) -> None:
        self._health_probes: dict[
            str,
            RegisteredHealthProbe,
        ] = {}

        self._mission_sources: dict[
            str,
            RegisteredMissionSource,
        ] = {}

        self._lock = RLock()

    def register_health_probe(
        self,
        *,
        id: str,
        name: str,
        probe: HealthProbe,
        required: bool = False,
        replace: bool = False,
    ) -> None:
        normalized_id = _require_identifier(id)
        normalized_name = _require_text(
            name,
            "Health probe name",
        )

        with self._lock:
            if (
                normalized_id in self._health_probes
                and not replace
            ):
                raise ValueError(
                    "Health probe already registered: "
                    f"{normalized_id}"
                )

            self._health_probes[normalized_id] = (
                RegisteredHealthProbe(
                    id=normalized_id,
                    name=normalized_name,
                    probe=probe,
                    required=required,
                )
            )

    def register_mission_source(
        self,
        *,
        id: str,
        name: str,
        source: MissionSource,
        replace: bool = False,
    ) -> None:
        normalized_id = _require_identifier(id)
        normalized_name = _require_text(
            name,
            "Mission source name",
        )

        with self._lock:
            if (
                normalized_id in self._mission_sources
                and not replace
            ):
                raise ValueError(
                    "Mission source already registered: "
                    f"{normalized_id}"
                )

            self._mission_sources[normalized_id] = (
                RegisteredMissionSource(
                    id=normalized_id,
                    name=normalized_name,
                    source=source,
                )
            )

    def health_probes(
        self,
    ) -> tuple[RegisteredHealthProbe, ...]:
        with self._lock:
            return tuple(
                self._health_probes.values()
            )

    def mission_sources(
        self,
    ) -> tuple[RegisteredMissionSource, ...]:
        with self._lock:
            return tuple(
                self._mission_sources.values()
            )

    def describe(self) -> dict[str, Any]:
        with self._lock:
            return {
                "healthProbes": [
                    {
                        "id": item.id,
                        "name": item.name,
                        "required": item.required,
                    }
                    for item in self._health_probes.values()
                ],
                "missionSources": [
                    {
                        "id": item.id,
                        "name": item.name,
                    }
                    for item in self._mission_sources.values()
                ],
            }


def _require_identifier(value: str) -> str:
    normalized = value.strip()

    if not normalized:
        raise ValueError(
            "Provider identifier cannot be empty."
        )

    return normalized


def _require_text(
    value: str,
    label: str,
) -> str:
    normalized = value.strip()

    if not normalized:
        raise ValueError(
            f"{label} cannot be empty."
        )

    return normalized
