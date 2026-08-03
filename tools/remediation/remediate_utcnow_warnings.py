from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALETHEUS = ROOT / "aletheus"
UTILITY = ALETHEUS / "time_utils.py"

REPORT_DIR = ROOT / "reports" / "repository_hygiene"

REPORT = REPORT_DIR / "utcnow_remediation.json"

EXCLUDED_PARTS = {
    "archive",
    "__pycache__",
    ".pytest_cache",
}

IMPORT_LINE = "from aletheus.time_utils import utc_now, utc_now_iso\n"

REPLACEMENTS = (
    (
        "datetime.utcnow().isoformat()",
        "utc_now_iso()",
    ),
    (
        "datetime.utcnow()",
        "utc_now()",
    ),
)


def active_python_files() -> list[Path]:
    result = []

    for path in ALETHEUS.rglob("*.py"):
        relative = path.relative_to(ROOT)

        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue

        if path == UTILITY:
            continue

        result.append(path)

    return sorted(result)


def import_insertion_offset(text: str) -> int:
    """
    Insert after module docstring and __future__ imports.
    """
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return 0

    text.splitlines(keepends=True)
    insertion_line = 0

    body = tree.body
    index = 0

    if (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    ):
        insertion_line = body[0].end_lineno or 0
        index = 1

    while index < len(body):
        node = body[index]

        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            insertion_line = node.end_lineno or insertion_line
            index += 1
            continue

        break

    return insertion_line


def add_import(text: str) -> str:
    if IMPORT_LINE.strip() in text:
        return text

    lines = text.splitlines(keepends=True)
    offset = import_insertion_offset(text)

    insertion = IMPORT_LINE

    if offset > 0:
        insertion = "\n" + IMPORT_LINE

    lines.insert(offset, insertion)
    return "".join(lines)


def transformed_text(
    text: str,
) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    updated = text

    for old, new in REPLACEMENTS:
        count = updated.count(old)
        counts[old] = count

        if count:
            updated = updated.replace(old, new)

    if sum(counts.values()):
        updated = add_import(updated)

    return updated, counts


def write_utility(apply: bool) -> bool:
    content = '''"""
Canonical UTC time utilities for AletheusOS.

All timestamps are timezone-aware and expressed in UTC.
"""

from __future__ import annotations

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return the current timezone-aware UTC datetime."""
    return datetime.now(UTC)


def utc_now_iso() -> str:
    """Return the current UTC timestamp in ISO-8601 format."""
    return utc_now().isoformat()
'''

    if UTILITY.exists():
        current = UTILITY.read_text(
            encoding="utf-8",
        )

        if current == content:
            return False

        raise RuntimeError(
            "aletheus/time_utils.py already exists with "
            "different content; refusing to overwrite it."
        )

    if apply:
        UTILITY.write_text(
            content,
            encoding="utf-8",
        )

    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
    )
    args = parser.parse_args()

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    changes = []
    total_replacements = 0

    for path in active_python_files():
        try:
            original = path.read_text(
                encoding="utf-8",
            )
        except (OSError, UnicodeDecodeError):
            continue

        updated, counts = transformed_text(original)

        replacements = sum(counts.values())

        if not replacements:
            continue

        if args.apply:
            path.write_text(
                updated,
                encoding="utf-8",
            )

        changes.append(
            {
                "path": str(path.relative_to(ROOT)),
                "replacements": replacements,
                "patterns": {
                    pattern: count for pattern, count in counts.items() if count
                },
            }
        )

        total_replacements += replacements

    utility_created = write_utility(args.apply)

    report = {
        "mode": ("apply" if args.apply else "dry_run"),
        "utility": str(UTILITY.relative_to(ROOT)),
        "utility_created": utility_created,
        "files_changed": len(changes),
        "total_replacements": total_replacements,
        "changes": changes,
    }

    REPORT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("UTCNOW Remediation — " + ("APPLY" if args.apply else "DRY RUN"))
    print("=" * 72)
    print(
        "Utility:",
        UTILITY.relative_to(ROOT),
    )
    print(
        "Files affected:",
        len(changes),
    )
    print(
        "Deprecated calls replaced:",
        total_replacements,
    )

    for change in changes:
        print(f"{change['replacements']:3}  {change['path']}")

    print()
    print(
        "Report:",
        REPORT.relative_to(ROOT),
    )

    if not args.apply:
        print("No source files were modified.")


if __name__ == "__main__":
    main()
