"""Exceptions for the Constitutional Runtime Executive."""

from __future__ import annotations


class ConstitutionalRuntimeExecutiveError(Exception):
    """Base exception for CRX failures."""


class ExecutivePolicyError(
    ConstitutionalRuntimeExecutiveError
):
    """Raised when executive policy evaluation fails."""


class ExecutiveDecisionError(
    ConstitutionalRuntimeExecutiveError
):
    """Raised when an executive decision is invalid."""


class RecoveryPlanError(
    ConstitutionalRuntimeExecutiveError
):
    """Raised when a recovery plan cannot be produced."""
