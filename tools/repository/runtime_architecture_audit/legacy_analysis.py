from __future__ import annotations

import ast

from .ast_utils import dotted_name, final_symbol
from .models import AuditReport, CallSite

RETIRED_SYMBOLS = {
    "RuntimeCoreShim",
    "CoreLifecycleBridge",
    "RuntimeMigrationBridge",
    "MigrationBridge",
}

RETIRED_MODULE_SEGMENTS = {
    "core_shim",
    "core_bridge",
}


def _record_reference(
    report: AuditReport,
    parsed_module_name: str,
    relative_path: str,
    node: ast.AST,
    symbol: str,
    qualified_symbol: str,
) -> CallSite:
    line = getattr(node, "lineno", 0)
    column = getattr(node, "col_offset", 0)

    site = CallSite(
        module=parsed_module_name,
        relative_path=relative_path,
        line=line,
        column=column,
        symbol=symbol,
        qualified_symbol=qualified_symbol,
    )

    report.add_finding(
        "error",
        "legacy_runtime",
        f"Retired runtime concept referenced: {qualified_symbol}",
        f"{relative_path}:{line}",
        symbol=symbol,
    )

    return site


def analyze_legacy_references(report: AuditReport) -> None:
    """Detect references to retired runtime bridge and shim concepts."""

    sites: list[CallSite] = []
    seen: set[tuple[str, int, str]] = set()

    for parsed in report.parsed_modules:
        if parsed.tree is None:
            continue

        relative_path = parsed.module.relative_path.as_posix()

        for node in ast.walk(parsed.tree):
            qualified_symbol: str | None = None

            if isinstance(node, (ast.Name, ast.Attribute)):
                qualified_symbol = dotted_name(node)

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    segments = set(alias.name.split("."))

                    if segments & RETIRED_MODULE_SEGMENTS:
                        key = (relative_path, node.lineno, alias.name)

                        if key not in seen:
                            seen.add(key)
                            sites.append(
                                _record_reference(
                                    report,
                                    parsed.module.name,
                                    relative_path,
                                    node,
                                    final_symbol(alias.name) or alias.name,
                                    alias.name,
                                )
                            )

                continue

            elif isinstance(node, ast.ImportFrom):
                imported_module = node.module or ""
                module_segments = set(imported_module.split("."))

                for alias in node.names:
                    full_name = ".".join(
                        part for part in (imported_module, alias.name) if part
                    )
                    symbol = alias.name

                    if (
                        symbol in RETIRED_SYMBOLS
                        or module_segments & RETIRED_MODULE_SEGMENTS
                    ):
                        key = (relative_path, node.lineno, full_name)

                        if key not in seen:
                            seen.add(key)
                            sites.append(
                                _record_reference(
                                    report,
                                    parsed.module.name,
                                    relative_path,
                                    node,
                                    symbol,
                                    full_name,
                                )
                            )

                continue

            if not qualified_symbol:
                continue

            symbol = final_symbol(qualified_symbol)
            segments = set(qualified_symbol.split("."))

            if symbol not in RETIRED_SYMBOLS and not segments & RETIRED_MODULE_SEGMENTS:
                continue

            key = (
                relative_path,
                getattr(node, "lineno", 0),
                qualified_symbol,
            )

            if key in seen:
                continue

            seen.add(key)
            sites.append(
                _record_reference(
                    report,
                    parsed.module.name,
                    relative_path,
                    node,
                    symbol or qualified_symbol,
                    qualified_symbol,
                )
            )

    report.legacy_references = sorted(
        sites,
        key=lambda site: (
            site.relative_path,
            site.line,
            site.qualified_symbol,
        ),
    )
