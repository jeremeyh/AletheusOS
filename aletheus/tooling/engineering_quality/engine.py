from __future__ import annotations

from .models import Assessment, Metric


class Engine:
    def evaluate(
        self,
        *,
        lint: float,
        formatting: float,
        tests: float,
        coverage: float,
        complexity: float,
        maintainability: float,
    ) -> Assessment:
        metrics = (
            Metric("lint", lint, 1.0, ("ruff",)),
            Metric("formatting", formatting, 0.8, ("black",)),
            Metric("tests", tests, 1.4, ("pytest",)),
            Metric("coverage", coverage, 1.2, ("coverage",)),
            Metric("complexity", complexity, 0.8, ("radon",)),
            Metric("maintainability", maintainability, 0.8, ("maintainability",)),
        )
        total = sum(item.score * item.weight for item in metrics)
        weight = sum(item.weight for item in metrics)
        score = round(total / weight, 2)
        status = "engineering_certified" if score >= 95 else "engineering_review"
        return Assessment(
            "EQI",
            score,
            status,
            metrics,
            ("Engineering quality is evidence-weighted and reproducible.",),
        )
