from __future__ import annotations

import json
import os
from typing import Any, Dict


class RuntimeState:
    def __init__(self, path: str = "data/runtime_state.json") -> None:
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.state: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.path):
            return {"runtime_version": "v3", "snapshots": []}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2, default=str)

    def set(self, key: str, value: Any) -> None:
        self.state[key] = value
        self.save()

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)

    def snapshot(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        from services.context import utc_now_iso
        snap = {"name": name, "timestamp": utc_now_iso(), "payload": payload}
        self.state.setdefault("snapshots", []).append(snap)
        self.save()
        return snap
