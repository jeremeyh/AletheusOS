"""Build a consolidated twin snapshot."""

from __future__ import annotations

from typing import Any

from .models import TwinNode, TwinRelationship


def build_nodes(
    repository: dict[str, Any],
    dependency: dict[str, Any],
) -> list[TwinNode]:
    nodes: dict[str, TwinNode] = {}

    for item in repository.get("modules", []):
        if not isinstance(item, dict):
            continue
        module = item.get("module")
        if not isinstance(module, str):
            continue
        node_id = f"module:{module}"
        nodes[node_id] = TwinNode(
            node_id=node_id,
            node_type="module",
            name=module,
            attributes={
                "package": item.get("package"),
                "path": item.get("path"),
                "owner": item.get("owner"),
            },
            provenance=("repository-intelligence",),
        )

    for item in dependency.get("nodes", []):
        if not isinstance(item, dict):
            continue
        node_id = item.get("node_id")
        if not isinstance(node_id, str):
            continue
        existing = nodes.get(node_id)
        merged = dict(existing.attributes) if existing else {}
        merged.update(
            {
                "owner": item.get("owner"),
                "capability": item.get("capability"),
                "evidence": item.get("evidence", []),
            }
        )
        nodes[node_id] = TwinNode(
            node_id=node_id,
            node_type=str(item.get("node_type", "unknown")),
            name=str(item.get("name", node_id)),
            attributes=merged,
            provenance=("constitutional-dependency-graph",),
        )

    return sorted(nodes.values(), key=lambda node: (node.node_type, node.node_id))


def build_relationships(
    dependency: dict[str, Any],
) -> list[TwinRelationship]:
    relationships: list[TwinRelationship] = []
    for item in dependency.get("relationships", []):
        if not isinstance(item, dict):
            continue
        source = item.get("source")
        target = item.get("target")
        relationship = item.get("relationship")
        if not all(isinstance(value, str) for value in (source, target, relationship)):
            continue
        relationships.append(
            TwinRelationship(
                source=source,
                target=target,
                relationship=relationship,
                attributes={
                    "confidence": item.get("confidence"),
                    "policy_status": item.get("policy_status"),
                    "evidence": item.get("evidence", []),
                },
                provenance=("constitutional-dependency-graph",),
            )
        )
    return relationships


def build_metrics(reports: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return {
        "integrity_score": reports["integrity"].get("total_score"),
        "cohesion_score": reports["cohesion"].get("average_score"),
        "health_score": reports["health"].get("total_score"),
        "health_readiness": reports["health"].get("readiness"),
        "boundary_findings": len(reports["boundary"].get("findings", [])),
        "optimization_candidates": len(reports["optimization"].get("candidates", [])),
        "execution_units": len(reports["orchestration"].get("units", [])),
        "topology_modules": len(reports["topology"].get("modules", [])),
    }
