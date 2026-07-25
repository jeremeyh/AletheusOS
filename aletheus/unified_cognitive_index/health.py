from __future__ import annotations

from .registry import uci


def health_report() -> dict:
    """
    Generate a health report for the Unified Cognitive Index.

    The UCI is healthy when:
      • Nodes are indexed
      • Relationships exist
      • Few orphan nodes exist
      • Relationship density remains healthy
    """

    report = uci.health()

    density = 0.0

    if report.node_count > 0:
        density = (
            report.relationship_count
            / report.node_count
        )

    return {
        "status": report.status,
        "node_count": report.node_count,
        "relationship_count": report.relationship_count,
        "orphan_nodes": report.orphan_node_count,
        "average_relationship_weight": round(
            report.average_relationship_weight,
            3,
        ),
        "relationship_density": round(
            density,
            3,
        ),
    }


def statistics() -> dict:
    """
    Convenience statistics endpoint.
    """

    stats = uci.statistics()

    return {
        **stats,
        **health_report(),
    }


def is_healthy() -> bool:
    report = uci.health()

    return (
        report.node_count >= 0
        and report.relationship_count >= 0
    )
