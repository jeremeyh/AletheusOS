"""Tests for transformed-source validation."""

from __future__ import annotations

from pathlib import Path

from tools.maintenance.ruf012.validator import SourceValidator


def test_validator_accepts_valid_python() -> None:
    result = SourceValidator().validate(
        "class Example:\n    VALUES = []\n",
        Path("example.py"),
    )

    assert result.valid is True
    assert result.error is None


def test_validator_rejects_invalid_python() -> None:
    result = SourceValidator().validate(
        "class Example\n    VALUES = []\n",
        Path("example.py"),
    )

    assert result.valid is False
    assert result.error is not None
