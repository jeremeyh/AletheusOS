"""Kinekt™ Evolution Orchestrator engine."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .loader import load_roadmap
from .models import ExecutionManifest
from .planner import build_units
from .provenance import sha256_file
from .reporting import write_reports


class OrchestrationEngine:
    def __init__(self, roadmap: Path, output: Path) -> None:
        self.roadmap = roadmap.resolve()
        self.output = output.resolve()

    def plan(self) -> ExecutionManifest:
        payload = load_roadmap(self.roadmap)
        units, abstentions = build_units(payload)
        status = "planned" if units else "abstained"

        manifest = ExecutionManifest(
            generated_at=datetime.now(UTC).isoformat(),
            source_roadmap=str(self.roadmap),
            status=status,
            units=units,
            abstentions=abstentions,
            provenance={
                "roadmap_sha256": sha256_file(self.roadmap),
                "roadmap_path": str(self.roadmap),
            },
        )
        write_reports(manifest, self.output)
        return manifest
