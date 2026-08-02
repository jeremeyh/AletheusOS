from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class VerificationState(str, Enum):
    NEBULAR_PROBABILITY = "NEBULAR_PROBABILITY"
    CRYSTALLINE_SOLID = "CRYSTALLINE_SOLID"


@dataclass(frozen=True)
class Money:
    amount: float
    currency: str


@dataclass(frozen=True)
class Asset:
    asset_id: str
    title: str
    owner_id: str
    declared_value: float
    verified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Request:
    request_id: str
    actor_id: str
    payload: dict[str, Any] = field(default_factory=dict)
