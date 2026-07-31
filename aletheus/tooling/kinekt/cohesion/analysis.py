"""Package cohesion calculations."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .models import CohesionSignal, PackageCohesion


def _status(score: float) -> str:
    if score >= 90:
        return "cohesive"
    if score >= 75:
        return "watch"
    if score >= 60:
        return "fragmented"
    return "critical"


def _bounded(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def analyze_packages(
    topology: dict[str, Any],
    dependency: dict[str, Any],
) -> list[PackageCohesion]:
    raw_packages = topology.get("packages", [])
    raw_nodes = dependency.get("nodes", [])

    if not isinstance(raw_packages, list):
        raise TypeError("Topology packages must be a list.")
    if not isinstance(raw_nodes, list):
        raise TypeError("Dependency nodes must be a list.")

    capabilities_by_package: dict[str, set[str]] = defaultdict(set)
    owners_by_package: dict[str, set[str]] = defaultdict(set)

    module_package: dict[str, str] = {}
    for item in raw_nodes:
        if not isinstance(item, dict):
            continue
        node_id = item.get("node_id")
        node_type = item.get("node_type")
        if node_type != "module" or not isinstance(node_id, str):
            continue
        module = str(item.get("name", ""))
        capability = item.get("capability")
        owner = item.get("owner")
        evidence = item.get("evidence", [])
        package = None
        if isinstance(evidence, list) and evidence:
            path = str(evidence[0])
            parts = path.split("/")
            if len(parts) >= 2 and parts[0] == "aletheus":
                package = ".".join(parts[:2])
        if package is None and module.startswith("aletheus."):
            package = ".".join(module.split(".")[:2])
        if package is None:
            continue
        module_package[module] = package
        if isinstance(capability, str) and capability:
            capabilities_by_package[package].add(capability)
        if isinstance(owner, str) and owner:
            owners_by_package[package].add(owner)

    results: list[PackageCohesion] = []
    for raw in raw_packages:
        if not isinstance(raw, dict):
            continue

        package = str(raw.get("package", "unknown"))
        modules = int(raw.get("modules", 0))
        internal_edges = int(raw.get("internal_edges", 0))
        inbound = len(raw.get("inbound_packages", []))
        outbound = len(raw.get("outbound_packages", []))
        isolated = int(raw.get("isolated_modules", 0))
        cycles = int(raw.get("cycle_groups", 0))
        capability_count = len(capabilities_by_package.get(package, set()))
        owner_count = len(owners_by_package.get(package, set()))

        score = 100.0
        signals: list[CohesionSignal] = []
        recommendations: list[str] = []

        isolated_ratio = isolated / modules if modules else 1.0
        score -= min(35.0, isolated_ratio * 35.0)
        signals.append(
            CohesionSignal(
                "isolated_ratio",
                round(isolated_ratio, 4),
                f"{isolated} of {modules} module(s) are isolated.",
            )
        )
        if isolated_ratio > 0.5:
            recommendations.append(
                "Review isolated modules for dynamic registration, archival, or missing integration."
            )

        density = internal_edges / max(1, modules)
        if density < 0.5:
            score -= min(20.0, (0.5 - density) * 40.0)
            recommendations.append(
                "Review whether the package groups modules with a shared responsibility."
            )
        signals.append(
            CohesionSignal(
                "internal_edge_density",
                round(density, 4),
                f"{internal_edges} internal edge(s) across {modules} module(s).",
            )
        )

        external_pressure = outbound / max(1, modules)
        score -= min(15.0, external_pressure * 10.0)
        signals.append(
            CohesionSignal(
                "outbound_pressure",
                round(external_pressure, 4),
                f"{outbound} outbound package dependency set(s).",
            )
        )
        if external_pressure > 0.75:
            recommendations.append(
                "Reduce outbound dependency pressure or introduce a stable package boundary."
            )

        if capability_count > 1:
            score -= min(15.0, (capability_count - 1) * 4.0)
            recommendations.append(
                "Review mixed capability ownership and consider extracting bounded responsibilities."
            )

        if owner_count > 1:
            score -= min(10.0, (owner_count - 1) * 3.0)
            recommendations.append("Clarify canonical ownership for this package.")

        if cycles:
            score -= min(20.0, cycles * 5.0)
            recommendations.append(
                "Review cycle-group participation before further expansion."
            )

        if modules > 150:
            score -= min(15.0, (modules - 150) / 20.0)
            recommendations.append(
                "Package size indicates possible bounded-growth pressure."
            )

        bounded = _bounded(score)
        results.append(
            PackageCohesion(
                package=package,
                score=bounded,
                status=_status(bounded),
                modules=modules,
                internal_edges=internal_edges,
                inbound_packages=inbound,
                outbound_packages=outbound,
                isolated_modules=isolated,
                cycle_groups=cycles,
                capability_count=capability_count,
                owner_count=owner_count,
                signals=tuple(signals),
                recommendations=tuple(dict.fromkeys(recommendations)),
            )
        )

    return sorted(results, key=lambda item: (item.score, item.package))
