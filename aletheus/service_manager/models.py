from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ServiceRegistration:
    service_id: str
    name: str
    version: str = "0.1.0"
    status: str = "registered"
    priority: int = 100
    critical: bool = False
    dependencies: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
