from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import ClassVar

from .models import Assessment, Metric


class Engine:
    THRESHOLDS: ClassVar[dict[str, float]] = {
        "production_certified": 95.0,
        "production_ready": 90.0,
        "conditional": 80.0,
        "not_ready": 0.0,
    }

    def evaluate(self, metrics: Iterable[Metric]) -> Assessment:
        items = tuple(metrics)
        if not items:
            raise ValueError("At least one metric is required.")
        total_weight = sum(item.weight for item in items)
        score = sum(item.score * item.weight for item in items) / total_weight
        status = "not_ready"
        for name, threshold in self.THRESHOLDS.items():
            if score >= threshold:
                status = name
                break
        rationale = tuple(
            f"{item.name}: {item.score:.2f} weighted at {item.weight:.2f}"
            for item in items
        )
        return Assessment("PSS", round(score, 2), status, items, rationale)

    def write_report(self, assessment: Assessment, output: Path) -> Path:
        output.mkdir(parents=True, exist_ok=True)
        target = output / "production-success-standard.json"
        target.write_text(
            json.dumps(assessment.to_dict(), indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return target
