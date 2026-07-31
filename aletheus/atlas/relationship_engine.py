from __future__ import annotations

from .models import ArchitectureGraph, AtlasEdge, AtlasEdgeType


class RelationshipEngine:
    """Adds semantic relationships based on authority/family inference."""

    def enrich_family_relationships(
        self, graph: ArchitectureGraph
    ) -> ArchitectureGraph:
        family_nodes: set[str] = set()

        for node in list(graph.nodes.values()):
            if not node.family:
                continue

            family_id = f"family:{node.family}"
            if family_id not in graph.nodes:
                from .models import AtlasNode, AtlasNodeType

                graph.add_node(
                    AtlasNode(id=family_id, name=node.family, type=AtlasNodeType.FAMILY)
                )
                family_nodes.add(family_id)

            graph.add_edge(
                AtlasEdge(
                    source_id=node.id,
                    target_id=family_id,
                    type=AtlasEdgeType.BELONGS_TO,
                    confidence=0.9,
                )
            )

        return graph
