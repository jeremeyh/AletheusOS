from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class DashboardEngine:
    def __init__(self, sources: dict[str, Path], output: Path) -> None:
        self.sources = sources
        self.output = output

    def build(self) -> dict[str, Any]:
        loaded: dict[str, dict[str, Any]] = {}
        for name, path in self.sources.items():
            if not path.exists():
                loaded[name] = {}
                continue
            payload = json.loads(path.read_text(encoding="utf-8"))
            loaded[name] = payload if isinstance(payload, dict) else {}

        observatory = loaded["observatory"]
        mission = loaded["mission_control"]
        com = loaded["com"]
        twin = loaded["twin"]

        dashboard = {
            "generated_at": datetime.now(UTC).isoformat(),
            "cards": [
                {
                    "id": "constitutional-health",
                    "label": "Constitutional Health",
                    "value": observatory.get("health_score", 0),
                },
                {
                    "id": "authority-coverage",
                    "label": "Authority Coverage",
                    "value": observatory.get("authority_coverage", 0),
                },
                {
                    "id": "missions",
                    "label": "Missions",
                    "value": len(mission.get("missions", [])),
                },
                {
                    "id": "consensus",
                    "label": "Consensus Records",
                    "value": len(com.get("consensus", [])),
                },
                {
                    "id": "twin-nodes",
                    "label": "Digital Twin Nodes",
                    "value": len(twin.get("nodes", [])),
                },
            ],
            "alerts": observatory.get("alerts", []),
            "readiness": observatory.get("readiness", "unknown"),
        }

        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "observatory-dashboard.json").write_text(
            json.dumps(dashboard, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return dashboard
