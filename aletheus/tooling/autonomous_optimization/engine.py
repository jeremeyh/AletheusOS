from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, diagnostics: Path, optimization: Path, output: Path) -> None:
        self.diagnostics = diagnostics
        self.optimization = optimization
        self.output = output

    def build(self) -> dict[str, Any]:
        diagnostics = json.loads(self.diagnostics.read_text(encoding="utf-8"))
        optimization = json.loads(self.optimization.read_text(encoding="utf-8"))
        candidates = optimization.get("candidates", [])
        if not isinstance(candidates, list):
            raise TypeError("Optimization candidates must be a list.")
        proposals = [
            {
                "proposal_id": f"auto::{item.get('candidate_id')}",
                "candidate_id": item.get("candidate_id"),
                "status": "proposed",
                "approval_required": True,
                "autonomous_execution_enabled": False,
            }
            for item in candidates[:25]
            if isinstance(item, dict)
        ]
        report = {
            "diagnostic_count": diagnostics.get("diagnostic_count", 0),
            "proposals": proposals,
            "proposal_count": len(proposals),
            "mode": "advisory_only",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "autonomous-runtime-optimization.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
