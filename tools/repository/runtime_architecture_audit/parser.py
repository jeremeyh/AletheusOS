from __future__ import annotations

import ast

from .models import AuditReport, ParsedRuntimeModule, RuntimeModule


def parse_runtime_module(module: RuntimeModule) -> ParsedRuntimeModule:
    """Parse one runtime module into an AST."""

    source = module.path.read_text(encoding="utf-8", errors="replace")

    try:
        tree = ast.parse(
            source,
            filename=str(module.path),
            type_comments=True,
        )
    except SyntaxError as exc:
        message = f"{exc.msg} at line {exc.lineno}, column {exc.offset}"
        return ParsedRuntimeModule(
            module=module,
            tree=None,
            syntax_error=message,
        )

    return ParsedRuntimeModule(
        module=module,
        tree=tree,
    )


def parse_runtime_modules(
    modules: list[RuntimeModule],
    report: AuditReport,
) -> list[ParsedRuntimeModule]:
    """Parse all discovered modules and record syntax failures."""

    parsed_modules: list[ParsedRuntimeModule] = []

    for module in modules:
        parsed = parse_runtime_module(module)
        parsed_modules.append(parsed)

        if parsed.syntax_error:
            report.add_finding(
                "error",
                "syntax",
                f"Unable to parse module: {parsed.syntax_error}",
                str(module.relative_path),
                module=module.name,
            )

    return parsed_modules
