"""Constitutional civilization bootstrap orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aletheus.constitutional_graph import ConstitutionalKnowledgeGraph
from aletheus.platform_registry import PlatformRegistry

from .canonical_catalog import canonical_institutions
from .projection import InstitutionProjector
from .readiness import (
    CivilizationReadinessReport,
    ReadinessCheck,
    ReadinessState,
)
from .registry import InstitutionRegistry
from .wiring import InstitutionWiring


class CivilizationBootstrap:
    """
    Establish and verify the institutional civilization.

    Intended placement:

        LighthouseBootloader
            -> CivilizationBootstrap
            -> BootRuntime
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        root: str | Path = ".",
        institution_registry: InstitutionRegistry | None = None,
        platform_registry: PlatformRegistry | None = None,
        constitutional_graph: ConstitutionalKnowledgeGraph | None = None,
        wiring: InstitutionWiring | None = None,
    ) -> None:
        self.root = Path(root).resolve()
        self.institution_registry = (
            institution_registry or InstitutionRegistry()
        )
        self.platform_registry = platform_registry or PlatformRegistry()
        self.constitutional_graph = (
            constitutional_graph or ConstitutionalKnowledgeGraph()
        )
        self.projector = InstitutionProjector(
            institution_registry=self.institution_registry,
            platform_registry=self.platform_registry,
            constitutional_graph=self.constitutional_graph,
        )
        self.wiring = wiring or InstitutionWiring(root=self.root)

    def bootstrap(self) -> CivilizationReadinessReport:
        report = CivilizationReadinessReport(
            metadata={
                "version": self.VERSION,
                "root": str(self.root),
            }
        )

        records = canonical_institutions()

        try:
            projections = self.projector.project_all(records)
            graph_stats = self.constitutional_graph.statistics()

            report.institution_count = len(records)
            report.platform_component_count = (
                self.platform_registry.statistics()["components"]
            )
            report.graph_node_count = graph_stats["nodes"]
            report.graph_edge_count = graph_stats["edges"]

            report.checks.append(
                ReadinessCheck(
                    name="institution_projection",
                    institution_id=(
                        "aletheus.institutional_civilization"
                    ),
                    state=ReadinessState.READY,
                    message=(
                        f"Projected {len(projections)} canonical "
                        "institutions."
                    ),
                    evidence={
                        "projection_count": len(projections),
                        "graph_nodes": report.graph_node_count,
                        "graph_edges": report.graph_edge_count,
                    },
                )
            )
        except Exception as exc:
            report.checks.append(
                ReadinessCheck(
                    name="institution_projection",
                    institution_id=(
                        "aletheus.institutional_civilization"
                    ),
                    state=ReadinessState.FAILED,
                    message=str(exc),
                )
            )
            report.calculate_harmony()
            return report

        watch_tower_check = self.wiring.run_watch_tower()
        spa_check = self.wiring.run_spa()

        report.checks.extend([
            watch_tower_check,
            spa_check,
        ])

        homeostasis_check = self.wiring.update_homeostasis(
            list(report.checks)
        )
        report.checks.append(homeostasis_check)

        council_check = self.wiring.escalate_to_council(
            list(report.checks)
        )
        report.checks.append(council_check)

        report.calculate_harmony()

        ledger_check = self.wiring.record_boot(
            {
                "bootstrap_id": report.bootstrap_id,
                "status": report.status,
                "institution_count": report.institution_count,
                "platform_component_count": (
                    report.platform_component_count
                ),
                "graph_node_count": report.graph_node_count,
                "graph_edge_count": report.graph_edge_count,
                "synthetic_harmony": report.synthetic_harmony,
                "checks": [
                    check.to_dict()
                    for check in report.checks
                ],
            }
        )
        report.checks.append(ledger_check)
        report.calculate_harmony()

        return report

    def health(self) -> dict[str, Any]:
        return {
            "name": "Civilization Bootstrap",
            "version": self.VERSION,
            "status": "online",
            "institutions": (
                self.institution_registry.statistics()["institutions"]
            ),
            "platform_components": (
                self.platform_registry.statistics()["components"]
            ),
            **self.constitutional_graph.statistics(),
        }
