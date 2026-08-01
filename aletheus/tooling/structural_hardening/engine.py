from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(
        self,
        roots: Path,
        cycles: Path,
        continuity: Path,
        output: Path,
    ) -> None:
        self.roots = roots
        self.cycles = cycles
        self.continuity = continuity
        self.output = output

    def build(self) -> dict[str, Any]:
        roots = json.loads(self.roots.read_text(encoding="utf-8"))
        cycles = json.loads(self.cycles.read_text(encoding="utf-8"))
        continuity = json.loads(self.continuity.read_text(encoding="utf-8"))

        braces = []
        for root in roots.get("ambiguous_roots", []):
            braces.append(
                {
                    "brace_id": f"root::{root}",
                    "subject": root,
                    "action": "require_semantic_parent_or_explicit_root_declaration",
                    "priority": "high",
                }
            )
        for cycle in cycles.get("unclassified_cycles", []):
            members = cycle.get("members", [])
            braces.append(
                {
                    "brace_id": "cycle::" + "::".join(str(item) for item in members),
                    "subject": members,
                    "action": "require_feedback_contract_and_termination_condition",
                    "priority": "high",
                }
            )
        if continuity.get("decision") == "warn":
            braces.append(
                {
                    "brace_id": "continuity::warning",
                    "subject": "platform_continuity",
                    "action": "preserve_current_routes_and_close_semantic_gaps",
                    "priority": "medium",
                }
            )

        report = {
            "braces": braces,
            "brace_count": len(braces),
            "temporary_scaffolds_allowed": False,
            "parallel_layer_created": False,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "structural-brace-plan.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
