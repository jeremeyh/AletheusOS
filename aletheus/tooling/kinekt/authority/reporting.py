import json
from pathlib import Path

from .models import AuthorityReport


def write_reports(report: AuthorityReport, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "capability-authority-map.json").write_text(
        json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8"
    )
    contracts = {
        c.name: {
            "runtime_role": c.runtime_role,
            "consumes": list(c.consumes),
            "produces": list(c.produces),
            "delegates_to": list(c.delegates_to),
            "must_not_own": list(c.must_not_own),
        }
        for c in report.capabilities
    }
    (output / "integration-contracts.json").write_text(
        json.dumps(contracts, indent=2, sort_keys=True), encoding="utf-8"
    )
    lines = [
        "# AletheusOS™ Capability Authority Map",
        "",
        f"- Capabilities: **{len(report.capabilities)}**",
        f"- Assigned modules: **{len(report.module_assignments)}**",
        f"- Unresolved modules: **{len(report.unresolved_modules)}**",
        f"- Findings: **{len(report.findings)}**",
        "",
    ]
    for c in report.capabilities:
        lines += [
            f"## {c.name}",
            "",
            f"- Runtime role: `{c.runtime_role}`",
            f"- Owns: {'; '.join(c.owns)}",
            f"- Delegates to: {'; '.join(c.delegates_to) or 'none'}",
            f"- Must not own: {'; '.join(c.must_not_own)}",
            "",
        ]
    (output / "capability-authority-map.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
