from __future__ import annotations

from statistics import mean


class Engine:
    def summarize(self, samples: tuple[dict[str, float], ...]) -> dict[str, object]:
        if not samples:
            raise ValueError("Telemetry samples are required.")
        keys = sorted(set().union(*(sample.keys() for sample in samples)))
        aggregates = {
            key: round(mean(sample.get(key, 0.0) for sample in samples), 3)
            for key in keys
        }
        return {
            "sample_count": len(samples),
            "aggregates": aggregates,
            "status": "observable",
        }
