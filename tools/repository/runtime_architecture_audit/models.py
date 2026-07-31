from __future__ import annotations

import ast
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SEVERITY_ORDER = {
    "error": 0,
    "warning": 1,
    "info": 2,
}


@dataclass(slots=True)
class RuntimeModule:
    """Filesystem-level information about one Python runtime module."""

    name: str
    path: Path
    relative_path: Path
    package: str
    lines: int
    size_bytes: int


@dataclass(slots=True)
class ParsedRuntimeModule:
    """Runtime module and its parsed Python syntax tree."""

    module: RuntimeModule
    tree: ast.Module | None
    syntax_error: str | None = None


@dataclass(slots=True, frozen=True)
class ImportEdge:
    """Directed import relationship between runtime modules."""

    source: str
    target: str
    line: int
    imported_name: str
    internal: bool


@dataclass(slots=True, frozen=True)
class CallSite:
    """Location of a function call or object construction."""

    module: str
    relative_path: str
    line: int
    column: int
    symbol: str
    qualified_symbol: str


@dataclass(slots=True)
class AuditFinding:
    """One architecture audit observation."""

    severity: str
    category: str
    message: str
    location: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ArchitectureHealth:
    """Computed architecture health summary."""

    score: int = 100
    grade: str = "A"
    deductions: dict[str, int] = field(default_factory=dict)
    metrics: dict[str, int | float | str | None] = field(default_factory=dict)


@dataclass(slots=True)
class AuditReport:
    """Complete result of a runtime architecture audit."""

    modules: list[RuntimeModule] = field(default_factory=list)
    parsed_modules: list[ParsedRuntimeModule] = field(default_factory=list)
    imports: list[ImportEdge] = field(default_factory=list)
    kernel_constructors: list[CallSite] = field(default_factory=list)
    boot_pipeline_calls: list[CallSite] = field(default_factory=list)
    legacy_references: list[CallSite] = field(default_factory=list)
    dependency_cycles: list[list[str]] = field(default_factory=list)
    orphan_modules: list[str] = field(default_factory=list)
    findings: list[AuditFinding] = field(default_factory=list)
    health: ArchitectureHealth = field(default_factory=ArchitectureHealth)

    @property
    def errors(self) -> int:
        return sum(finding.severity == "error" for finding in self.findings)

    @property
    def warnings(self) -> int:
        return sum(finding.severity == "warning" for finding in self.findings)

    @property
    def infos(self) -> int:
        return sum(finding.severity == "info" for finding in self.findings)

    def add_finding(
        self,
        severity: str,
        category: str,
        message: str,
        location: str | None = None,
        **metadata: Any,
    ) -> None:
        if severity not in SEVERITY_ORDER:
            raise ValueError(f"Unsupported finding severity: {severity}")

        self.findings.append(
            AuditFinding(
                severity=severity,
                category=category,
                message=message,
                location=location,
                metadata=metadata,
            )
        )

    def sorted_findings(self) -> list[AuditFinding]:
        return sorted(
            self.findings,
            key=lambda finding: (
                SEVERITY_ORDER.get(finding.severity, 99),
                finding.category,
                finding.location or "",
                finding.message,
            ),
        )
