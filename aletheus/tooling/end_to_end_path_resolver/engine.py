from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, wiring: Path, output: Path) -> None:
        self.wiring = wiring
        self.output = output

    def build(self) -> dict[str, Any]:
        wiring = json.loads(self.wiring.read_text(encoding="utf-8"))
        adjacency: dict[str, list[str]] = defaultdict(list)
        nodes: set[str] = set()
        for route in wiring.get("routes", []):
            if not isinstance(route, dict):
                continue
            source = str(route.get("source"))
            target = str(route.get("target"))
            adjacency[source].append(target)
            nodes.update((source, target))

        roots = sorted(
            node
            for node in nodes
            if all(node not in targets for targets in adjacency.values())
        )
        leaves = sorted(node for node in nodes if not adjacency.get(node))
        report = {
            "nodes": sorted(nodes),
            "roots": roots,
            "leaves": leaves,
            "adjacency": {key: sorted(set(value)) for key, value in adjacency.items()},
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "end-to-end-path-resolver.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
