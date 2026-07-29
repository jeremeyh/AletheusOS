from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class RuntimeCapability:
    name: str
    provider: str
    version: str = "1.0.0"
    metadata: Mapping[str, Any] = field(default_factory=dict)
