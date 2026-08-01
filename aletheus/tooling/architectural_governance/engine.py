from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class GovernanceEngine:
    def __init__(
        self,
        authority: Path,
        boundary: Path,
        health: Path,
        registry: Path,
        output: Path,
    ) -> None:
        self.paths = {
            "authority": authority,
            "boundary": boundary,
            "health": health,
            "registry": registry,
        }
        self.output = output

    def evaluate(self) -> dict[str, Any]:
        loaded = {
            name: json.loads(path.read_text(encoding="utf-8"))
            for name, path in self.paths.items()
        }
        findings: list[dict[str, Any]] = []

        for item in loaded["authority"].get("findings", []):
            if isinstance(item, dict):
                findings.append({"source": "authority", **item})

        for item in loaded["boundary"].get("findings", []):
            if isinstance(item, dict):
                findings.append({"source": "boundary", **item})

        readiness = str(loaded["health"].get("readiness", "unknown"))
        if readiness == "not_ready":
            findings.append(
                {
                    "source": "health",
                    "code": "PLATFORM_NOT_READY",
                    "severity": "high",
                    "message": "Constitutional readiness is not_ready.",
                }
            )

        critical = sum(item.get("severity") == "critical" for item in findings)
        high = sum(item.get("severity") == "high" for item in findings)
        decision = "block" if critical else "warn" if high else "pass"

        report = {
            "generated_at": datetime.now(UTC).isoformat(),
            "decision": decision,
            "findings": findings,
            "critical": critical,
            "high": high,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "governance-findings.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        (self.output / "policy-violations.json").write_text(
            json.dumps({"violations": findings}, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        (self.output / "governance-summary.md").write_text(
            "# Architectural Governance\n\n"
            f"- Decision: **{decision}**\n"
            f"- Critical: **{critical}**\n"
            f"- High: **{high}**\n",
            encoding="utf-8",
        )
        return report
