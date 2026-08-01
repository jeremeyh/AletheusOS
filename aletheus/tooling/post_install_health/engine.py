from __future__ import annotations

import asyncio
import json
from collections.abc import Callable
from importlib import import_module
from pathlib import Path
from typing import Any

MissionFactory = Callable[[Path, Path, Path], Any]


class Engine:
    def __init__(
        self,
        process: Path,
        bus: Path,
        output: Path,
        mission_factory: MissionFactory | None = None,
    ) -> None:
        self.process = process
        self.bus = bus
        self.output = output
        self.mission_factory = mission_factory

    def _factory(self) -> MissionFactory:
        if self.mission_factory is not None:
            return self.mission_factory
        module = import_module("aletheus.tooling.end_to_end_mission.engine")
        return module.MissionExecutionEngine

    def verify(self) -> dict[str, Any]:
        mission = self._factory()(
            self.process,
            self.bus,
            self.output / "mission",
        )
        result = asyncio.run(
            mission.execute(
                "post-install-health",
                {"purpose": "production-readiness"},
            )
        )
        report = {
            "mission_status": result["status"],
            "platform_certification": result["platform_certification"],
            "healthy": (
                result["status"] == "completed"
                and result["platform_certification"] == "READY"
            ),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "post-install-health.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return report
