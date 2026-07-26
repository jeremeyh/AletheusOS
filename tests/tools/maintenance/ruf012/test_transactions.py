"""Tests for the read-only transaction boundary."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from tools.maintenance.ruf012.models import RewritePreview
from tools.maintenance.ruf012.transactions import DryRunTransaction


def test_dry_run_transaction_never_commits() -> None:
    preview = RewritePreview(
        candidate=SimpleNamespace(),
        path=Path("sample.py"),
        original_source="VALUES = []\n",
        rewritten_source="VALUES: ClassVar = []\n",
        diff="-VALUES = []\n+VALUES: ClassVar = []\n",
        changed=True,
        validated=True,
        transformation="ruf012-classvar",
    )

    result = DryRunTransaction().apply(preview)

    assert result.committed is False
    assert result.path == Path("sample.py")
    assert "no source file was modified" in result.message.lower()
