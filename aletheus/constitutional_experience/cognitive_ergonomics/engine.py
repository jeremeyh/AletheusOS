from ..helpers import clamp


class Engine:
    def density(self, urgency: float, intent: float, load: float) -> float:
        return clamp(
            (0.55 * clamp(urgency) + 0.45 * clamp(intent)) / (1 + 1.5 * clamp(load)),
            0.15,
            1.0,
        )
