#!/usr/bin/env python3
"""Apply conservative repository-integrity hardening operations."""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "config" / "repository_policy.json"
STATE_DIRECTORY = ROOT / ".repository_steward"


@dataclass(frozen=True)
class Operation:
    action: str
    source: str
    destination: str | None
    reason: str


def load_policy() -> dict[str, Any]:
    try:
        return json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing policy: {POLICY_PATH}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid policy JSON: {exc}") from exc


def malformed_destination(source: Path) -> Path:
    lower = source.name.lower()

    if "reason engine" in lower and "evaluation" in lower:
        return ROOT / "docs" / "repository" / "genesis49_reason_engine_evaluation.txt"

    return ROOT / "docs" / "repository" / "recovered_malformed_root_artifact.txt"


def plan_operations(policy: dict[str, Any]) -> list[Operation]:
    operations: list[Operation] = []

    ds_store = ROOT / ".DS_Store"
    if ds_store.exists():
        operations.append(
            Operation(
                action="delete",
                source=str(ds_store.relative_to(ROOT)),
                destination=None,
                reason="Generated macOS metadata",
            )
        )

    for entry in ROOT.iterdir():
        if not entry.is_file():
            continue

        if any(
            ord(character) < 32 or ord(character) == 127 for character in entry.name
        ):
            destination = malformed_destination(entry)
            operations.append(
                Operation(
                    action="move",
                    source=str(entry.relative_to(ROOT)),
                    destination=str(destination.relative_to(ROOT)),
                    reason="Malformed filename contains control characters",
                )
            )

    deterministic = policy.get("deterministic_moves", {})

    for source_name, destination_name in deterministic.items():
        source = ROOT / source_name
        destination = ROOT / destination_name

        if not source.exists():
            continue

        operations.append(
            Operation(
                action="move",
                source=source_name,
                destination=destination_name,
                reason="Explicit repository-policy classification",
            )
        )

    gitignore = ROOT / ".gitignore"
    gitignore_content = (
        gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    )

    if ".DS_Store" not in {line.strip() for line in gitignore_content.splitlines()}:
        operations.append(
            Operation(
                action="append",
                source=".gitignore",
                destination=None,
                reason="Ignore macOS metadata",
            )
        )

    return operations


def ensure_unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix

    for index in range(1, 1000):
        candidate = destination.with_name(f"{stem}-{index}{suffix}")
        if not candidate.exists():
            return candidate

    raise RuntimeError(f"Could not allocate unique destination for {destination}")


def save_manifest(operations: list[Operation]) -> Path:
    STATE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = STATE_DIRECTORY / f"hardening-{stamp}.json"

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "operations": [asdict(operation) for operation in operations],
    }

    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def apply_operations(operations: list[Operation]) -> None:
    for operation in operations:
        source = ROOT / operation.source

        if operation.action == "delete":
            if source.exists():
                source.unlink()
                print(f"[DELETE] {operation.source}")
            continue

        if operation.action == "append":
            gitignore = ROOT / ".gitignore"
            existing = (
                gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
            )

            if existing and not existing.endswith("\n"):
                existing += "\n"

            gitignore.write_text(
                existing + ".DS_Store\n",
                encoding="utf-8",
            )
            print("[APPEND] .DS_Store -> .gitignore")
            continue

        if operation.action == "move":
            if operation.destination is None:
                raise RuntimeError("Move operation has no destination.")

            if not source.exists():
                print(f"[SKIP] Missing source: {operation.source}")
                continue

            destination = ensure_unique_destination(ROOT / operation.destination)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))

            print(f"[MOVE] {operation.source} -> {destination.relative_to(ROOT)}")
            continue

        raise RuntimeError(f"Unsupported operation: {operation.action}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply conservative AletheusOS repository hardening."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the planned hardening operations.",
    )
    args = parser.parse_args()

    policy = load_policy()
    operations = plan_operations(policy)

    print("AletheusOS Repository Hardening")
    print("=" * 48)
    print(f"Planned operations: {len(operations)}")

    for operation in operations:
        if operation.destination:
            print(
                f"[{operation.action.upper()}] "
                f"{operation.source} -> {operation.destination}"
            )
        else:
            print(
                f"[{operation.action.upper()}] {operation.source} ({operation.reason})"
            )

    if not operations:
        print("\nNo deterministic hardening operations are required.")
        return 0

    if not args.apply:
        print("\nDry run only. Use --apply to execute.")
        return 0

    manifest = save_manifest(operations)
    apply_operations(operations)

    print(f"\nManifest: {manifest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
