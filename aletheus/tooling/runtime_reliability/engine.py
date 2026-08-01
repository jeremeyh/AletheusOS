from __future__ import annotations

from .models import Assessment, Metric


class Engine:
    def evaluate(
        self,
        *,
        lifecycle: float,
        scheduler: float,
        event_latency: float,
        resilience: float,
        saturation: float,
        async_correctness: float,
    ) -> Assessment:
        metrics = (
            Metric("lifecycle", lifecycle, 1.0),
            Metric("scheduler", scheduler, 1.0),
            Metric("event_latency", event_latency, 1.0),
            Metric("resilience", resilience, 1.3),
            Metric("saturation_control", saturation, 1.0),
            Metric("async_correctness", async_correctness, 1.2),
        )
        score = round(
            sum(item.score * item.weight for item in metrics)
            / sum(item.weight for item in metrics),
            2,
        )
        status = "runtime_certified" if score >= 95 else "runtime_review"
        return Assessment(
            "RRI",
            score,
            status,
            metrics,
            ("Reliability is demonstrated across lifecycle and pressure.",),
        )
