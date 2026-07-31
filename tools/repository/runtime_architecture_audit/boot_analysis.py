from __future__ import annotations

import ast

from .ast_utils import dotted_name, final_symbol
from .models import AuditReport, CallSite

BOOT_PIPELINE_BUILDER = "build_runtime_boot_pipeline"

SANCTIONED_BOOT_PIPELINE_PATHS = {
    "aletheus/runtime/composition/root.py",
    "aletheus/runtime/core.py",
    "aletheus/runtime/boot_pipeline/default_pipeline.py",
}


def analyze_boot_pipeline(report: AuditReport) -> None:
    """Find boot-pipeline builder calls and validate sanctioned locations."""

    sites: list[CallSite] = []

    for parsed in report.parsed_modules:
        if parsed.tree is None:
            continue

        for node in ast.walk(parsed.tree):
            if not isinstance(node, ast.Call):
                continue

            qualified_symbol = dotted_name(node.func)

            if final_symbol(qualified_symbol) != BOOT_PIPELINE_BUILDER:
                continue

            relative_path = parsed.module.relative_path.as_posix()

            site = CallSite(
                module=parsed.module.name,
                relative_path=relative_path,
                line=node.lineno,
                column=node.col_offset,
                symbol=BOOT_PIPELINE_BUILDER,
                qualified_symbol=qualified_symbol or BOOT_PIPELINE_BUILDER,
            )
            sites.append(site)

            if relative_path not in SANCTIONED_BOOT_PIPELINE_PATHS:
                report.add_finding(
                    "error",
                    "boot_pipeline_ownership",
                    "Boot pipeline is assembled outside a sanctioned path.",
                    f"{relative_path}:{node.lineno}",
                    symbol=qualified_symbol,
                )

    report.boot_pipeline_calls = sorted(
        sites,
        key=lambda site: (site.relative_path, site.line, site.column),
    )

    if not sites:
        report.add_finding(
            "warning",
            "boot_pipeline",
            "No runtime boot-pipeline construction call was discovered.",
        )
    elif len(sites) > 1:
        report.add_finding(
            "warning",
            "boot_pipeline",
            f"Multiple runtime boot-pipeline paths remain active ({len(sites)}).",
            paths=[site.relative_path for site in sites],
        )
