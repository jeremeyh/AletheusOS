from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

from .contracts import HealthProbeResult


def repository_probe(
    repository_root: Path,
) -> HealthProbeResult:
    required_paths = (
        repository_root / "aletheus",
        repository_root / "nimble",
        repository_root / "tests",
    )

    missing = tuple(str(path) for path in required_paths if not path.exists())

    if missing:
        return HealthProbeResult(
            id="repository-structure",
            name="Repository structure",
            state="degraded",
            detail=("Required repository paths are missing: " + ", ".join(missing)),
            metadata={
                "missingPaths": missing,
            },
        )

    return HealthProbeResult(
        id="repository-structure",
        name="Repository structure",
        state="healthy",
        detail=("Core AletheusOS, Nimble, and test boundaries are present."),
        metadata={
            "repositoryRoot": str(repository_root),
        },
    )


def runtime_import_probe() -> HealthProbeResult:
    module_name = "aletheus.runtime.core"

    specification = importlib.util.find_spec(module_name)

    if specification is None:
        return HealthProbeResult(
            id="runtime-import",
            name="Runtime import boundary",
            state="unavailable",
            detail=(f"Python could not resolve {module_name}."),
        )

    return HealthProbeResult(
        id="runtime-import",
        name="Runtime import boundary",
        state="healthy",
        detail=(
            f"{module_name} is import-resolvable without instantiating the runtime."
        ),
        metadata={
            "origin": specification.origin,
        },
    )


def gateway_import_probe() -> HealthProbeResult:
    module_name = "aletheus.experience_gateway.fastapi_app"

    specification = importlib.util.find_spec(module_name)

    if specification is None:
        return HealthProbeResult(
            id="experience-gateway-import",
            name="Experience Gateway import",
            state="unavailable",
            detail=(f"Python could not resolve {module_name}."),
        )

    return HealthProbeResult(
        id="experience-gateway-import",
        name="Experience Gateway import",
        state="healthy",
        detail=("The bounded Experience Gateway adapter is import-resolvable."),
    )


def nimble_build_probe(
    repository_root: Path,
) -> HealthProbeResult:
    application_root = repository_root / "nimble" / "apps" / "platform-shell"

    package_manifest = application_root / "package.json"

    output_index = application_root / "dist" / "index.html"

    if not package_manifest.exists():
        return HealthProbeResult(
            id="nimble-production-build",
            name="Nimble production build",
            state="unavailable",
            detail=("The Nimble platform-shell package manifest is missing."),
        )

    if not output_index.exists():
        return HealthProbeResult(
            id="nimble-production-build",
            name="Nimble production build",
            state="degraded",
            detail=(
                "The shell exists, but no current production build output was found."
            ),
            metadata={
                "buildOutput": str(output_index),
            },
        )

    return HealthProbeResult(
        id="nimble-production-build",
        name="Nimble production build",
        state="healthy",
        detail=("A Nimble production build artifact is present."),
        metadata={
            "buildOutput": str(output_index),
            "sizeBytes": output_index.stat().st_size,
        },
    )


def gateway_missions() -> list[dict[str, Any]]:
    return [
        {
            "id": "live-provider-registry",
            "name": "Live Provider Registry",
            "description": (
                "Aggregate bounded subsystem state "
                "without coupling Nimble to runtime internals."
            ),
            "state": "active",
            "progress": 78,
            "confidence": 0.96,
        },
        {
            "id": "continuous-runtime-probes",
            "name": "Continuous Runtime Probes",
            "description": (
                "Replace repository-level probes with "
                "registered live subsystem adapters."
            ),
            "state": "active",
            "progress": 34,
            "confidence": 0.88,
        },
        {
            "id": "command-gateway",
            "name": "Command Gateway",
            "description": (
                "Introduce preview, authorization, execution, and reversal contracts."
            ),
            "state": "planned",
            "progress": 10,
            "confidence": 0.91,
        },
    ]
