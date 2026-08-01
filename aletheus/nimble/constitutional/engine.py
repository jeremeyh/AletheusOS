from __future__ import annotations

from .models import PrimitiveDefinition


class Engine:
    def catalog(self) -> tuple[PrimitiveDefinition, ...]:
        return (
            PrimitiveDefinition(
                name="AletheusIndex",
                layer="constitutional",
                purpose="Reserved constitutional truth and integrity instrument.",
                props=("score", "evidence", "confidence", "provenance"),
                reserved=True,
            ),
            PrimitiveDefinition(
                name="THORx",
                layer="constitutional",
                purpose="Reserved constitutional confidence and decision instrument.",
                props=("q_def", "d_def", "strike_zone", "confidence"),
                reserved=True,
            ),
        )
