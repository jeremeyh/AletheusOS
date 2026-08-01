from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class Engine:
    def __init__(
        self,
        vertical: Path,
        horizontal: Path,
        access: Path,
        governance: Path,
        output: Path,
    ) -> None:
        self.vertical = vertical
        self.horizontal = horizontal
        self.access = access
        self.governance = governance
        self.output = output

    def build(self) -> dict[str, Any]:
        vertical = json.loads(self.vertical.read_text(encoding="utf-8"))
        horizontal = json.loads(self.horizontal.read_text(encoding="utf-8"))
        access = json.loads(self.access.read_text(encoding="utf-8"))
        governance = json.loads(self.governance.read_text(encoding="utf-8"))

        blockers = []
        warnings = []
        if not vertical.get("top_to_bottom_connected"):
            blockers.append("Top-to-bottom vertical continuity failed.")
        if not horizontal.get("horizontal_mesh_connected"):
            blockers.append("Horizontal Mesh continuity failed.")
        if access.get("access_module_count", 0) == 0:
            blockers.append("No access modules were realized.")
        if governance.get("decision") == "warn":
            warnings.append("Architectural Governance is in warn state.")
        if governance.get("decision") == "block":
            blockers.append("Architectural Governance is blocking.")

        decision = "block" if blockers else "warn" if warnings else "pass"
        report = {
            "generated_at": datetime.now(UTC).isoformat(),
            "decision": decision,
            "vertical_continuity": vertical.get("top_to_bottom_connected"),
            "horizontal_continuity": horizontal.get("horizontal_mesh_connected"),
            "access_modules": access.get("access_module_count", 0),
            "governance_decision": governance.get("decision", "unknown"),
            "blockers": blockers,
            "warnings": warnings,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "full-platform-continuity-gate.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
