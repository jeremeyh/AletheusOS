"""Exceptions for the Constitutional Policy Engine."""

from __future__ import annotations


class ConstitutionalPolicyEngineError(Exception):
    """Base exception for CPE failures."""


class PolicyAlreadyRegisteredError(
    ConstitutionalPolicyEngineError
):
    """Raised when a policy identifier is already registered."""


class PolicyNotFoundError(
    ConstitutionalPolicyEngineError
):
    """Raised when a requested policy does not exist."""


class PolicyEvaluationError(
    ConstitutionalPolicyEngineError
):
    """Raised when deterministic policy evaluation fails."""


class PolicyRegistryFrozenError(
    ConstitutionalPolicyEngineError
):
    """Raised when mutation is attempted after registry freezing."""
