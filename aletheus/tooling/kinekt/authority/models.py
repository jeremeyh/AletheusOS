from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class CapabilityAuthority:
    name: str
    runtime_role: str
    module_prefixes: tuple[str, ...]
    owns: tuple[str, ...]
    consumes: tuple[str, ...]
    produces: tuple[str, ...]
    delegates_to: tuple[str, ...]
    must_not_own: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AuthorityFinding:
    code: str
    severity: str
    subject: str
    message: str
    evidence: tuple[str, ...] = ()


@dataclass(slots=True)
class AuthorityReport:
    generated_at: str
    registry_path: str
    twin_path: str
    capabilities: list[CapabilityAuthority] = field(default_factory=list)
    module_assignments: dict[str, str] = field(default_factory=dict)
    findings: list[AuthorityFinding] = field(default_factory=list)
    unresolved_modules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
