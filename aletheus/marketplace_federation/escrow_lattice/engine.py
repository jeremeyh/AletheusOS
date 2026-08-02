from __future__ import annotations

from typing import ClassVar


class Engine:
    TRANSITIONS: ClassVar[dict[str, frozenset[str]]] = {
        "CREATED": frozenset({"FUNDED", "CANCELLED"}),
        "FUNDED": frozenset({"LOCKED", "CANCELLED"}),
        "LOCKED": frozenset({"VERIFIED", "CANCELLED"}),
        "VERIFIED": frozenset({"RELEASE_AUTHORIZED"}),
        "RELEASE_AUTHORIZED": frozenset({"SETTLED"}),
        "SETTLED": frozenset(),
        "CANCELLED": frozenset(),
    }

    def transition(self, current: str, target: str) -> str:
        if target not in self.TRANSITIONS[current]:
            raise ValueError("invalid escrow transition")
        return target
