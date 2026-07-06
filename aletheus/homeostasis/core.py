from __future__ import annotations

from statistics import mean

from .models import VitalSign


class HomeostasisEngine:
    """
    Homeostasis Engine™

    Maintains a high-level stability picture of AletheusOS.
    """

    GENESIS = "7.1"
    VERSION = "0.1.0"

    def __init__(self):
        self.vitals: dict[str, VitalSign] = {}

    def record(self, name: str, score: float, message: str = "") -> VitalSign:
        score = max(0.0, min(100.0, float(score)))

        if score >= 95:
            status = "optimal"
        elif score >= 85:
            status = "stable"
        elif score >= 70:
            status = "warning"
        elif score >= 50:
            status = "degraded"
        else:
            status = "critical"

        vital = VitalSign(
            name=name,
            score=score,
            status=status,
            message=message,
        )

        self.vitals[name] = vital
        return vital

    def overall_score(self) -> float:
        if not self.vitals:
            return 100.0

        return round(mean(v.score for v in self.vitals.values()), 2)

    def overall_status(self) -> str:
        score = self.overall_score()

        if score >= 95:
            return "optimal"
        if score >= 85:
            return "stable"
        if score >= 70:
            return "warning"
        if score >= 50:
            return "degraded"

        return "critical"

    def health(self) -> dict:
        return {
            "name": "Homeostasis Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": self.overall_status(),
            "score": self.overall_score(),
            "vitals": {
                name: {
                    "score": vital.score,
                    "status": vital.status,
                    "message": vital.message,
                }
                for name, vital in self.vitals.items()
            },
        }

    def statistics(self) -> dict:
        return {
            "vital_signs": len(self.vitals),
            "overall_score": self.overall_score(),
            "overall_status": self.overall_status(),
        }


homeostasis_engine = HomeostasisEngine()
