from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class BrainState:
    name: str
    active: bool = True
    changed_at: str = datetime.now(UTC).isoformat()
