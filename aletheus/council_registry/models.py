from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CouncilMember:
    member_id: str
    name: str
    role: str
    domain: str
    authority: str
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "role": self.role,
            "domain": self.domain,
            "authority": self.authority,
            "enabled": self.enabled,
            "metadata": self.metadata,
        }
