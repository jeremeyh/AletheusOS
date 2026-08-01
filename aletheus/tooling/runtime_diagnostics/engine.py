from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, observability: Path, governance: Path, output: Path) -> None:
        self.observability = observability
        self.governance = governance
        self.output = output

    def build(self) -> dict[str, Any]:
        observability = json.loads(self.observability.read_text(encoding="utf-8"))
        governance = json.loads(self.governance.read_text(encoding="utf-8"))
        diagnostics = []
        if observability.get("readiness") == "not_ready":
            diagnostics.append({"code": "RUNTIME_NOT_READY", "severity": "high"})
        if governance.get("decision") in {"warn", "block"}:
            diagnostics.append(
                {
                    "code": "GOVERNANCE_ATTENTION_REQUIRED",
                    "severity": "high"
                    if governance.get("decision") == "block"
                    else "medium",
                }
            )
        report = {"diagnostics": diagnostics, "diagnostic_count": len(diagnostics)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "constitutional-runtime-diagnostics.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
