"""Exceptions for the Constitutional Runtime Kernel."""

from __future__ import annotations


class ConstitutionalRuntimeKernelError(Exception):
    """Base exception for CRK failures."""


class KernelLifecycleError(ConstitutionalRuntimeKernelError):
    """Raised when a CRK lifecycle transition is invalid."""


class KernelCompositionError(ConstitutionalRuntimeKernelError):
    """Raised when CRK composition cannot be completed."""


class KernelServiceRegistrationError(ConstitutionalRuntimeKernelError):
    """Raised when canonical CRK services cannot be registered."""
