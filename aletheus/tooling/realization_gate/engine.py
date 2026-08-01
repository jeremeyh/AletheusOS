from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class RealizationGateEngine:
    def __init__(
        self,
        ledger: Path,
        catalog: Path,
        mesh: Path,
        governance: Path,
        output: Path,
    ) -> None:
        self.paths = {
            "ledger": ledger,
            "catalog": catalog,
            "mesh": mesh,
            "governance": governance,
        }
        self.output = output

    def evaluate(self) -> dict[str, Any]:
        loaded = {
            name: json.loads(path.read_text(encoding="utf-8"))
            for name, path in self.paths.items()
        }
        ledger_entries = loaded["ledger"].get("entries", [])
        catalog_entries = loaded["catalog"].get("entries", [])
        disconnected = loaded["mesh"].get("disconnected", [])
        missing_targets = loaded["mesh"].get("missing_targets", [])
        governance_decision = loaded["governance"].get("decision", "unknown")

        realized = sum(
            isinstance(item, dict) and bool(item.get("realized"))
            for item in ledger_entries
        )
        total_ledger = len(ledger_entries) if isinstance(ledger_entries, list) else 0
        total_catalog = len(catalog_entries) if isinstance(catalog_entries, list) else 0

        blockers: list[str] = []
        warnings: list[str] = []

        if governance_decision == "block":
            blockers.append("Architectural Governance decision is block.")
        if total_catalog < total_ledger:
            blockers.append("Expanded catalog contains fewer entries than the ledger.")
        if missing_targets:
            warnings.append(f"{len(missing_targets)} Mesh targets are undeclared.")
        if disconnected:
            warnings.append(f"{len(disconnected)} catalog entries are disconnected.")
        if total_ledger and realized / total_ledger < 0.75:
            warnings.append("Ledger realization is below 75%.")

        decision = "block" if blockers else "warn" if warnings else "pass"
        report = {
            "generated_at": datetime.now(UTC).isoformat(),
            "decision": decision,
            "ledger_entries": total_ledger,
            "ledger_realized": realized,
            "catalog_entries": total_catalog,
            "disconnected": len(disconnected),
            "missing_targets": len(missing_targets),
            "governance_decision": governance_decision,
            "blockers": blockers,
            "warnings": warnings,
        }

        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "ecosystem-realization-gate.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        (self.output / "realization-readiness.md").write_text(
            "# Ecosystem Realization Gate\n\n"
            f"- Decision: **{decision}**\n"
            f"- Ledger realized: **{realized}/{total_ledger}**\n"
            f"- Catalog entries: **{total_catalog}**\n"
            f"- Disconnected: **{len(disconnected)}**\n"
            f"- Missing targets: **{len(missing_targets)}**\n",
            encoding="utf-8",
        )
        return report
