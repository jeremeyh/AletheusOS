"""Configuration for Kinekt™ analysis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DEFAULT_EXCLUDED_PARTS = frozenset(
    {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "node_modules",
        "site-packages",
    }
)


@dataclass(frozen=True, slots=True)
class BoundaryRule:
    source_prefix: str
    forbidden_target_prefix: str
    reason: str


DEFAULT_BOUNDARY_RULES = (
    BoundaryRule(
        source_prefix="aletheus.runtime",
        forbidden_target_prefix="aletheus.experience",
        reason="Runtime must not depend on experience surfaces.",
    ),
    BoundaryRule(
        source_prefix="aletheus.runtime",
        forbidden_target_prefix="aletheus.applications",
        reason="Runtime must not depend on product applications.",
    ),
)


@dataclass(frozen=True, slots=True)
class KinektConfiguration:
    root: Path
    output: Path
    excluded_parts: frozenset[str] = DEFAULT_EXCLUDED_PARTS
    boundary_rules: tuple[BoundaryRule, ...] = DEFAULT_BOUNDARY_RULES
