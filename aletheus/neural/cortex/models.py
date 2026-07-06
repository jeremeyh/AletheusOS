from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Cortex:
    id: str
    name: str
    role: str
    status: str = "inactive"
    metadata: dict[str, Any] = field(default_factory=dict)
