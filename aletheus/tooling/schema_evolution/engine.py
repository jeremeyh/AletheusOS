from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class Migration:
    name: str
    from_version: int
    to_version: int
    apply: Callable[[dict[str, Any]], dict[str, Any]]


class Engine:
    def __init__(self, output: Path) -> None:
        self.output = output
        self._migrations: dict[int, Migration] = {}

    def register(self, migration: Migration) -> None:
        if migration.from_version in self._migrations:
            raise ValueError(f"Migration already registered: {migration.from_version}")
        self._migrations[migration.from_version] = migration

    def migrate(self, payload: dict[str, Any], target_version: int) -> dict[str, Any]:
        current = int(payload.get("schema_version", 0))
        result = dict(payload)
        history = list(result.get("migration_history", []))
        while current < target_version:
            migration = self._migrations.get(current)
            if migration is None:
                raise RuntimeError(f"No migration path from version {current}")
            result = migration.apply(result)
            current = migration.to_version
            result["schema_version"] = current
            history.append(migration.name)
        result["migration_history"] = history
        return result

    def write_report(self, payload: dict[str, Any]) -> Path:
        self.output.mkdir(parents=True, exist_ok=True)
        path = self.output / "schema-evolution.json"
        path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        return path
