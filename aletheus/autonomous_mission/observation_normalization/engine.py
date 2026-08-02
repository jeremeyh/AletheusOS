from __future__ import annotations

from hashlib import sha256
from json import dumps
from typing import Any, ClassVar

from .models import MissionSpec, ObservationFrame


class Engine:
    """Canonicalizes heterogeneous observations into stable evidence frames."""

    VERSION: ClassVar[str] = "33.8.0"

    def normalize(
        self,
        source: str,
        raw: dict[str, Any],
        timestamp: int,
    ) -> ObservationFrame:
        cleaned = {
            str(key).strip(): value for key, value in raw.items() if value is not None
        }
        canonical = dumps(cleaned, sort_keys=True, separators=(",", ":"))
        digest = sha256(canonical.encode()).hexdigest()
        return ObservationFrame(
            observation_id=f"obs_{digest[:16]}",
            entity_id=str(cleaned.get("entity_id", digest[:24])),
            source_resource_id=source,
            timestamp=timestamp,
            payload=cleaned,
            content_hash=digest,
        )

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        frame = self.normalize(
            "resource:internal:demo",
            {"entity_id": mission.mission_id, "objective": mission.objective},
            0,
        )
        return {"normalized": True, "frame": frame}
