from __future__ import annotations

import json
from pathlib import Path

from .models import ExecutionResult, RepairPlan, ScanManifest


class RepairReporter:
    def __init__(self, report_root: Path) -> None:
        self.report_root = report_root

    def write(
        self,
        target: ScanManifest,
        plan: RepairPlan,
        result: ExecutionResult | None = None,
    ) -> Path:
        self.report_root.mkdir(parents=True, exist_ok=True)
        (self.report_root / "target_manifest.json").write_text(
            json.dumps(target.to_dict(), indent=2), encoding="utf-8"
        )
        (self.report_root / "repair_plan.json").write_text(
            json.dumps(plan.to_dict(), indent=2), encoding="utf-8"
        )
        if result:
            (self.report_root / "execution_result.json").write_text(
                json.dumps(result.to_dict(), indent=2), encoding="utf-8"
            )
        summary = [
            "# Repository Self-Repair Report",
            "",
            f"Target: `{plan.target_root}`",
            f"Source: `{plan.source_root or 'none'}`",
            "",
            "## Plan counts",
            "",
        ]
        summary.extend(
            f"- {name}: **{count}**" for name, count in sorted(plan.counts().items())
        )
        conflicts = [a for a in plan.actions if a.kind.value == "conflict"]
        if conflicts:
            summary.extend(["", "## Conflicts requiring review", ""])
            summary.extend(f"- `{action.relative_path}`" for action in conflicts)
        if result:
            summary.extend(
                [
                    "",
                    "## Execution",
                    "",
                    f"- Dry run: **{result.dry_run}**",
                    f"- Success: **{result.success}**",
                    f"- Applied: **{len(result.applied)}**",
                    f"- Failed: **{len(result.failed)}**",
                ]
            )
            if result.archive_path:
                summary.append(f"- Archive: `{result.archive_path}`")
        path = self.report_root / "summary.md"
        path.write_text("\n".join(summary) + "\n", encoding="utf-8")
        return path
