from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "reports" / "repository_hygiene" / "empty_python_files.csv"

BATCH_ID = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

QUARANTINE_ROOT = ROOT / "archive" / "quarantine" / "empty_python_modules" / BATCH_ID
MANIFEST = QUARANTINE_ROOT / "manifest.json"


def load_candidates() -> list[Path]:
    if not REPORT.exists():
        raise FileNotFoundError(REPORT)

    candidates: list[Path] = []

    with REPORT.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        reader = csv.DictReader(handle)

        for row in reader:
            if row.get("classification") != "DELETE_CANDIDATE":
                continue

            relative_path = Path(row["path"])
            source = ROOT / relative_path

            if source.name == "__init__.py":
                raise RuntimeError(
                    f"Package marker incorrectly classified: {relative_path}"
                )

            candidates.append(source)

    return candidates


def validate_candidate(path: Path) -> None:
    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError(f"Candidate is outside repository: {path}") from exc

    if not path.exists():
        return

    if not path.is_file():
        raise RuntimeError(f"Candidate is not a file: {path}")

    if path.suffix != ".py":
        raise RuntimeError(f"Candidate is not Python: {path}")

    if path.name == "__init__.py":
        raise RuntimeError(f"Refusing to quarantine package marker: {path}")

    if path.stat().st_size != 0:
        raise RuntimeError(f"Candidate is no longer empty: {path}")


def remove_empty_parents(start: Path) -> list[str]:
    removed: list[str] = []
    current = start

    while current != ROOT:
        try:
            if any(current.iterdir()):
                break
        except FileNotFoundError:
            current = current.parent
            continue

        relative = current.relative_to(ROOT)
        current.rmdir()
        removed.append(str(relative))
        current = current.parent

    return removed


def main() -> None:
    parser = argparse.ArgumentParser(
        description=("Move audited empty Python modules into a reversible quarantine.")
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Move files. Without this option, perform a dry run.",
    )
    args = parser.parse_args()

    candidates = load_candidates()

    print("=" * 72)
    print("Empty Python Module Quarantine — " + ("APPLY" if args.apply else "DRY RUN"))
    print("=" * 72)
    print(f"Candidates: {len(candidates)}")
    print(f"Quarantine: {QUARANTINE_ROOT}")

    existing = []

    for source in candidates:
        validate_candidate(source)

        if source.exists():
            existing.append(source)

    print(f"Existing empty candidates: {len(existing)}")
    print(f"Already absent: {len(candidates) - len(existing)}")

    if not args.apply:
        print()
        print("No files were moved.")
        print("Apply with: python quarantine_empty_modules.py --apply")
        return

    if not existing:
        print()
        print(
            "No existing candidates remain. "
            "Nothing was moved and no manifest was created."
        )
        return

    QUARANTINE_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    moved: list[dict[str, str]] = []
    removed_directories: list[str] = []

    for source in existing:
        relative = source.relative_to(ROOT)
        destination = QUARANTINE_ROOT / relative

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        shutil.move(
            str(source),
            str(destination),
        )

        moved.append(
            {
                "source": str(relative),
                "quarantine": str(destination.relative_to(ROOT)),
            }
        )

        removed_directories.extend(remove_empty_parents(source.parent))

    manifest = {
        "created_at": datetime.now(UTC).isoformat(),
        "source_report": str(REPORT.relative_to(ROOT)),
        "moved_count": len(moved),
        "moved": moved,
        "removed_empty_directories": sorted(set(removed_directories)),
    }

    MANIFEST.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print(f"Moved files: {len(moved)}")
    print(f"Removed newly empty directories: {len(set(removed_directories))}")
    print(f"Manifest: {MANIFEST.relative_to(ROOT)}")
    print("Quarantine completed successfully.")


if __name__ == "__main__":
    main()
