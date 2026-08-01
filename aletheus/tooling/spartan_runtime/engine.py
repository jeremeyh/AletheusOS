from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SECURITY_COMPONENTS = [
    "SPARTAN",
    "SPAN",
    "Watch Tower",
    "Conclave",
    "Sentinel",
    "Security Mesh",
]


class Engine:
    def __init__(self, catalog: Path, bus: Path, output: Path) -> None:
        self.catalog = catalog
        self.bus = bus
        self.output = output

    def build(self) -> dict[str, Any]:
        catalog = json.loads(self.catalog.read_text(encoding="utf-8"))
        bus = json.loads(self.bus.read_text(encoding="utf-8"))
        names = {
            str(item.get("name"))
            for item in catalog.get("entries", [])
            if isinstance(item, dict)
        }
        channels = bus.get("channels", [])
        components = [
            {
                "name": name,
                "cataloged": name in names,
                "runtime": "shared_constitutional_runtime",
                "separate_security_runtime": False,
            }
            for name in SECURITY_COMPONENTS
        ]
        report = {
            "components": components,
            "service_bus_channels": len(channels) if isinstance(channels, list) else 0,
            "integration_mode": "shared_crk_runtime",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "spartan-runtime-integration.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
