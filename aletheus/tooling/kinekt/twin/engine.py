"""Kinekt™ Architectural Digital Twin engine."""

from __future__ import annotations

import hashlib
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from .builder import build_metrics, build_nodes, build_relationships
from .history import compare_previous
from .loader import load_object
from .models import TwinSnapshot
from .reporting import write_reports


class TwinEngine:
    def __init__(
        self,
        reports: dict[str, Path],
        output: Path,
        previous: Path | None = None,
    ) -> None:
        self.reports = {name: path.resolve() for name, path in reports.items()}
        self.output = output.resolve()
        self.previous = previous.resolve() if previous else None

    def build(self) -> TwinSnapshot:
        loaded = {name: load_object(path) for name, path in self.reports.items()}
        repository_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            check=True,
            text=True,
        ).stdout.strip()

        generated_at = datetime.now(UTC).isoformat()
        snapshot_seed = f"{repository_commit}:{generated_at}".encode()
        snapshot_id = hashlib.sha256(snapshot_seed).hexdigest()[:16]

        snapshot = TwinSnapshot(
            generated_at=generated_at,
            snapshot_id=snapshot_id,
            repository_commit=repository_commit,
            nodes=build_nodes(loaded["repository"], loaded["dependency"]),
            relationships=build_relationships(loaded["dependency"]),
            metrics=build_metrics(loaded),
            provenance={name: str(path) for name, path in self.reports.items()},
        )
        snapshot.changes = compare_previous(snapshot.to_dict(), self.previous)
        write_reports(snapshot, self.output)
        return snapshot
