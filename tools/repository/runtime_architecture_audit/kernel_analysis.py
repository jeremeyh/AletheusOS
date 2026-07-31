from __future__ import annotations

import ast

from .ast_utils import dotted_name, final_symbol
from .models import AuditReport, CallSite

KERNEL_SYMBOL = "RuntimeKernel"

SANCTIONED_KERNEL_CONSTRUCTION_PATHS = {
    "aletheus/runtime/composition/root.py",
}


def analyze_kernel_construction(report: AuditReport) -> None:
    """Find RuntimeKernel constructor calls and validate ownership."""

    sites: list[CallSite] = []

    for parsed in report.parsed_modules:
        if parsed.tree is None:
            continue

        for node in ast.walk(parsed.tree):
            if not isinstance(node, ast.Call):
                continue

            qualified_symbol = dotted_name(node.func)

            if final_symbol(qualified_symbol) != KERNEL_SYMBOL:
                continue

            relative_path = parsed.module.relative_path.as_posix()

            site = CallSite(
                module=parsed.module.name,
                relative_path=relative_path,
                line=node.lineno,
                column=node.col_offset,
                symbol=KERNEL_SYMBOL,
                qualified_symbol=qualified_symbol or KERNEL_SYMBOL,
            )
            sites.append(site)

            location = f"{relative_path}:{node.lineno}"

            if relative_path not in SANCTIONED_KERNEL_CONSTRUCTION_PATHS:
                report.add_finding(
                    "error",
                    "kernel_ownership",
                    "RuntimeKernel is constructed outside the composition root.",
                    location,
                    symbol=qualified_symbol,
                )

    report.kernel_constructors = sorted(
        sites,
        key=lambda site: (site.relative_path, site.line, site.column),
    )

    if not sites:
        report.add_finding(
            "warning",
            "kernel_ownership",
            "No RuntimeKernel construction site was discovered.",
        )
