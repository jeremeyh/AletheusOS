from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .finding import FindingSet


@dataclass(slots=True)
class SPANReport:
    project_root: str
    profile: str
    findings: FindingSet
    metadata: dict[str, Any]

    def summary(self) -> dict[str, Any]:
        return {
            "project_root": self.project_root,
            "profile": self.profile,
            **self.findings.summary(),
            "metadata": self.metadata,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "findings": [finding.to_dict() for finding in self.findings],
        }

    def to_json(self, *, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)

    def to_markdown(self) -> str:
        summary = self.summary()
        lines = [
            "# SPAN Constitutional Intelligence Report",
            "",
            f"- Project: `{self.project_root}`",
            f"- Profile: `{self.profile}`",
            f"- Findings: **{summary['total']}**",
            "",
            "## Severity Summary",
            "",
        ]
        for severity, count in summary["by_severity"].items():
            lines.append(f"- {severity}: {count}")

        lines.extend(["", "## Findings", ""])
        if not self.findings:
            lines.append("No findings.")
        else:
            for finding in self.findings:
                lines.extend(
                    [
                        f"### {finding.id} — {finding.title}",
                        "",
                        f"- Category: `{finding.category}`",
                        f"- Severity: `{finding.severity.value}`",
                        f"- Confidence: `{finding.confidence:.2f}`",
                        "",
                        finding.description,
                        "",
                        f"**Recommendation:** {finding.recommendation or 'Review the supporting evidence.'}",
                        "",
                    ]
                )
        return "\n".join(lines)

    def write(self, path: str | Path) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.suffix.lower() == ".json":
            output.write_text(self.to_json() + "\n", encoding="utf-8")
        else:
            output.write_text(self.to_markdown() + "\n", encoding="utf-8")
        return output
