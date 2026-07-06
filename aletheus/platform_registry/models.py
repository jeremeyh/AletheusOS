from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PlatformComponentRecord:
    component_id: str
    name: str
    version: str = "0.1.0"
    genesis: str = "unknown"
    status: str = "registered"
    critical: bool = False
    dependencies: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
