from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class PrimitiveDefinition:
    name: str
    layer: str
    purpose: str
    props: tuple[str, ...] = ()
    reserved: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    findings: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {"valid": self.valid, "findings": list(self.findings)}
