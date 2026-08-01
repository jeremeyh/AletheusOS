from __future__ import annotations

from dataclasses import dataclass

from .models import ConstitutionalState


@dataclass(frozen=True)
class Potential:
    potential_id: str
    intent: str
    state: ConstitutionalState
    primitives: tuple[str, ...]
    constraints: tuple[str, ...] = ()


class Engine:
    def evaluate(self, p: Potential) -> dict[str, object]:
        s = p.state.bounded()
        ready = s.consensus >= 0.60 and s.confidence >= 0.50 and bool(p.primitives)
        return {
            "potentialId": p.potential_id,
            "intent": p.intent,
            "manifestable": ready,
            "constraints": list(p.constraints),
        }
