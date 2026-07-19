"""Exceptions for the Constitutional Runtime Governor."""

from __future__ import annotations


class ConstitutionalRuntimeGovernorError(Exception):
    """Base exception for CRG failures."""


class GovernorConstraintError(
    ConstitutionalRuntimeGovernorError
):
    """Raised when governor constraints are invalid."""


class GovernorTargetNotFoundError(
    ConstitutionalRuntimeGovernorError
):
    """Raised when a governed target does not exist."""


class GovernorStateError(
    ConstitutionalRuntimeGovernorError
):
    """Raised when a governor state change is invalid."""
