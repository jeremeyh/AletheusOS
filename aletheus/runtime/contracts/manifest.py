from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True, slots=True)
class ComponentManifest:
    """Immutable description of a runtime component."""

    component_id: str
    name: str
    version: str
    responsibility: str
    provides: FrozenSet[str] = field(default_factory=frozenset)
    requires: FrozenSet[str] = field(default_factory=frozenset)
    constitutional_tags: FrozenSet[str] = field(default_factory=frozenset)

    def __post_init__(self) -> None:
        if not self.component_id.strip():
            raise ValueError("component_id must not be empty")

        if not self.name.strip():
            raise ValueError("name must not be empty")

        if not self.version.strip():
            raise ValueError("version must not be empty")

        if not self.responsibility.strip():
            raise ValueError("responsibility must not be empty")
