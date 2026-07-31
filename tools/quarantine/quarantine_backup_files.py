from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "reports" / "repository_hygiene" / "backup_files.csv"

BATCH_ID = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

QUARANTINE_ROOT = ROOT / "archive" / "quarantine" / "backup_files" / BATCH_ID

MANIFEST = QUARANTINE_ROOT / "manifest.json"


def load_candidates() -> list[Path]:
    if not REPORT.exists():
        raise FileNotFoundError(REPORT)

    result: list[Path] = []

    with REPORT.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:
        for row in csv.DictReader(handle):
            relative = Path(row["path"])
            result.append(ROOT / relative)

    return result


def original_candidate(path: Path) -> Path | None:
    name = path.name

    suffix_patterns = (
        ".bak",
        ".orig",
        ".old",
        "~",
    )

    for suffix in suffix_patterns:
        if name.endswith(suffix):
            return path.with_name(name[: -len(suffix)])

    backup_match = re.match(
        r"^(?P<base>.+?)\.backup(?:_.*)?$",
        name,
    )

    if backup_match:
        return path.with_name(backup_match.group("base"))

    return None


def classify(path: Path) -> tuple[str, Path | None]:
    if not path.exists():
        return "ABSENT", None

    if not path.is_file():
        return "REVIEW_NOT_FILE", None

    original = original_candidate(path)

    if original is None:
        return "REVIEW_UNKNOWN_PATTERN", None

    if not original.exists():
        return "REVIEW_NO_ORIGINAL", original

    if not original.is_file():
        return "REVIEW_ORIGINAL_NOT_FILE", original

    try:
        backup_bytes = path.read_bytes()
        original_bytes = original.read_bytes()
    except OSError:
        return "REVIEW_READ_ERROR", original

    if backup_bytes == original_bytes:
        return "SAFE_DUPLICATE", original

    return "REVIEW_DIFFERENT_CONTENT", original


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
    )
    args = parser.parse_args()

    candidates = load_candidates()

    rows = []
    safe = []

    for path in candidates:
        status, original = classify(path)

        row = {
            "path": str(path.relative_to(ROOT)),
            "status": status,
            "original": (
                str(original.relative_to(ROOT)) if original is not None else ""
            ),
        }
        rows.append(row)

        if status == "SAFE_DUPLICATE":
            safe.append(path)

    print("=" * 72)
    print("Backup File Quarantine — " + ("APPLY" if args.apply else "DRY RUN"))
    print("=" * 72)
    print(f"Reported backup files: {len(candidates)}")
    print(f"Safe duplicates: {len(safe)}")
    print(
        "Review required:",
        len(candidates) - len(safe),
    )

    for row in rows:
        print(f"{row['status']:28} {row['path']}")

    if not args.apply:
        print()
        print("No files were moved.")
        return

    if not safe:
        print()
        print("No byte-identical backup files to move.")
        return

    QUARANTINE_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    moved = []

    for source in safe:
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

    manifest = {
        "created_at": datetime.now(UTC).isoformat(),
        "source_report": str(REPORT.relative_to(ROOT)),
        "moved_count": len(moved),
        "moved": moved,
        "review": [row for row in rows if row["status"] != "SAFE_DUPLICATE"],
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
    print(f"Moved safe duplicates: {len(moved)}")
    print(f"Manifest: {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
