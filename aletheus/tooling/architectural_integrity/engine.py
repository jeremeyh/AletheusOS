from __future__ import annotations

from .models import Assessment, Metric


class Engine:
    def evaluate(
        self,
        *,
        boundaries: float,
        cycles: float,
        registry: float,
        authority: float,
        cohesion: float,
        constitutional_compliance: float,
    ) -> Assessment:
        metrics = (
            Metric("boundary_integrity", boundaries, 1.2),
            Metric("cycle_freedom", cycles, 1.1),
            Metric("registry_consistency", registry, 1.0),
            Metric("authority_alignment", authority, 1.2),
            Metric("cohesion", cohesion, 0.9),
            Metric("constitutional_compliance", constitutional_compliance, 1.4),
        )
        score = round(
            sum(item.score * item.weight for item in metrics)
            / sum(item.weight for item in metrics),
            2,
        )
        status = "architecture_certified" if score >= 95 else "architecture_review"
        return Assessment(
            "AII",
            score,
            status,
            metrics,
            ("Architecture is judged by integrity, not visual neatness.",),
        )
