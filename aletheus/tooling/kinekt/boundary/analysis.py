"""Analyze dependency relationships against boundary policy."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .models import BoundaryFinding, PackagePressure
from .policy import evaluate
from .taxonomy import classify_layer


def analyze_boundaries(
    dependency: dict[str, Any],
    cohesion: dict[str, Any],
) -> tuple[list[BoundaryFinding], list[PackagePressure], int]:
    raw_nodes = dependency.get("nodes", [])
    raw_relationships = dependency.get("relationships", [])
    raw_packages = cohesion.get("packages", [])

    if not isinstance(raw_nodes, list):
        raise TypeError("Dependency nodes must be a list.")
    if not isinstance(raw_relationships, list):
        raise TypeError("Dependency relationships must be a list.")
    if not isinstance(raw_packages, list):
        raise TypeError("Cohesion packages must be a list.")

    nodes: dict[str, dict[str, Any]] = {
        str(item.get("node_id")): item
        for item in raw_nodes
        if isinstance(item, dict) and isinstance(item.get("node_id"), str)
    }

    findings: list[BoundaryFinding] = []
    unresolved = 0
    inbound: dict[str, int] = defaultdict(int)
    outbound: dict[str, int] = defaultdict(int)
    violations: dict[str, int] = defaultdict(int)
    seams: dict[str, int] = defaultdict(int)

    for relationship in raw_relationships:
        if not isinstance(relationship, dict):
            continue
        if relationship.get("relationship") != "imports":
            continue

        source_id = str(relationship.get("source", ""))
        target_id = str(relationship.get("target", ""))
        source_node = nodes.get(source_id)
        target_node = nodes.get(target_id)

        if source_node is None or target_node is None:
            unresolved += 1
            continue

        source_name = str(source_node.get("name", source_id))
        target_name = str(target_node.get("name", target_id))
        source_layer = classify_layer(
            source_id,
            source_name,
            source_node.get("capability")
            if isinstance(source_node.get("capability"), str)
            else None,
        )
        target_layer = classify_layer(
            target_id,
            target_name,
            target_node.get("capability")
            if isinstance(target_node.get("capability"), str)
            else None,
        )

        source_package = ".".join(source_name.split(".")[:2])
        target_package = ".".join(target_name.split(".")[:2])
        outbound[source_package] += 1
        inbound[target_package] += 1

        if source_layer == "unknown" or target_layer == "unknown":
            unresolved += 1
            continue

        evidence = tuple(
            str(item)
            for item in relationship.get("evidence", [])
            if isinstance(item, str)
        )

        finding = evaluate(
            source_name,
            target_name,
            source_layer,
            target_layer,
            evidence,
        )
        if finding is not None:
            findings.append(finding)
            violations[source_package] += 1
            seams[source_package] += 1

    package_names = {
        str(item.get("package"))
        for item in raw_packages
        if isinstance(item, dict) and isinstance(item.get("package"), str)
    }
    package_names.update(inbound)
    package_names.update(outbound)

    pressure: list[PackagePressure] = []
    for package in sorted(package_names):
        violation_count = violations[package]
        seam_count = seams[package]
        score = max(
            0.0,
            100.0
            - violation_count * 15.0
            - seam_count * 3.0
            - min(20.0, outbound[package] / 10.0),
        )
        status = (
            "healthy"
            if score >= 90
            else "watch"
            if score >= 75
            else "degraded"
            if score >= 60
            else "critical"
        )
        pressure.append(
            PackagePressure(
                package=package,
                inbound_edges=inbound[package],
                outbound_edges=outbound[package],
                violations=violation_count,
                seam_candidates=seam_count,
                score=round(score, 2),
                status=status,
            )
        )

    return (
        sorted(findings, key=lambda item: (item.severity, item.code, item.source)),
        sorted(pressure, key=lambda item: (item.score, item.package)),
        unresolved,
    )
