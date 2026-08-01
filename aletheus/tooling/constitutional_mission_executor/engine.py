from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(
        self, orchestrator: Path, mission_graph: Path, bus: Path, output: Path
    ) -> None:
        self.orchestrator = orchestrator
        self.mission_graph = mission_graph
        self.bus = bus
        self.output = output

    def build(self) -> dict[str, Any]:
        orchestration = json.loads(self.orchestrator.read_text(encoding="utf-8"))
        graph = json.loads(self.mission_graph.read_text(encoding="utf-8"))
        bus = json.loads(self.bus.read_text(encoding="utf-8"))
        channels = {
            item.get("channel_id")
            for item in bus.get("channels", [])
            if isinstance(item, dict)
        }
        missions = []
        for unit in orchestration.get("units", []):
            if not isinstance(unit, dict):
                continue
            missions.append(
                {
                    "mission_id": f"mission::{unit.get('unit_id')}",
                    "unit_id": unit.get("unit_id"),
                    "status": "awaiting_approval",
                    "scheduler": "Mission Scheduler",
                    "executor": "Mission Engine",
                    "service_bus_available": bool(channels),
                    "execution_enabled": False,
                }
            )
        report = {
            "missions": missions,
            "mission_count": len(missions),
            "graph_nodes": len(graph.get("nodes", [])),
            "mode": "approval_gated",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "constitutional-mission-executor.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
