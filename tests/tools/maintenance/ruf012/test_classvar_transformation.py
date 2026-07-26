"""Tests for the conservative ClassVar transformation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from tools.maintenance.ruf012.transforms import (
    ClassVarTransformation,
    TransformationError,
)


def test_transformation_adds_classvar_to_existing_typing_import(
    candidate_factory: Any,
) -> None:
    source = (
        "from __future__ import annotations\n"
        "\n"
        "from typing import Any\n"
        "\n"
        "class Example:\n"
        "    VALUES = []\n"
    )
    candidate = candidate_factory(line=6)

    rewritten, notes = ClassVarTransformation().transform(
        candidate=candidate,
        path=Path("sample.py"),
        source=source,
    )

    assert "from typing import Any, ClassVar\n" in rewritten
    assert "    VALUES: ClassVar = []\n" in rewritten
    assert "Converted direct class assignment to ClassVar." in notes
    assert "Added ClassVar to existing typing import." in notes


def test_transformation_creates_classvar_import_after_future_import(
    candidate_factory: Any,
) -> None:
    source = (
        '"""Example module."""\n'
        "\n"
        "from __future__ import annotations\n"
        "\n"
        "\n"
        "class Example:\n"
        "    VALUES = {}\n"
    )
    candidate = candidate_factory(line=7)

    rewritten, notes = ClassVarTransformation().transform(
        candidate=candidate,
        path=Path("sample.py"),
        source=source,
    )

    expected_prefix = (
        '"""Example module."""\n'
        "\n"
        "from __future__ import annotations\n"
        "from typing import ClassVar\n"
    )

    assert rewritten.startswith(expected_prefix)
    assert "    VALUES: ClassVar = {}\n" in rewritten
    assert "Created ClassVar typing import." in notes


def test_transformation_reuses_existing_classvar_import(
    candidate_factory: Any,
) -> None:
    source = (
        "from typing import ClassVar\n"
        "\n"
        "\n"
        "class Example:\n"
        "    VALUES = set()\n"
    )
    candidate = candidate_factory(line=5)

    rewritten, notes = ClassVarTransformation().transform(
        candidate=candidate,
        path=Path("sample.py"),
        source=source,
    )

    assert rewritten.count("from typing import ClassVar") == 1
    assert "    VALUES: ClassVar = set()\n" in rewritten
    assert "Existing ClassVar import preserved." in notes


def test_transformation_rejects_non_safe_candidate(
    candidate_factory: Any,
) -> None:
    candidate = candidate_factory(classification="shared-class-state")

    assert ClassVarTransformation().supports(candidate) is False


def test_transformation_rejects_wrong_assignment_line(
    candidate_factory: Any,
) -> None:
    source = (
        "class Example:\n"
        "    VALUES = []\n"
    )
    candidate = candidate_factory(line=1)

    with pytest.raises(
        TransformationError,
        match="Expected exactly one direct class assignment",
    ):
        ClassVarTransformation().transform(
            candidate=candidate,
            path=Path("sample.py"),
            source=source,
        )


def test_transformation_rejects_nested_instance_assignment(
    candidate_factory: Any,
) -> None:
    source = (
        "class Example:\n"
        "    def __init__(self) -> None:\n"
        "        self.VALUES = []\n"
    )
    candidate = candidate_factory(line=3)

    with pytest.raises(
        TransformationError,
        match="Expected exactly one direct class assignment",
    ):
        ClassVarTransformation().transform(
            candidate=candidate,
            path=Path("sample.py"),
            source=source,
        )


def test_transformation_preserves_inline_comment(
    candidate_factory: Any,
) -> None:
    source = (
        "class Example:\n"
        "    VALUES = []  # maintained as a constant\n"
    )
    candidate = candidate_factory(line=2)

    rewritten, _ = ClassVarTransformation().transform(
        candidate=candidate,
        path=Path("sample.py"),
        source=source,
    )

    assert (
        "    VALUES: ClassVar = []  # maintained as a constant\n"
        in rewritten
    )
