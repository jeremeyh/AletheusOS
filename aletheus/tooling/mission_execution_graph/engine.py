from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, orchestration: Path, output: Path) -> None:
        self.orchestration = orchestration
        self.output = output

    def build(self) -> dict[str, Any]:
        payload = json.loads(self.orchestration.read_text(encoding="utf-8"))
        units = payload.get("units", [])
        if not isinstance(units, list):
            raise TypeError("Orchestration units must be a list.")

        nodes = [
            {"node_id": str(unit.get("unit_id")), "status": unit.get("status")}
            for unit in units
            if isinstance(unit, dict)
        ]
        edges = [
            {"source": nodes[index]["node_id"], "target": nodes[index + 1]["node_id"]}
            for index in range(max(0, len(nodes) - 1))
        ]
        graph = {"nodes": nodes, "edges": edges}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "mission-execution-graph.json").write_text(
            json.dumps(graph, indent=2, sort_keys=True), encoding="utf-8"
        )
        return graph
