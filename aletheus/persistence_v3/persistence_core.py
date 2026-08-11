from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class RuntimeSnapshot:
    snapshot_id: str
    name: str
    created_at: str
    path: str
    metadata: dict[str, Any] = field(default_factory=dict)


class AletheusPersistenceEngine:
    VERSION = "3.2.0"

    def __init__(self, base_path: str = "runtime_state"):
        self.base_path = Path(base_path)
        self.snapshots: dict[str, RuntimeSnapshot] = {}
        self.last_save: str | None = None
        self.last_load: str | None = None

    @property
    def version(self):
        return self.VERSION

    def bootstrap(self):
        self.base_path.mkdir(parents=True, exist_ok=True)
        (self.base_path / "snapshots").mkdir(parents=True, exist_ok=True)

        for name in [
            "runtime",
            "plugins",
            "applications",
            "agents",
            "workflows",
            "plans",
            "cluster",
            "metrics",
            "events",
        ]:
            path = self.base_path / f"{name}.json"
            if not path.exists():
                path.write_text(json.dumps({}, indent=2))

        return self._statistics_no_bootstrap()

    def save(self, runtime=None):
        self.bootstrap()

        state = self._collect_runtime_state(runtime)

        for key, value in state.items():
            path = self.base_path / f"{key}.json"
            path.write_text(json.dumps(value, indent=2, default=str))

        self.last_save = utc_now()

        return {
            "saved": True,
            "path": str(self.base_path),
            "last_save": self.last_save,
            "files": list(state.keys()),
        }

    def load(self):
        self.bootstrap()

        loaded = {}

        for file in self.base_path.glob("*.json"):
            try:
                loaded[file.stem] = json.loads(file.read_text())
            except Exception:
                loaded[file.stem] = {}

        self.last_load = utc_now()

        return {
            "loaded": True,
            "last_load": self.last_load,
            "state": loaded,
        }

    def snapshot(self, name: str = "Runtime Snapshot", runtime=None):
        self.save(runtime)

        (self.base_path / "snapshots").mkdir(parents=True, exist_ok=True)

        snapshot_id = str(uuid.uuid4())
        snapshot_dir = self.base_path / "snapshots" / snapshot_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        for file in self.base_path.glob("*.json"):
            if file.is_file():
                (snapshot_dir / file.name).write_text(file.read_text())

        snap = RuntimeSnapshot(
            snapshot_id=snapshot_id,
            name=name,
            created_at=utc_now(),
            path=str(snapshot_dir),
            metadata={
                "engine": "Aletheus Persistence Engine",
                "version": self.VERSION,
            },
        )

        self.snapshots[snapshot_id] = snap

        index_path = self.base_path / "snapshots.json"
        index_path.write_text(
            json.dumps(
                [asdict(s) for s in self.snapshots.values()],
                indent=2,
                default=str,
            )
        )

        return asdict(snap)

    def restore(self, snapshot_id: str):
        snap = self.snapshots.get(snapshot_id)

        if snap is None:
            index_path = self.base_path / "snapshots.json"
            if index_path.exists():
                for item in json.loads(index_path.read_text()):
                    if item.get("snapshot_id") == snapshot_id:
                        snap = RuntimeSnapshot(**item)
                        self.snapshots[snapshot_id] = snap
                        break

        if snap is None:
            return {"error": f"Snapshot not found: {snapshot_id}"}

        snapshot_dir = Path(snap.path)

        if not snapshot_dir.exists():
            return {"error": f"Snapshot path not found: {snap.path}"}

        for file in snapshot_dir.glob("*.json"):
            (self.base_path / file.name).write_text(file.read_text())

        return {
            "restored": True,
            "snapshot_id": snapshot_id,
            "path": str(snapshot_dir),
        }

    def export(self):
        self.bootstrap()

        return {
            "exported": True,
            "state": self.load()["state"],
        }

    def import_state(self, state: dict[str, Any]):
        self.bootstrap()

        for key, value in state.items():
            path = self.base_path / f"{key}.json"
            path.write_text(json.dumps(value, indent=2, default=str))

        self.last_save = utc_now()

        return {
            "imported": True,
            "items": len(state),
            "last_save": self.last_save,
        }

    def statistics(self):
        self.base_path.mkdir(parents=True, exist_ok=True)
        return self._statistics_no_bootstrap()

    def _statistics_no_bootstrap(self):
        json_files = list(self.base_path.glob("*.json"))
        snapshot_dirs = (
            list((self.base_path / "snapshots").glob("*"))
            if (self.base_path / "snapshots").exists()
            else []
        )

        size = sum(file.stat().st_size for file in json_files if file.is_file())

        return {
            "version": self.VERSION,
            "path": str(self.base_path),
            "files": len(json_files),
            "snapshots": len(snapshot_dirs),
            "last_save": self.last_save,
            "last_load": self.last_load,
            "size_bytes": size,
            "health": "healthy",
        }

    def _collect_runtime_state(self, runtime=None):
        if runtime is None:
            return {
                "runtime": {"version": self.VERSION},
                "plugins": {},
                "applications": {},
                "agents": {},
                "workflows": {},
                "plans": {},
                "cluster": {},
                "metrics": {},
                "events": {},
            }

        def safe(callable_obj, fallback):
            try:
                return callable_obj()
            except Exception:
                return fallback

        return {
            "runtime": {
                "version": getattr(runtime, "version", "unknown"),
                "status": getattr(runtime, "status", "unknown"),
            },
            "plugins": safe(lambda: runtime.plugins_v3.status(), {}),
            "applications": safe(lambda: runtime.applications.list_applications(), {}),
            "agents": safe(lambda: runtime.agents_v2.status(), {}),
            "workflows": safe(lambda: runtime.workflow_v3.status(), {}),
            "plans": safe(lambda: runtime.planning_v2.status(), {}),
            "cluster": safe(lambda: runtime.distributed.status(), {}),
            "metrics": safe(lambda: runtime.metrics.list(), {}),
            "events": safe(lambda: runtime.events.list(), {}),
        }


persistence_core = AletheusPersistenceEngine()
