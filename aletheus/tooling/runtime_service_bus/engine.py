from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ServiceBusEngine:
    def __init__(self, wiring: Path, output: Path) -> None:
        self.wiring = wiring
        self.output = output

    def build(self) -> dict[str, Any]:
        wiring = json.loads(self.wiring.read_text(encoding="utf-8"))
        channels: list[dict[str, Any]] = []
        for route in wiring.get("routes", []):
            if not isinstance(route, dict):
                continue
            source = route.get("source")
            target = route.get("target")
            if not isinstance(source, str) or not isinstance(target, str):
                continue
            channels.append(
                {
                    "channel_id": f"bus::{source}::{target}",
                    "source": source,
                    "target": target,
                    "modes": ["request_reply", "publish_subscribe"],
                    "requires_authority_context": True,
                    "requires_provenance": True,
                    "status": "declared",
                }
            )

        manifest = {
            "channels": channels,
            "channel_count": len(channels),
            "runtime_binding": "deferred_to_crk_event_bus_adapter",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "runtime-service-bus.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
        )
        (self.output / "channel-index.json").write_text(
            json.dumps(
                {item["channel_id"]: item for item in channels},
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return manifest
