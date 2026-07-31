from __future__ import annotations

from pathlib import Path

from .models import ArchitectureGraph, AtlasNode, AtlasNodeType, TopologySnapshot


class TopologyEngine:
    """Discovers top-level architectural subsystems from the repository."""

    def discover_from_path(self, aletheus_root: Path) -> TopologySnapshot:
        graph = ArchitectureGraph()

        for child in sorted(aletheus_root.iterdir()):
            if not child.is_dir() or child.name.startswith("__"):
                continue

            node = AtlasNode(
                id=f"subsystem:{child.name}",
                name=child.name,
                type=self._infer_type(child.name),
                path=str(child),
                family=self._infer_family(child.name),
            )
            graph.add_node(node)

        families = {node.family for node in graph.nodes.values() if node.family}
        authorities = {
            node.authority for node in graph.nodes.values() if node.authority
        }

        return TopologySnapshot(
            graph=graph,
            subsystem_count=graph.node_count(),
            authority_count=len(authorities),
            family_count=len(families),
        )

    def _infer_type(self, name: str) -> AtlasNodeType:
        lowered = name.lower()
        if "runtime" in lowered:
            return AtlasNodeType.RUNTIME
        if "registry" in lowered:
            return AtlasNodeType.REGISTRY
        if "fabric" in lowered:
            return AtlasNodeType.FABRIC
        if "circuit" in lowered:
            return AtlasNodeType.CIRCUIT
        if "memory" in lowered:
            return AtlasNodeType.MEMORY
        if "security" in lowered or "guardian" in lowered or "conclave" in lowered:
            return AtlasNodeType.SECURITY
        if "council" in lowered or "constitutional" in lowered:
            return AtlasNodeType.GOVERNANCE
        if "engine" in lowered:
            return AtlasNodeType.ENGINE
        return AtlasNodeType.SUBSYSTEM

    def _infer_family(self, name: str) -> str:
        lowered = name.lower()
        if "runtime" in lowered:
            return "Execution"
        if "memory" in lowered or "knowledge" in lowered or "cognitive" in lowered:
            return "Memory / Awareness"
        if "constitutional" in lowered or "council" in lowered:
            return "Constitutional"
        if "security" in lowered or "guardian" in lowered or "conclave" in lowered:
            return "Security / Defense"
        if "registry" in lowered:
            return "Registry"
        if (
            "atlas" in lowered
            or "oracle" in lowered
            or "watch" in lowered
            or "repository" in lowered
        ):
            return "Platform Intelligence"
        return "Unclassified"
