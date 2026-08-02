from __future__ import annotations

from hashlib import sha256
from json import dumps
from typing import Any, ClassVar

from .models import MissionSpec


class Engine:
    """Append-only cryptographic evidence provenance chronicle."""

    VERSION: ClassVar[str] = "33.12.0"

    def append(
        self,
        mission_id: str,
        event_type: str,
        payload: dict[str, Any],
        previous_hash: str = "GENESIS",
    ) -> dict[str, Any]:
        node = {
            "missionId": mission_id,
            "eventType": event_type,
            "payload": payload,
            "previousNodeHash": previous_hash,
        }
        node["nodeHash"] = sha256(
            dumps(node, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return node

    def verify(self, node: dict[str, Any]) -> bool:
        supplied = node.get("nodeHash", "")
        body = {key: value for key, value in node.items() if key != "nodeHash"}
        expected = sha256(
            dumps(body, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()
        return supplied == expected

    def evaluate(self, mission: MissionSpec) -> dict[str, Any]:
        node = self.append(
            mission.mission_id,
            "MISSION_ACTIVATED",
            {"objective": mission.objective},
        )
        return {"verified": self.verify(node), "node": node}
