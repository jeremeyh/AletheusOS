"""Tests for transformation resolution."""

from __future__ import annotations

from typing import Any

from tools.maintenance.ruf012.registry import TransformationRegistry
from tools.maintenance.ruf012.transforms import ClassVarTransformation


def test_registry_resolves_safe_classvar_candidate(
    candidate_factory: Any,
) -> None:
    candidate = candidate_factory()

    transformation = TransformationRegistry().resolve(candidate)

    assert isinstance(transformation, ClassVarTransformation)


def test_registry_returns_none_for_unsupported_candidate(
    candidate_factory: Any,
) -> None:
    candidate = candidate_factory(classification="manual-review")

    transformation = TransformationRegistry().resolve(candidate)

    assert transformation is None
