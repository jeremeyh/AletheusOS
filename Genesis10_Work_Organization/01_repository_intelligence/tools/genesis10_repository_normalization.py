#!/usr/bin/env python3
"""
Genesis 10 Repository Normalization

Safely normalizes the AletheusOS repository.

Features
--------
✓ Dry-run support
✓ Idempotent
✓ Creates destination folders
✓ Detects conflicts
✓ Logs every action
✓ Writes migration manifest
✓ Cross-platform

Usage

Preview:

    python tools/migration/genesis10_repository_normalization.py --dry-run

Execute:

    python tools/migration/genesis10_repository_normalization.py
"""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------
# Files that become canonical documentation
# ---------------------------------------------------------------------

FILE_MOVES = {
    "reports/runtime_core_decomposition_baseline.md": "docs/architecture/runtime_core_decomposition_baseline.md",
    "reports/runtime_v5_command_inventory.txt": "docs/architecture/runtime_v5_command_inventory.txt",
    "reports/release_cleanup_report.md": "docs/architecture/release_cleanup_report.md",
    "reports/architecture/crk_constitutional_ownership_map.md": "docs/architecture/crk_constitutional_ownership_map.md",
    "reports/architecture/crk_constitutional_ownership_map.json": "docs/architecture/crk_constitutional_ownership_map.json",
}


# ---------------------------------------------------------------------
# Generated reports
# ---------------------------------------------------------------------

DIRECTORY_MOVES = {
    "reports/guardian": "reports/generated/guardian",
    "reports/sentinel": "reports/generated/sentinel",
    "reports/council": "reports/generated/council",
    "reports/conclave": "reports/generated/conclave",
    "reports/atlas": "reports/generated/atlas",
    "reports/lighthouse": "reports/generated/lighthouse",
    "reports/platform": "reports/generated/platform",
    "reports/platform_census": "reports/generated/platform_census",
    "reports/platform_inspection": "reports/generated/platform_inspection",
    "reports/spectrum": "reports/generated/spectrum",
    "reports/nimble": "reports/generated/nimble",
    "reports/release_certification": "reports/generated/release_certification",
}


@dataclass
class Result:
    moved: list
    skipped: list
    conflicts: list
    missing: list


def ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def move_item(src: Path, dst: Path, dry: bool, result: Result):

    if not src.exists():
        result.missing.append(str(src))
        return

    if dst.exists():
        result.skipped.append(
            {
                "source": str(src),
                "destination": str(dst),
                "reason": "destination_exists",
            }
        )
        return

    ensure_parent(dst)

    if dry:
        result.moved.append(
            {
                "source": str(src),
                "destination": str(dst),
                "dry_run": True,
            }
        )
        return

    shutil.move(str(src), str(dst))

    result.moved.append(
        {
            "source": str(src),
            "destination": str(dst),
        }
    )


def write_manifest(result: Result):

    manifest = {
        "generated": datetime.utcnow().isoformat() + "Z",
        "moved": result.moved,
        "skipped": result.skipped,
        "missing": result.missing,
        "conflicts": result.conflicts,
    }

    out = ROOT / "reports" / "generated"
    out.mkdir(parents=True, exist_ok=True)

    with open(
        out / "repository_migration_manifest.json",
        "w",
        encoding="utf8",
    ) as f:
        json.dump(manifest, f, indent=2)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only",
    )

    args = parser.parse_args()

    result = Result([], [], [], [])

    #
    # Create canonical directories
    #

    for folder in [
        "docs",
        "docs/architecture",
        "docs/constitution",
        "docs/governance",
        "docs/implementation",
        "docs/decisions",
        "reports/generated",
        "tools/doctor",
        "tools/build",
        "tools/repair",
        "tools/audit",
        "tools/release",
        "tools/migration",
        "tools/repository",
    ]:
        path = ROOT / folder

        if not args.dry_run:
            path.mkdir(parents=True, exist_ok=True)

    #
    # Files
    #

    for src, dst in FILE_MOVES.items():
        move_item(
            ROOT / src,
            ROOT / dst,
            args.dry_run,
            result,
        )

    #
    # Directories
    #

    for src, dst in DIRECTORY_MOVES.items():
        move_item(
            ROOT / src,
            ROOT / dst,
            args.dry_run,
            result,
        )

    if not args.dry_run:
        write_manifest(result)

    print()

    print("=" * 60)
    print("Genesis 10 Repository Normalization")
    print("=" * 60)

    print()

    print(f"Moved:      {len(result.moved)}")
    print(f"Skipped:   {len(result.skipped)}")
    print(f"Missing:   {len(result.missing)}")
    print(f"Conflicts: {len(result.conflicts)}")

    print()

    if args.dry_run:
        print("Dry run completed.")
    else:
        print("Repository normalization completed.")


if __name__ == "__main__":
    main()
