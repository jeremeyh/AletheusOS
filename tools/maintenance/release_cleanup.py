#!/usr/bin/env python3
"""
=========================================================================
AletheusOS Release Cleanup
=========================================================================

Performs safe repository cleanup before Release Candidate / Production
builds.

Features
--------
✓ Removes Python cache
✓ Removes macOS junk
✓ Removes pytest/mypy/ruff caches
✓ Archives legacy directories (never deletes)
✓ Generates release cleanup report
✓ Dry-run mode
✓ Verbose output

Usage
-----

Dry run:

    python tools/maintenance/release_cleanup.py

Actually perform cleanup:

    python tools/maintenance/release_cleanup.py --apply

Verbose:

    python tools/maintenance/release_cleanup.py --apply --verbose

=========================================================================
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = ROOT / "reports"
LEGACY_DIR = ROOT / "legacy"

REMOVE_DIRS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

REMOVE_FILES = {
    ".DS_Store",
    ".AppleDouble",
    ".LSOverride",
}

REMOVE_SUFFIXES = {
    ".pyc",
    ".pyo",
}

ARCHIVE_DIRS = [
    "platform",
    "engine",
    "runtime",
]

SKIP_ARCHIVE_IF_CANONICAL = {
    "runtime",  # keep if still canonical
}

removed = []
archived = []
skipped = []


def log(msg: str):
    print(msg)


def delete_path(path: Path, apply: bool):
    if path.is_dir():
        if apply:
            shutil.rmtree(path)
        removed.append(str(path.relative_to(ROOT)))
    else:
        if apply:
            path.unlink(missing_ok=True)
        removed.append(str(path.relative_to(ROOT)))


def archive_directory(dirname: str, apply: bool):
    src = ROOT / dirname

    if not src.exists():
        return

    if dirname in SKIP_ARCHIVE_IF_CANONICAL:
        skipped.append(dirname)
        return

    LEGACY_DIR.mkdir(exist_ok=True)

    dst = LEGACY_DIR / dirname

    if dst.exists():
        skipped.append(dirname)
        return

    if apply:
        shutil.move(str(src), str(dst))

    archived.append(dirname)


def cleanup(remove_apply: bool):
    for path in ROOT.rglob("*"):

        if ".git" in path.parts:
            continue

        if path.is_dir() and path.name in REMOVE_DIRS:
            delete_path(path, remove_apply)
            continue

        if path.is_file():

            if path.name in REMOVE_FILES:
                delete_path(path, remove_apply)
                continue

            if path.suffix in REMOVE_SUFFIXES:
                delete_path(path, remove_apply)
                continue


def generate_report(apply: bool):

    REPORT_DIR.mkdir(exist_ok=True)

    report = REPORT_DIR / "release_cleanup_report.md"

    lines = []

    lines.append("# AletheusOS Release Cleanup")
    lines.append("")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append("")
    lines.append(f"Mode: {'APPLY' if apply else 'DRY RUN'}")
    lines.append("")
    lines.append("## Removed")
    lines.append("")

    if removed:
        lines.extend(f"- {r}" for r in sorted(removed))
    else:
        lines.append("- None")

    lines.append("")
    lines.append("## Archived")
    lines.append("")

    if archived:
        lines.extend(f"- legacy/{a}" for a in archived)
    else:
        lines.append("- None")

    lines.append("")
    lines.append("## Skipped")
    lines.append("")

    if skipped:
        lines.extend(f"- {s}" for s in skipped)
    else:
        lines.append("- None")

    report.write_text("\n".join(lines), encoding="utf-8")

    log("")
    log(f"Report written -> {report.relative_to(ROOT)}")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Perform cleanup instead of dry-run.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
    )

    args = parser.parse_args()

    log("")
    log("=" * 72)
    log("AletheusOS Release Cleanup")
    log("=" * 72)

    cleanup(args.apply)

    for d in ARCHIVE_DIRS:
        archive_directory(d, args.apply)

    generate_report(args.apply)

    log("")
    log("=" * 72)
    log(f"Removed : {len(removed)}")
    log(f"Archived: {len(archived)}")
    log(f"Skipped : {len(skipped)}")
    log("=" * 72)

    if not args.apply:
        log("")
        log("Dry run complete.")
        log("")
        log("Run with:")
        log("")
        log("    python tools/maintenance/release_cleanup.py --apply")


if __name__ == "__main__":
    main()
