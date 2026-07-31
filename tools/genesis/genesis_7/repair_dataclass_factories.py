#!/usr/bin/env python3
"""
Genesis 7 Structural Repair Tool

Repairs malformed dataclass field declarations of the form:

    field(default_factory(
        lambda: ...
    ))

into:

    field(
        default_factory=lambda: ...
    )

The malformed code is syntactically valid Python but fails during import
because it attempts to call a nonexistent name named ``default_factory``.

Safety features:
- AST-based detection
- Dry-run mode
- Timestamped backups
- Per-file compilation validation
- Automatic rollback on failed compilation
- Detailed repair report
"""

from __future__ import annotations

import argparse
import ast
import py_compile
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


@dataclass(frozen=True)
class Repair:
    """A single source-code replacement."""

    start: int
    end: int
    replacement: str
    original: str
    lineno: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Repair malformed dataclass default_factory declarations."
    )

    parser.add_argument(
        "--root",
        default="aletheus",
        help="Root package directory to scan. Default: aletheus",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report repairs without modifying files.",
    )

    parser.add_argument(
        "--report-dir",
        default="reports/genesis_7_structural_repair",
        help=(
            "Directory for backups and reports. "
            "Default: reports/genesis_7_structural_repair"
        ),
    )

    return parser.parse_args()


def line_offsets(source: str) -> list[int]:
    """
    Return absolute character offsets for the beginning of each source line.

    Index zero represents line 1.
    """

    offsets = [0]

    for index, character in enumerate(source):
        if character == "\n":
            offsets.append(index + 1)

    return offsets


def absolute_offset(
    offsets: list[int],
    lineno: int,
    col_offset: int,
) -> int:
    """Convert AST line and column coordinates to an absolute offset."""

    return offsets[lineno - 1] + col_offset


def is_name(node: ast.AST, expected: str) -> bool:
    return isinstance(node, ast.Name) and node.id == expected


def discover_repairs(source: str, path: Path) -> list[Repair]:
    """
    Identify malformed field(default_factory(...)) expressions.

    The target structure is:

        ast.Call(
            func=Name("field"),
            args=[
                ast.Call(
                    func=Name("default_factory"),
                    args=[factory_expression],
                )
            ],
        )

    Correct declarations using the keyword form are not modified.
    """

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        print(
            f"SKIP  {path}: existing SyntaxError: {exc.msg} at line {exc.lineno}",
            file=sys.stderr,
        )
        return []

    offsets = line_offsets(source)
    repairs: list[Repair] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if not is_name(node.func, "field"):
            continue

        if node.keywords:
            continue

        if len(node.args) != 1:
            continue

        malformed_factory = node.args[0]

        if not isinstance(malformed_factory, ast.Call):
            continue

        if not is_name(malformed_factory.func, "default_factory"):
            continue

        if malformed_factory.keywords:
            continue

        if len(malformed_factory.args) != 1:
            continue

        factory_expression = malformed_factory.args[0]
        expression_source = ast.get_source_segment(
            source,
            factory_expression,
        )

        if expression_source is None:
            print(
                f"SKIP  {path}:{node.lineno}: could not recover factory expression",
                file=sys.stderr,
            )
            continue

        if not all(
            hasattr(node, attribute)
            for attribute in (
                "lineno",
                "col_offset",
                "end_lineno",
                "end_col_offset",
            )
        ):
            print(
                f"SKIP  {path}:{node.lineno}: AST location information is incomplete",
                file=sys.stderr,
            )
            continue

        start = absolute_offset(
            offsets,
            node.lineno,
            node.col_offset,
        )
        end = absolute_offset(
            offsets,
            node.end_lineno,
            node.end_col_offset,
        )

        original = source[start:end]
        replacement = f"field(default_factory={expression_source})"

        repairs.append(
            Repair(
                start=start,
                end=end,
                replacement=replacement,
                original=original,
                lineno=node.lineno,
            )
        )

    return sorted(
        repairs,
        key=lambda repair: repair.start,
        reverse=True,
    )


def apply_repairs(source: str, repairs: list[Repair]) -> str:
    """Apply replacements from the end of the file toward the beginning."""

    updated = source

    for repair in repairs:
        updated = updated[: repair.start] + repair.replacement + updated[repair.end :]

    return updated


def compile_file(path: Path) -> tuple[bool, str]:
    """Compile a Python file and return validation status."""

    try:
        py_compile.compile(
            str(path),
            doraise=True,
        )
    except py_compile.PyCompileError as exc:
        return False, str(exc)

    return True, ""


def backup_path_for(
    path: Path,
    root: Path,
    backup_root: Path,
) -> Path:
    """Return a path preserving the source tree inside the backup folder."""

    relative = path.relative_to(root.parent)
    return backup_root / relative


def main() -> int:
    args = parse_args()

    root = Path(args.root).resolve()
    report_root = Path(args.report_dir).resolve()

    if not root.exists():
        print(f"ERROR: scan root does not exist: {root}", file=sys.stderr)
        return 1

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_root = report_root / timestamp
    backup_root = run_root / "backups"
    report_path = run_root / "repair_report.txt"

    run_root.mkdir(parents=True, exist_ok=True)

    python_files = sorted(root.rglob("*.py"))

    scanned_count = 0
    candidate_file_count = 0
    repair_count = 0
    changed_file_count = 0
    rollback_count = 0
    syntax_skip_count = 0

    report_lines = [
        "Genesis 7 Structural Repair Report",
        "=" * 72,
        f"Generated: {datetime.now(UTC).isoformat()}",
        f"Root: {root}",
        f"Dry run: {args.dry_run}",
        "",
    ]

    for path in python_files:
        scanned_count += 1

        try:
            source = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            report_lines.append(f"READ-FAIL {path}: {type(exc).__name__}: {exc}")
            continue

        try:
            ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            syntax_skip_count += 1
            report_lines.append(f"SYNTAX-SKIP {path}:{exc.lineno}: {exc.msg}")
            continue

        repairs = discover_repairs(source, path)

        if not repairs:
            continue

        candidate_file_count += 1
        repair_count += len(repairs)

        report_lines.append(f"FILE {path}")

        for repair in sorted(repairs, key=lambda item: item.lineno):
            report_lines.append(
                f"  LINE {repair.lineno}: "
                "field(default_factory(...)) "
                "-> field(default_factory=...)"
            )

        if args.dry_run:
            report_lines.append("  STATUS DRY-RUN")
            report_lines.append("")
            continue

        updated = apply_repairs(source, repairs)

        backup_path = backup_path_for(
            path,
            root,
            backup_root,
        )
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(path, backup_path)

        try:
            path.write_text(updated, encoding="utf-8")
        except OSError as exc:
            shutil.copy2(backup_path, path)

            rollback_count += 1
            report_lines.append(f"  STATUS WRITE-FAIL / ROLLED-BACK: {exc}")
            report_lines.append("")
            continue

        compiled, compile_error = compile_file(path)

        if not compiled:
            shutil.copy2(backup_path, path)

            rollback_count += 1
            report_lines.append("  STATUS COMPILE-FAIL / ROLLED-BACK")
            report_lines.append(f"  ERROR {compile_error}")
            report_lines.append("")
            continue

        changed_file_count += 1
        report_lines.append("  STATUS REPAIRED")
        report_lines.append(f"  BACKUP {backup_path}")
        report_lines.append("")

    report_lines.extend(
        [
            "=" * 72,
            "Summary",
            "-" * 72,
            f"Python files scanned: {scanned_count}",
            f"Candidate files: {candidate_file_count}",
            f"Malformed declarations found: {repair_count}",
            f"Files repaired: {changed_file_count}",
            f"Files rolled back: {rollback_count}",
            f"Files skipped for existing syntax errors: {syntax_skip_count}",
            "",
        ]
    )

    report_path.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print("=" * 72)
    print("Genesis 7 Structural Repair Tool")
    print("=" * 72)
    print(f"Python files scanned:          {scanned_count}")
    print(f"Candidate files:              {candidate_file_count}")
    print(f"Malformed declarations found: {repair_count}")
    print(f"Files repaired:               {changed_file_count}")
    print(f"Files rolled back:            {rollback_count}")
    print(f"Syntax-error files skipped:   {syntax_skip_count}")
    print()
    print(f"Report: {report_path}")

    if not args.dry_run and changed_file_count:
        print(f"Backups: {backup_root}")

    if rollback_count:
        print()
        print("WARNING: One or more repairs failed validation.")
        print("Review the report before continuing.")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
