"""Load optimization roadmaps."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_roadmap(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("Optimization roadmap must be a JSON object.")
    work_packages = payload.get("work_packages")
    if not isinstance(work_packages, list):
        raise TypeError("Optimization roadmap work_packages must be a list.")
    return payload
