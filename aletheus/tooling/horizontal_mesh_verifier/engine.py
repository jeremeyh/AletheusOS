from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, mesh: Path, connectors: Path, output: Path) -> None:
        self.mesh = mesh
        self.connectors = connectors
        self.output = output

    def build(self) -> dict[str, Any]:
        mesh = json.loads(self.mesh.read_text(encoding="utf-8"))
        connectors = json.loads(self.connectors.read_text(encoding="utf-8"))
        edge_count = len(mesh.get("edges", []))
        connector_count = connectors.get("connector_count", 0)
        report = {
            "mesh_edges": edge_count,
            "connectors": connector_count,
            "horizontal_mesh_connected": edge_count > 0
            and connector_count == edge_count,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "horizontal-mesh-verification.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
