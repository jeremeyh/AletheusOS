from __future__ import annotations

from functools import partial
from pathlib import Path

from .contracts import ProviderRegistry
from .default_probes import (
    gateway_import_probe,
    gateway_missions,
    nimble_build_probe,
    repository_probe,
    runtime_import_probe,
)


def create_default_provider_registry(
    repository_root: Path | None = None,
) -> ProviderRegistry:
    root = (
        repository_root
        or Path(__file__).resolve().parents[3]
    )

    registry = ProviderRegistry()

    registry.register_health_probe(
        id="repository-structure",
        name="Repository structure",
        probe=partial(
            repository_probe,
            root,
        ),
        required=True,
    )

    registry.register_health_probe(
        id="runtime-import",
        name="Runtime import boundary",
        probe=runtime_import_probe,
        required=True,
    )

    registry.register_health_probe(
        id="experience-gateway-import",
        name="Experience Gateway import",
        probe=gateway_import_probe,
        required=True,
    )

    registry.register_health_probe(
        id="nimble-production-build",
        name="Nimble production build",
        probe=partial(
            nimble_build_probe,
            root,
        ),
        required=False,
    )

    registry.register_mission_source(
        id="experience-gateway",
        name="Experience Gateway",
        source=gateway_missions,
    )

    return registry
