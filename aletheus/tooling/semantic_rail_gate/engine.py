from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class Engine:
    def __init__(
        self, roots: Path, rails: Path, forks: Path, continuity: Path, output: Path
    ) -> None:
        self.roots = roots
        self.rails = rails
        self.forks = forks
        self.continuity = continuity
        self.output = output

    def build(self) -> dict[str, Any]:
        roots = json.loads(self.roots.read_text(encoding="utf-8"))
        rails = json.loads(self.rails.read_text(encoding="utf-8"))
        forks = json.loads(self.forks.read_text(encoding="utf-8"))
        continuity = json.loads(self.continuity.read_text(encoding="utf-8"))

        blockers = []
        warnings = []
        if roots.get("unresolved_roots"):
            blockers.append("Root ambiguity remains.")
        if not rails.get("parallel_in_out_enabled"):
            blockers.append("Parallel in/out rails are not enabled.")
        if continuity.get("decision") == "block":
            blockers.append("Platform continuity is blocking.")
        elif continuity.get("decision") == "warn":
            warnings.append("Platform continuity remains in warn state.")

        decision = "block" if blockers else "warn" if warnings else "pass"
        report = {
            "generated_at": datetime.now(UTC).isoformat(),
            "decision": decision,
            "resolved_roots": roots.get("resolved_count", 0),
            "parallel_rails": rails.get("paired_rails", 0),
            "forked_claims": forks.get("fork_count", 0),
            "blockers": blockers,
            "warnings": warnings,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "semantic-rail-continuity-gate.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
