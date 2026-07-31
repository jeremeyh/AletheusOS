#!/usr/bin/env python3
"""
Repository Steward.

Plans and applies safe structural moves for classifiable artifacts located in
the repository root. Dry-run is the default. Apply mode writes a rollback
manifest before changing the filesystem.
"""

from __future__ import annotations

import argparse
import json
import shutil
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

if __package__ in {None, ""}:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.repository.classifier import RepositoryClassifier, build_default_classifier
from tools.repository.inventory import RepositoryInventory
from tools.repository.rules import RepositoryPolicy


@dataclass(frozen=True, slots=True)
class MoveOperation:
    source: Path
    destination: Path
    rule_name: str
    confidence: float

    def to_dict(self) -> dict[str, object]:
        return {
            "source": str(self.source),
            "destination": str(self.destination),
            "rule_name": self.rule_name,
            "confidence": self.confidence,
        }


class RepositorySteward:
    def __init__(
        self,
        root: Path | str = ".",
        classifier: RepositoryClassifier | None = None,
    ) -> None:
        self.root = Path(root).resolve()
        self.classifier = classifier or build_default_classifier()
        self.state_directory = self.root / ".repository_steward"

    def plan(self) -> list[MoveOperation]:
        inventory = RepositoryInventory(self.root)
        policy = RepositoryPolicy(classifier=self.classifier)
        violations = policy.evaluate(inventory.root_files())

        operations: list[MoveOperation] = []

        for violation in violations:
            source = self.root / violation.path
            classification = self.classifier.classify(violation.path)

            if not classification.destination or not classification.rule_name:
                continue

            destination = self.root / classification.destination

            if source.resolve() == destination.resolve():
                continue

            operations.append(
                MoveOperation(
                    source=source,
                    destination=destination,
                    rule_name=classification.rule_name,
                    confidence=classification.confidence,
                )
            )

        return operations

    def conflicts(
        self,
        operations: Iterable[MoveOperation],
    ) -> list[MoveOperation]:
        return [operation for operation in operations if operation.destination.exists()]

    def apply(self, operations: Iterable[MoveOperation]) -> Path:
        operation_list = list(operations)
        conflicts = self.conflicts(operation_list)

        if conflicts:
            names = ", ".join(str(item.destination) for item in conflicts)
            raise FileExistsError(f"Destination conflicts detected: {names}")

        manifest_path = self._write_manifest(operation_list)

        for operation in operation_list:
            operation.destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(operation.source), str(operation.destination))

        self._write_latest(manifest_path)
        return manifest_path

    def rollback(self, manifest_path: Path | str | None = None) -> int:
        manifest = (
            Path(manifest_path) if manifest_path else self._latest_manifest_path()
        )

        if not manifest.exists():
            raise FileNotFoundError(f"Rollback manifest not found: {manifest}")

        payload = json.loads(manifest.read_text(encoding="utf-8"))
        operations = payload.get("operations", [])
        restored = 0

        for item in reversed(operations):
            source = Path(item["source"])
            destination = Path(item["destination"])

            if not destination.exists():
                continue

            if source.exists():
                raise FileExistsError(
                    f"Cannot rollback because source exists: {source}"
                )

            source.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(destination), str(source))
            restored += 1

        return restored

    def _write_manifest(self, operations: list[MoveOperation]) -> Path:
        self.state_directory.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        path = self.state_directory / f"moves-{timestamp}.json"

        payload = {
            "created_at": datetime.now(UTC).isoformat(),
            "root": str(self.root),
            "operation_count": len(operations),
            "operations": [operation.to_dict() for operation in operations],
        }

        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def _write_latest(self, manifest_path: Path) -> None:
        latest = self.state_directory / "latest.json"
        latest.write_text(
            json.dumps({"manifest": str(manifest_path)}, indent=2),
            encoding="utf-8",
        )

    def _latest_manifest_path(self) -> Path:
        latest = self.state_directory / "latest.json"

        if not latest.exists():
            raise FileNotFoundError("No latest rollback manifest is recorded.")

        payload = json.loads(latest.read_text(encoding="utf-8"))
        return Path(payload["manifest"])


def print_plan(
    operations: list[MoveOperation],
    conflicts: list[MoveOperation],
) -> None:
    print("AletheusOS Repository Steward")
    print("=" * 60)
    print(f"Planned moves: {len(operations)}")
    print(f"Conflicts:     {len(conflicts)}")
    print()

    for operation in operations:
        marker = "CONFLICT" if operation in conflicts else "MOVE"
        print(
            f"[{marker}] {operation.source} -> {operation.destination} "
            f"({operation.rule_name}, {operation.confidence:.0%})"
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Plan or apply repository structural normalization."
    )
    parser.add_argument("--root", default=".")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--rollback", nargs="?", const="latest")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    steward = RepositorySteward(args.root)

    if args.rollback:
        manifest = None if args.rollback == "latest" else args.rollback
        restored = steward.rollback(manifest)
        print(f"Restored {restored} files.")
        return 0

    operations = steward.plan()
    conflicts = steward.conflicts(operations)

    if args.json:
        print(
            json.dumps(
                {
                    "planned_moves": len(operations),
                    "conflicts": len(conflicts),
                    "operations": [item.to_dict() for item in operations],
                },
                indent=2,
            )
        )
    else:
        print_plan(operations, conflicts)

    if not args.apply:
        print("\nDry run only. Use --apply to execute.")
        return 0

    if conflicts:
        print("\nApply aborted because destination conflicts exist.")
        return 2

    manifest = steward.apply(operations)
    print(f"\nApplied {len(operations)} moves.")
    print(f"Rollback manifest: {manifest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
