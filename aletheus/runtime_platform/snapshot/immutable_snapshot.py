from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ImmutableRuntimeSnapshot:
    topology: Any

    providers: dict

    health: Any

    diagnostics: dict

    version: str
