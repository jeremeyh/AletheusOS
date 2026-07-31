from __future__ import annotations

from .models import ArchitectureGraph, AtlasReport, TopologySnapshot


class AtlasAnalyzer:
    """Produces simple structural findings from an ArchitectureGraph."""

    def analyze(self, graph: ArchitectureGraph) -> AtlasReport:
        families = {
            node.family
            for node in graph.nodes.values()
            if getattr(node, "family", None)
        }

        snapshot = TopologySnapshot(
            graph=graph,
            subsystem_count=len(
                [n for n in graph.nodes.values() if n.id.startswith("subsystem:")]
            ),
            authority_count=len(
                [n for n in graph.nodes.values() if n.type.value == "authority"]
            ),
            family_count=len(families),
        )

        report = AtlasReport(snapshot=snapshot)

        if snapshot.subsystem_count > 100:
            report.findings.append(
                "Large Super-Mesh detected; authority and collision controls are required."
            )

        if "Unclassified" in families:
            report.warnings.append(
                "Unclassified subsystems detected; Authority Ledger should be updated."
            )

        return report
