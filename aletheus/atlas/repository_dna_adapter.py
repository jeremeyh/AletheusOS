from __future__ import annotations

from .models import ArchitectureGraph, AtlasNode, AtlasNodeType


class RepositoryDNAAtlasAdapter:
    """Converts Repository DNA inventory into Atlas graph nodes."""

    def graph_from_inventory(self, records) -> ArchitectureGraph:
        graph = ArchitectureGraph()

        for record in records:
            # Support both dataclass objects and dictionary records.
            if hasattr(record, "__dict__"):
                name = record.name
                path = record.path
                family = getattr(record, "family", "Unclassified")
                py_files = getattr(record, "python_files", 0)
            else:
                name = record["name"]
                path = record["path"]
                family = record.get("family", "Unclassified")
                py_files = record.get("python_files", 0)

            graph.add_node(
                AtlasNode(
                    id=f"subsystem:{name}",
                    name=name,
                    type=self._infer_type(name),
                    family=family,
                    path=path,
                    metadata={
                        "python_files": py_files,
                        "source": "repository_dna",
                    },
                )
            )

        return graph

    def _infer_type(self, name: str) -> AtlasNodeType:
        lowered = name.lower()

        if "runtime" in lowered:
            return AtlasNodeType.RUNTIME
        if "registry" in lowered:
            return AtlasNodeType.REGISTRY
        if "fabric" in lowered:
            return AtlasNodeType.FABRIC
        if "memory" in lowered:
            return AtlasNodeType.MEMORY
        if "security" in lowered or "guardian" in lowered or "conclave" in lowered:
            return AtlasNodeType.SECURITY
        if "council" in lowered or "constitutional" in lowered:
            return AtlasNodeType.GOVERNANCE
        if "engine" in lowered:
            return AtlasNodeType.ENGINE

        return AtlasNodeType.SUBSYSTEM
