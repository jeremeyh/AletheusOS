from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class DecisionEnvelope:
    stage: str
    payload: dict[str, Any] = field(default_factory=dict)
    human_authority_required: bool = True
    execution_authorized: bool = False
