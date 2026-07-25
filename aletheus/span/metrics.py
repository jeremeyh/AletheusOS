from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class Metric:
    name:str
    subject:str
    value:float
    category:str="general"
    unit:str=""
    metadata:dict[str,Any]=field(default_factory=dict)
    timestamp:datetime=field(default_factory=lambda: datetime.now(UTC))
