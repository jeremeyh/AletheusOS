"""Domain models for Kinekt™ repository intelligence."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class DefinitionRecord:
    module: str
    path: str
    kind: str
    name: str
    qualified_name: str
    line: int
    end_line: int
    fingerprint: str
    has_docstring: bool
    statement_count: int
    branch_count: int


@dataclass(frozen=True, slots=True)
class ModuleRecord:
    module: str
    path: str
    package: str
    owner: str
    lines: int
    imports: tuple[str, ...]
    definitions: tuple[DefinitionRecord, ...]
    syntax_valid: bool = True


@dataclass(frozen=True, slots=True)
class Finding:
    code: str
    severity: str
    subject: str
    message: str
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class PackageMetric:
    package: str
    modules: int
    definitions: int
    lines: int
    internal_fan_in: int
    internal_fan_out: int
    orphan_candidates: int
    duplicate_definitions: int
    boundary_findings: int
    health_score: int


@dataclass(slots=True)
class AnalysisResult:
    root: str
    generated_at: str
    modules: list[ModuleRecord] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    package_metrics: list[PackageMetric] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def definition_count(self) -> int:
        return sum(len(module.definitions) for module in self.modules)
