"""Load Kinekt repository-intelligence data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_repository_report(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError("Repository intelligence report must be an object.")
    modules = payload.get("modules")
    if not isinstance(modules, list):
        raise TypeError("Repository intelligence report modules must be a list.")
    return payload
