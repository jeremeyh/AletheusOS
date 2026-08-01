from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(
        self, catalog: Path, graph: Path, observability: Path, output: Path
    ) -> None:
        self.catalog = catalog
        self.graph = graph
        self.observability = observability
        self.output = output

    def build(self) -> dict[str, Any]:
        catalog = json.loads(self.catalog.read_text(encoding="utf-8"))
        graph = json.loads(self.graph.read_text(encoding="utf-8"))
        observability = json.loads(self.observability.read_text(encoding="utf-8"))
        report = {
            "layer": "Breadth",
            "role": "shroud_layer",
            "owns_decisions": False,
            "owns_execution": False,
            "owns_governance": False,
            "catalog_entries": len(catalog.get("entries", [])),
            "knowledge_nodes": len(graph.get("nodes", [])),
            "readiness": observability.get("readiness", "unknown"),
            "awareness_scope": "whole_system",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "breadth-shroud-layer.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
