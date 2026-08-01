from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, telemetry: Path, observatory: Path, output: Path) -> None:
        self.telemetry = telemetry
        self.observatory = observatory
        self.output = output

    def build(self) -> dict[str, Any]:
        telemetry = json.loads(self.telemetry.read_text(encoding="utf-8"))
        observatory = json.loads(self.observatory.read_text(encoding="utf-8"))
        report = {
            "telemetry_records": telemetry.get("record_count", 0),
            "health_score": observatory.get("health_score", 0),
            "readiness": observatory.get("readiness", "unknown"),
            "alerts": observatory.get("alerts", []),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "runtime-observability.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
