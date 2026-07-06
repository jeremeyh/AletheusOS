from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class IntelligenceEngine:

    engine_id: str
    name: str
    version: str
    category: str
    foundation_engine: str

    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):

        return {
            "engine_id": self.engine_id,
            "name": self.name,
            "version": self.version,
            "category": self.category,
            "foundation_engine": self.foundation_engine,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }
