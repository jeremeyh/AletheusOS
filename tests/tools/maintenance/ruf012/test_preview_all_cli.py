"""Tests for the Genesis 11.2 batch-preview CLI foundation."""

from pathlib import Path

from tools.maintenance.ruf012.preview_all import build_parser


def test_preview_all_parser_uses_current_directory_by_default() -> None:
    args = build_parser().parse_args([])

    assert args.root == Path.cwd()
    assert args.report_dir == Path("reports/maintenance/ruf012")
    assert args.no_reports is False
    assert args.fail_on_error is False


def test_preview_all_parser_accepts_batch_options() -> None:
    args = build_parser().parse_args(
        [
            "--root",
            "/tmp/repository",
            "--report-dir",
            "/tmp/reports",
            "--no-reports",
            "--fail-on-error",
        ]
    )

    assert args.root == Path("/tmp/repository")
    assert args.report_dir == Path("/tmp/reports")
    assert args.no_reports is True
    assert args.fail_on_error is True
