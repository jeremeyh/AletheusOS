from __future__ import annotations

from .models import Assessment, Metric


class Engine:
    def evaluate(
        self,
        *,
        deployability: float,
        rollback: float,
        backup: float,
        provenance: float,
        compatibility: float,
        recovery: float,
    ) -> Assessment:
        metrics = (
            Metric("deployability", deployability, 1.1),
            Metric("rollback", rollback, 1.2),
            Metric("backup", backup, 0.9),
            Metric("provenance", provenance, 1.0),
            Metric("compatibility", compatibility, 1.1),
            Metric("recovery", recovery, 1.2),
        )
        score = round(
            sum(item.score * item.weight for item in metrics)
            / sum(item.weight for item in metrics),
            2,
        )
        status = "operationally_certified" if score >= 95 else "operational_review"
        return Assessment(
            "OEI",
            score,
            status,
            metrics,
            ("Operational confidence must survive failure, not only success.",),
        )
