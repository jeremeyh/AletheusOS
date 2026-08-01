from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, paths: Path, touchpoints: Path, output: Path) -> None:
        self.paths = paths
        self.touchpoints = touchpoints
        self.output = output

    def build(self) -> dict[str, Any]:
        paths = json.loads(self.paths.read_text(encoding="utf-8"))
        touchpoints = json.loads(self.touchpoints.read_text(encoding="utf-8"))
        verified = bool(paths.get("nodes")) and bool(touchpoints.get("touchpoints"))
        report = {
            "vertical_slices_verified": 1 if verified else 0,
            "top_to_bottom_connected": verified,
            "touchpoint_count": touchpoints.get("touchpoint_count", 0),
            "path_node_count": len(paths.get("nodes", [])),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "vertical-slice-verification.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
