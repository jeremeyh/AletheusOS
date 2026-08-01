from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, access_modules: Path, graph: Path, output: Path) -> None:
        self.access_modules = access_modules
        self.graph = graph
        self.output = output

    def build(self) -> dict[str, Any]:
        access = json.loads(self.access_modules.read_text(encoding="utf-8"))
        graph = json.loads(self.graph.read_text(encoding="utf-8"))
        nodes = {
            str(item.get("node_id"))
            for item in graph.get("nodes", [])
            if isinstance(item, dict)
        }

        touchpoints = []
        for module in access.get("access_modules", []):
            if not isinstance(module, dict):
                continue
            connector = str(module.get("connector_id"))
            touchpoints.append(
                {
                    "touchpoint_id": f"touch::{connector}",
                    "access_module_id": module.get("access_module_id"),
                    "contract_present": module.get("contract_present"),
                    "knowledge_graph_attached": bool(nodes),
                    "status": "realized",
                }
            )
        report = {"touchpoints": touchpoints, "touchpoint_count": len(touchpoints)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "platform-touchpoint-matrix.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
