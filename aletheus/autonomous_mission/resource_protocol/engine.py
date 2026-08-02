from __future__ import annotations

from hashlib import sha256
from json import dumps
from typing import Any, ClassVar, Protocol, runtime_checkable

from .models import MissionSpec, ObservationFrame


@runtime_checkable
class MissionResource(Protocol):
    def resource_id(self) -> str: ...
    def poll(self, mission: MissionSpec) -> list[dict[str, Any]]: ...
    def status(self) -> dict[str, Any]: ...


class Engine:
    """Domain-neutral protocol compiler for mission resources."""

    VERSION: ClassVar[str] = "33.4.0"

    def normalize(
        self,
        resource_id: str,
        mission: MissionSpec,
        payload: dict[str, Any],
        timestamp: int = 0,
    ) -> ObservationFrame:
        canonical = dumps(payload, sort_keys=True, separators=(",", ":"))
        digest = sha256(canonical.encode()).hexdigest()
        return ObservationFrame(
            observation_id=f"obs_{digest[:16]}",
            entity_id=str(payload.get("entity_id", digest[:24])),
            source_resource_id=resource_id,
            timestamp=timestamp,
            payload=payload,
            content_hash=digest,
        )

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        frame = self.normalize(
            "resource:internal:demo",
            mission,
            {"entity_id": mission.mission_id, "objective": mission.objective},
        )
        return {"resourceProtocol": True, "observation": frame}
