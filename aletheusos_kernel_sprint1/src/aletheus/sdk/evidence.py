from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True,slots=True)
class Evidence:
    claim:str
    source:str
    confidence:float
    data:dict[str,Any]=field(default_factory=dict)
    id:UUID=field(default_factory=uuid4)
    observed_at:datetime=field(default_factory=lambda:datetime.now(UTC))
    def __post_init__(self):
        if not 0<=self.confidence<=1: raise ValueError("Evidence confidence must be between 0.0 and 1.0.")
        if not self.claim.strip() or not self.source.strip(): raise ValueError("Evidence requires claim and source.")
