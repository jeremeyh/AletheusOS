from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, graph: Path, output: Path) -> None:
        self.graph = graph
        self.output = output

    def build(self) -> dict[str, Any]:
        payload = json.loads(self.graph.read_text(encoding="utf-8"))
        telemetry = [
            {
                "node_id": node.get("node_id"),
                "timestamp": datetime.now(UTC).isoformat(),
                "latency_ms": None,
                "throughput": None,
                "status": "not_executed",
                "provenance": "mission_execution_graph",
            }
            for node in payload.get("nodes", [])
            if isinstance(node, dict)
        ]
        report = {"telemetry": telemetry, "record_count": len(telemetry)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "runtime-telemetry.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
