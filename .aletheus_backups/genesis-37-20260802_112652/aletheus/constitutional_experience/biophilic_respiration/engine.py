from ..helpers import clamp


class Engine:
    def cadence_hz(self, activity: float, reduced_motion: bool = False) -> float:
        return 0.0 if reduced_motion else 0.10 + 0.15 * clamp(activity)
