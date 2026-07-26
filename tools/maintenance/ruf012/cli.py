"""
Genesis 11 native RUF012 command-line interface.

This module is responsible only for:

    * Parsing command-line arguments
    * Invoking the Runner
    * Returning an exit code

Business logic belongs in Runner.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tools.maintenance.ruf012.runner import Runner


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""

    parser = argparse.ArgumentParser(
        prog="ruf012",
        description="Genesis 11 native RUF012 maintenance pipeline.",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Repository root (default: current directory).",
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "--preview",
        action="store_true",
        help="Run in preview mode (default).",
    )

    mode.add_argument(
        "--apply",
        action="store_true",
        help="Apply repository changes (reserved for future implementation).",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Reserved for future machine-readable output.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="Genesis 11 RUF012 Pipeline",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.apply:
        parser.error(
            "--apply is not yet implemented. "
            "Preview mode is currently the only supported mode."
        )

    runner = Runner(
        root=Path(args.path),
    )

    return runner.run()


if __name__ == "__main__":
    sys.exit(main())
