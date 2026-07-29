from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

Factory = Callable[[Any], Any]


@dataclass(frozen=True, slots=True)
class ManifestEntry:
    name: str
    kind: str
    factory: Factory
    version: str = "1.0.0"
    dependencies: tuple[str, ...] = field(default_factory=tuple)
    capabilities: tuple[str, ...] = field(default_factory=tuple)
    required: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)
