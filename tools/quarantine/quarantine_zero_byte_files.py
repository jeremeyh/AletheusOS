from __future__ import annotations

import argparse
import csv
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = (
    ROOT
    / "reports"
    / "repository_hygiene"
    / "zero_byte_other_files.csv"
)

BATCH_ID = datetime.now(
    UTC
).strftime("%Y%m%dT%H%M%SZ")

QUARANTINE_ROOT = (
    ROOT
    / "archive"
    / "quarantine"
    / "zero_byte_non_python"
    / BATCH_ID
)

MANIFEST = QUARANTINE_ROOT / "manifest.json"

PROTECTED_NAMES = {
    ".gitkeep",
    ".keep",
    ".gitignore",
}

PROTECTED_DIRECTORY_NAMES = {
    "uploads",
    "exports",
    "logs",
    "runtime_state",
    "snapshots",
    "cache",
    "caches",
    "artifacts",
    "data",
    "tmp",
    "temp",
    "storage",
    "checkpoints",
}


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

            relative = Path(row["path"])

            if relative.name in PROTECTED_NAMES:
                continue

            if any(
                part.lower() in PROTECTED_DIRECTORY_NAMES
                for part in relative.parts
            ):
                continue

            candidates.append(ROOT / relative)

    return candidates


def validate(path: Path) -> None:
    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise RuntimeError(
            f"Path outside repository: {path}"
        ) from exc

    if not path.exists():
        return

    if not path.is_file():
        raise RuntimeError(
            f"Candidate is not a file: {path}"
        )

    if path.suffix == ".py":
        raise RuntimeError(
            f"Python file reached non-Python quarantine: {path}"
        )

    if path.stat().st_size != 0:
        raise RuntimeError(
            f"Candidate is no longer zero bytes: {path}"
        )


def remove_empty_parents(start: Path) -> list[str]:
    removed: list[str] = []
    current = start

    while current != ROOT:
        relative = current.relative_to(ROOT)

        if any(
            part.lower() in PROTECTED_DIRECTORY_NAMES
            for part in relative.parts
        ):
            break

        try:
            if any(current.iterdir()):
                break
        except FileNotFoundError:
            current = current.parent
            continue

        current.rmdir()
        removed.append(str(relative))
        current = current.parent

    return removed


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Quarantine audited zero-byte non-Python files."
        )
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Move files. Default behavior is a dry run.",
    )
    args = parser.parse_args()

    candidates = load_candidates()
    existing: list[Path] = []

    for path in candidates:
        validate(path)

        if path.exists():
            existing.append(path)

    print("=" * 72)
    print(
        "Zero-Byte Non-Python Quarantine — "
        + ("APPLY" if args.apply else "DRY RUN")
    )
    print("=" * 72)
    print(f"Audited candidates: {len(candidates)}")
    print(f"Existing candidates: {len(existing)}")
    print(f"Already absent: {len(candidates) - len(existing)}")
    print(f"Quarantine: {QUARANTINE_ROOT}")

    for path in existing[:100]:
        print(path.relative_to(ROOT))

    if len(existing) > 100:
        print(
            f"... and {len(existing) - 100} more"
        )

    if not args.apply:
        print()
        print("No files were moved.")
        print(
            "Apply with: "
            "python quarantine_zero_byte_files.py --apply"
        )
        return

    if not existing:
        print()
        print(
            "No existing candidates remain. "
            "Nothing was moved."
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
                "quarantine": str(
                    destination.relative_to(ROOT)
                ),
            }
        )

        removed_directories.extend(
            remove_empty_parents(source.parent)
        )

    manifest = {
        "created_at": datetime.now(
            UTC
        ).isoformat(),
        "source_report": str(
            REPORT.relative_to(ROOT)
        ),
        "moved_count": len(moved),
        "moved": moved,
        "removed_empty_directories": sorted(
            set(removed_directories)
        ),
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
    print(
        "Removed newly empty directories: "
        f"{len(set(removed_directories))}"
    )
    print(
        f"Manifest: {MANIFEST.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
