"""Command-line entry point for the Genesis 11.2 batch preview engine."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """Build the batch-preview command-line parser."""

    parser = argparse.ArgumentParser(
        prog="python -m tools.maintenance.ruf012.preview_all",
        description=(
            "Scan the repository for safe RUF012 candidates and generate "
            "a validated, read-only batch preview."
        ),
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root. Defaults to the current working directory.",
    )
    parser.add_argument(
        "--report-dir",
        type=Path,
        default=Path("reports/maintenance/ruf012"),
        help=(
            "Directory for generated preview reports. Relative paths are "
            "resolved beneath the repository root."
        ),
    )
    parser.add_argument(
        "--no-reports",
        action="store_true",
        help="Print the summary without writing report artifacts.",
    )
    parser.add_argument(
        "--fail-on-error",
        action="store_true",
        help="Return a non-zero exit code when any candidate preview fails.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the repository-wide RUF012 batch preview."""

    args = build_parser().parse_args(argv)

    try:
        from .batch import BatchPreviewEngine
    except ImportError as exc:
        raise SystemExit(
            "Genesis 11.2 batch orchestration is not installed yet. "
            "Install Part 2 and Part 3 before running preview_all."
        ) from exc

    repository_root = args.root.expanduser().resolve()

    report_dir = args.report_dir.expanduser()
    if not report_dir.is_absolute():
        report_dir = repository_root / report_dir
    report_dir = report_dir.resolve()

    engine = BatchPreviewEngine(repository_root=repository_root)
    summary = engine.preview_all()

    print(engine.format_console_summary(summary))

    if not args.no_reports:
        from .reporting import BatchReportWriter

        writer = BatchReportWriter(
            repository_root=repository_root,
            report_directory=report_dir,
        )
        artifacts = writer.write(summary)

        print()
        print("Reports")
        print("-" * 72)
        for artifact in artifacts:
            print(artifact)

    if args.fail_on_error and summary.failed_count:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
