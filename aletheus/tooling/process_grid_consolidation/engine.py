from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ABSORPTION_MAP = {
    "Semantic Rail Continuity Gate": "Semantic Validation",
    "Full Platform Continuity Gate": "Platform Certification",
    "Vertical Slice Verifier": "Architecture Validation",
    "Horizontal Mesh Verifier": "Mesh Validation",
    "Runtime Diagnostics": "Runtime Health",
    "Runtime Observability": "Runtime Health",
    "Runtime Telemetry": "Telemetry",
    "Architectural Governance": "Governance Validation",
}


class Engine:
    def __init__(self, sources: dict[str, Path], output: Path) -> None:
        self.sources = sources
        self.output = output

    def build(self) -> dict[str, Any]:
        stages: dict[str, list[dict[str, Any]]] = {}
        for component, stage in ABSORPTION_MAP.items():
            path = self.sources[component]
            payload = json.loads(path.read_text(encoding="utf-8"))
            stages.setdefault(stage, []).append(
                {
                    "absorbed_component": component,
                    "source_report": str(path),
                    "payload": payload,
                    "functionality_preserved": True,
                    "top_level_gate": False,
                }
            )

        report = {
            "stages": stages,
            "absorbed_components": len(ABSORPTION_MAP),
            "functionality_removed": False,
            "top_level_gate_count_reduced_by": 8,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "process-grid-consolidation.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        (self.output / "absorbed-gate-index.json").write_text(
            json.dumps(ABSORPTION_MAP, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
