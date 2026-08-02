from __future__ import annotations

from dataclasses import asdict
from hashlib import sha256
from json import dumps
from typing import Any, ClassVar

from .models import MissionSpec, MissionStatus


class Engine:
    """Checkpoint and recovery runtime for durable mission state."""

    VERSION: ClassVar[str] = "33.11.0"

    def checkpoint(
        self,
        mission: MissionSpec,
        status: MissionStatus,
        sequence: int,
    ) -> dict[str, Any]:
        body = {
            "mission": asdict(mission),
            "status": status.value,
            "sequence": sequence,
        }
        body["checkpointHash"] = sha256(
            dumps(body, sort_keys=True).encode()
        ).hexdigest()
        return body

    def recover(self, checkpoint: dict[str, Any]) -> dict[str, Any]:
        supplied = checkpoint.get("checkpointHash", "")
        body = {
            key: value for key, value in checkpoint.items() if key != "checkpointHash"
        }
        expected = sha256(dumps(body, sort_keys=True).encode()).hexdigest()
        if supplied != expected:
            raise ValueError("Checkpoint integrity verification failed.")
        return {"recovered": True, **checkpoint}

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        return self.checkpoint(mission, MissionStatus.ACTIVATED, 1)
