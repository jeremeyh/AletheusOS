from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class AutonomyMode(StrEnum):
    OBSERVE = "OBSERVE"
    ADVISE = "ADVISE"
    PREPARE = "PREPARE"
    EXECUTE_WITH_APPROVAL = "EXECUTE_WITH_APPROVAL"


class DecisionState(StrEnum):
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True, slots=True)
class CollectorPolicy:
    max_transaction_value: float = 500.0
    max_daily_commitment: float = 1000.0
    require_human_approval: bool = True
    allowed_markets: tuple[str, ...] = ()
    prohibited_assets: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Mission:
    mission_id: str
    objective: str
    budget: float
    mode: AutonomyMode = AutonomyMode.ADVISE
    constraints: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Opportunity:
    opportunity_id: str
    asset_id: str
    market: str
    asking_price: float
    estimated_value: float
    confidence: float
    evidence_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
