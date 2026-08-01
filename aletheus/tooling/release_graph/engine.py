from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, manifests_root: Path, output: Path) -> None:
        self.manifests_root = manifests_root
        self.output = output

    def build(self) -> dict[str, Any]:
        nodes: dict[str, dict[str, Any]] = {}
        edges: list[dict[str, str]] = []
        for manifest_path in self.manifests_root.rglob("release-manifest.json"):
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            release_id = str(payload["release_id"])
            nodes[release_id] = {
                "release_id": release_id,
                "version": payload["version"],
                "title": payload["title"],
                "manifest": str(manifest_path),
            }
            for dependency in payload.get("dependencies", []):
                edges.append(
                    {
                        "source": str(dependency),
                        "target": release_id,
                        "kind": "requires",
                    }
                )
        indegree = defaultdict(int)
        graph = defaultdict(list)
        for edge in edges:
            graph[edge["source"]].append(edge["target"])
            indegree[edge["target"]] += 1
        queue = deque(sorted(node for node in nodes if indegree[node] == 0))
        order = []
        while queue:
            node = queue.popleft()
            order.append(node)
            for target in sorted(graph[node]):
                indegree[target] -= 1
                if indegree[target] == 0:
                    queue.append(target)
        report = {
            "nodes": list(nodes.values()),
            "edges": edges,
            "release_count": len(nodes),
            "topological_order": order,
            "cycle_free": len(order) == len(nodes),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "release-graph.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
