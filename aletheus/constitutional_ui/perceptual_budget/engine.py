from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Cost:
    node_id: str
    priority: float
    visual: float
    motion: float
    depth: float
    interaction: float
    audio: float
    haptic: float

    @property
    def total(self) -> float:
        return (
            self.visual
            + self.motion
            + self.depth
            + self.interaction
            + self.audio
            + self.haptic
        )


class Engine:
    def allocate(self, costs: tuple[Cost, ...], budget: float) -> dict[str, object]:
        selected = []
        ambient = []
        consumed = 0.0
        for item in sorted(costs, key=lambda x: (x.priority, -x.total), reverse=True):
            if consumed + item.total <= budget:
                selected.append(item.node_id)
                consumed += item.total
            else:
                ambient.append(item.node_id)
        return {
            "budget": budget,
            "consumed": consumed,
            "selected": selected,
            "ambientCollapsed": ambient,
            "withinBudget": consumed <= budget,
        }
