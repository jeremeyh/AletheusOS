from __future__ import annotations

import json
from pathlib import Path


class OverlayStorage:
    GENESIS = "21.5"
    VERSION = "0.1.0"

    def save(self, overlays: list[dict], path: str | Path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            json.dumps(overlays, indent=2),
            encoding="utf-8",
        )

        return {
            "saved": True,
            "path": str(path),
            "overlays": len(overlays),
        }

    def load(self, path: str | Path):
        path = Path(path)

        if not path.exists():
            return []

        return json.loads(path.read_text(encoding="utf-8"))


overlay_storage = OverlayStorage()
