"""Exceptions for the Constitutional Runtime Supervisor."""

from __future__ import annotations


class ConstitutionalRuntimeSupervisorError(Exception):
    """Base exception for CRS failures."""


class SupervisorLifecycleError(
    ConstitutionalRuntimeSupervisorError
):
    """Raised when a supervisor lifecycle action is invalid."""


class SupervisorRecoveryError(
    ConstitutionalRuntimeSupervisorError
):
    """Raised when dependency-aware recovery cannot complete."""


class SupervisorServiceNotFoundError(
    ConstitutionalRuntimeSupervisorError
):
    """Raised when a supervised service does not exist."""
