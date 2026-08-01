from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


class KnowledgeGraphEngine:
    def __init__(self, registry: Path, twin: Path, output: Path) -> None:
        self.registry = registry
        self.twin = twin
        self.output = output

    def build(self) -> dict[str, Any]:
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        twin = json.loads(self.twin.read_text(encoding="utf-8"))
        nodes = twin.get("nodes", [])
        edges = twin.get("relationships", [])
        adjacency: dict[str, list[str]] = defaultdict(list)
        if isinstance(edges, list):
            for edge in edges:
                if not isinstance(edge, dict):
                    continue
                source = edge.get("source")
                target = edge.get("target")
                if isinstance(source, str) and isinstance(target, str):
                    adjacency[source].append(target)
        graph = {
            "nodes": nodes if isinstance(nodes, list) else [],
            "relationships": edges if isinstance(edges, list) else [],
            "adjacency": {key: sorted(set(value)) for key, value in adjacency.items()},
            "registry_capabilities": registry.get("capabilities", []),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "runtime-knowledge-graph.json").write_text(
            json.dumps(graph, indent=2, sort_keys=True), encoding="utf-8"
        )
        (self.output / "graph-statistics.json").write_text(
            json.dumps(
                {
                    "nodes": len(graph["nodes"]),
                    "relationships": len(graph["relationships"]),
                    "adjacency_roots": len(graph["adjacency"]),
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        (self.output / "graph-summary.md").write_text(
            "# Runtime Knowledge Graph\n\n"
            f"- Nodes: **{len(graph['nodes'])}**\n"
            f"- Relationships: **{len(graph['relationships'])}**\n",
            encoding="utf-8",
        )
        return graph
