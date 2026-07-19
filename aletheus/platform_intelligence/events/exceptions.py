"""Exceptions for constitutional event contracts."""

from __future__ import annotations


class ConstitutionalEventError(Exception):
    """Base exception for constitutional event failures."""


class ConstitutionalEventValidationError(
    ConstitutionalEventError
):
    """Raised when an event violates its constitutional contract."""
