from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class Engine:
    def __init__(
        self,
        spartan: Path,
        observability: Path,
        diagnostics: Path,
        governance: Path,
        output: Path,
    ) -> None:
        self.spartan = spartan
        self.observability = observability
        self.diagnostics = diagnostics
        self.governance = governance
        self.output = output

    def build(self) -> dict[str, Any]:
        spartan = json.loads(self.spartan.read_text(encoding="utf-8"))
        observability = json.loads(self.observability.read_text(encoding="utf-8"))
        diagnostics = json.loads(self.diagnostics.read_text(encoding="utf-8"))
        governance = json.loads(self.governance.read_text(encoding="utf-8"))

        report = {
            "generated_at": datetime.now(UTC).isoformat(),
            "authority": "Sentinel",
            "runtime_role": "operational_security_command",
            "spartan_mode": spartan.get("integration_mode"),
            "readiness": observability.get("readiness", "unknown"),
            "diagnostics": diagnostics.get("diagnostics", []),
            "governance_decision": governance.get("decision", "unknown"),
            "response_mode": "approval_gated",
            "autonomous_response_enabled": False,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "sentinel-platform-runtime.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
