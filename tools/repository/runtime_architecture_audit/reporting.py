from __future__ import annotations

import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .models import AuditReport, CallSite, ImportEdge, RuntimeModule
from .tree import build_package_tree


def _relative_location(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _module_payload(
    module: RuntimeModule,
    repo_root: Path,
) -> dict[str, Any]:
    return {
        "name": module.name,
        "package": module.package,
        "path": _relative_location(module.path, repo_root),
        "relative_path": module.relative_path.as_posix(),
        "lines": module.lines,
        "size_bytes": module.size_bytes,
    }


def _edge_payload(edge: ImportEdge) -> dict[str, Any]:
    return asdict(edge)


def _call_site_payload(site: CallSite) -> dict[str, Any]:
    return asdict(site)


def build_report_payload(
    report: AuditReport,
    repo_root: Path,
) -> dict[str, Any]:
    modules_by_size = sorted(
        report.modules,
        key=lambda module: (-module.lines, module.name),
    )

    largest = modules_by_size[0] if modules_by_size else None
    total_lines = sum(module.lines for module in report.modules)
    average_lines = round(total_lines / len(report.modules), 2) if report.modules else 0

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "summary": {
            "module_count": len(report.modules),
            "total_lines": total_lines,
            "average_module_lines": average_lines,
            "largest_module": largest.name if largest else None,
            "largest_module_lines": largest.lines if largest else 0,
            "internal_import_edges": sum(edge.internal for edge in report.imports),
            "dependency_cycles": len(report.dependency_cycles),
            "orphan_modules": len(report.orphan_modules),
            "kernel_constructors": len(report.kernel_constructors),
            "boot_pipeline_paths": len(report.boot_pipeline_calls),
            "legacy_references": len(report.legacy_references),
            "errors": report.errors,
            "warnings": report.warnings,
            "infos": report.infos,
        },
        "health": asdict(report.health),
        "modules": [
            _module_payload(module, repo_root)
            for module in sorted(
                report.modules,
                key=lambda module: module.name,
            )
        ],
        "imports": [
            _edge_payload(edge)
            for edge in sorted(
                report.imports,
                key=lambda edge: (
                    edge.source,
                    edge.target,
                    edge.line,
                ),
            )
        ],
        "kernel_constructors": [
            _call_site_payload(site) for site in report.kernel_constructors
        ],
        "boot_pipeline_calls": [
            _call_site_payload(site) for site in report.boot_pipeline_calls
        ],
        "legacy_references": [
            _call_site_payload(site) for site in report.legacy_references
        ],
        "dependency_cycles": report.dependency_cycles,
        "orphan_modules": report.orphan_modules,
        "findings": [asdict(finding) for finding in report.sorted_findings()],
    }


def _render_call_sites(
    title: str,
    sites: list[CallSite],
) -> list[str]:
    lines = [
        f"## {title}",
        "",
    ]

    if not sites:
        lines.extend(["- None discovered.", ""])
        return lines

    for site in sites:
        lines.append(
            f"- `{site.relative_path}:{site.line}` — `{site.qualified_symbol}`"
        )

    lines.append("")
    return lines


def render_markdown(
    report: AuditReport,
    runtime_root: Path,
    payload: dict[str, Any],
) -> str:
    summary = payload["summary"]
    health = payload["health"]

    lines = [
        "# Runtime Architecture Audit",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "## Architecture Health",
        "",
        f"- Score: **{health['score']}/100**",
        f"- Grade: **{health['grade']}**",
        f"- Errors: **{summary['errors']}**",
        f"- Warnings: **{summary['warnings']}**",
        f"- Informational findings: **{summary['infos']}**",
        "",
        "### Score Deductions",
        "",
    ]

    deductions = health["deductions"]

    if any(deductions.values()):
        for category, deduction in deductions.items():
            lines.append(f"- {category.replace('_', ' ').title()}: -{deduction}")
    else:
        lines.append("- No deductions.")

    lines.extend(
        [
            "",
            "## Runtime Module Inventory",
            "",
            f"- Modules: **{summary['module_count']}**",
            f"- Total lines: **{summary['total_lines']}**",
            (f"- Average module size: **{summary['average_module_lines']} lines**"),
            (
                "- Largest module: "
                f"**{summary['largest_module']}** "
                f"({summary['largest_module_lines']} lines)"
            ),
            (f"- Internal import edges: **{summary['internal_import_edges']}**"),
            f"- Dependency cycles: **{summary['dependency_cycles']}**",
            f"- Orphan modules: **{summary['orphan_modules']}**",
            f"- Kernel constructors: **{summary['kernel_constructors']}**",
            f"- Boot pipeline paths: **{summary['boot_pipeline_paths']}**",
            f"- Legacy references: **{summary['legacy_references']}**",
            "",
            "## Runtime Package Tree",
            "",
            "```text",
            build_package_tree(runtime_root),
            "```",
            "",
        ]
    )

    lines.extend(
        _render_call_sites(
            "RuntimeKernel Construction",
            report.kernel_constructors,
        )
    )
    lines.extend(
        _render_call_sites(
            "Boot Pipeline Construction",
            report.boot_pipeline_calls,
        )
    )
    lines.extend(
        _render_call_sites(
            "Legacy Runtime References",
            report.legacy_references,
        )
    )

    lines.extend(
        [
            "## Dependency Cycles",
            "",
        ]
    )

    if report.dependency_cycles:
        for cycle in report.dependency_cycles:
            lines.append(f"- `{' → '.join(cycle)}`")
    else:
        lines.append("- No dependency cycles discovered.")

    lines.extend(
        [
            "",
            "## Orphan Modules",
            "",
        ]
    )

    if report.orphan_modules:
        for module_name in report.orphan_modules:
            lines.append(f"- `{module_name}`")
    else:
        lines.append("- No orphan modules discovered.")

    lines.extend(
        [
            "",
            "## Findings",
            "",
        ]
    )

    findings = report.sorted_findings()

    if findings:
        for finding in findings:
            location = f" — `{finding.location}`" if finding.location else ""
            lines.append(
                f"- **{finding.severity.upper()}** "
                f"`{finding.category}`: "
                f"{finding.message}{location}"
            )
    else:
        lines.append("- No findings.")

    lines.append("")

    return "\n".join(lines)


def write_reports(
    report: AuditReport,
    repo_root: Path,
    runtime_root: Path,
    output_root: Path,
) -> None:
    output_root.mkdir(parents=True, exist_ok=True)

    payload = build_report_payload(report, repo_root)

    json_path = output_root / "runtime-architecture-audit.json"
    markdown_path = output_root / "runtime-architecture-audit.md"

    json_path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    markdown_path.write_text(
        render_markdown(
            report=report,
            runtime_root=runtime_root,
            payload=payload,
        ),
        encoding="utf-8",
    )
