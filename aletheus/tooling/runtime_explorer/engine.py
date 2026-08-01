from __future__ import annotations

import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


class RuntimeExplorer:
    def __init__(self, twin_path: Path) -> None:
        payload = json.loads(twin_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise TypeError("Digital Twin must be a JSON object.")
        self.nodes = {
            str(node["node_id"]): node
            for node in payload.get("nodes", [])
            if isinstance(node, dict) and "node_id" in node
        }
        self.outgoing: dict[str, set[str]] = defaultdict(set)
        self.incoming: dict[str, set[str]] = defaultdict(set)
        for edge in payload.get("relationships", []):
            if not isinstance(edge, dict):
                continue
            source = edge.get("source")
            target = edge.get("target")
            if isinstance(source, str) and isinstance(target, str):
                self.outgoing[source].add(target)
                self.incoming[target].add(source)

    def node(self, node_id: str) -> dict[str, Any] | None:
        return self.nodes.get(node_id)

    def impact(self, node_id: str, depth: int = 2) -> dict[str, list[str]]:
        visited = {node_id}
        queue = deque([(node_id, 0)])
        downstream: set[str] = set()
        upstream: set[str] = set()

        while queue:
            current, level = queue.popleft()
            if level >= depth:
                continue
            for target in self.outgoing.get(current, set()):
                downstream.add(target)
                if target not in visited:
                    visited.add(target)
                    queue.append((target, level + 1))

        visited = {node_id}
        queue = deque([(node_id, 0)])
        while queue:
            current, level = queue.popleft()
            if level >= depth:
                continue
            for source in self.incoming.get(current, set()):
                upstream.add(source)
                if source not in visited:
                    visited.add(source)
                    queue.append((source, level + 1))

        return {
            "upstream": sorted(upstream),
            "downstream": sorted(downstream),
        }
