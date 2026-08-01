from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SourceResult:
    source_id: str
    source_type: str
    payload: dict[str, Any]
    reliability: float
    latency_ms: float


class Engine:
    def gather(self, results: tuple[SourceResult, ...]) -> dict[str, object]:
        if not results:
            return {"sourceCount": 0, "agreement": 0.0, "results": []}
        agreement = sum(min(1.0, max(0.0, item.reliability)) for item in results) / len(
            results
        )
        return {
            "sourceCount": len(results),
            "agreement": agreement,
            "results": [
                {
                    "sourceId": item.source_id,
                    "sourceType": item.source_type,
                    "payload": item.payload,
                    "reliability": item.reliability,
                    "latencyMs": item.latency_ms,
                }
                for item in results
            ],
        }
