"""Exceptions for the Constitutional Event Bus."""

from __future__ import annotations


class ConstitutionalEventBusError(Exception):
    """Base exception for event bus failures."""


class DuplicateSubscriptionError(
    ConstitutionalEventBusError
):
    """Raised when an identical subscription already exists."""


class SubscriptionNotFoundError(
    ConstitutionalEventBusError
):
    """Raised when a requested subscription does not exist."""


class EventPublicationError(
    ConstitutionalEventBusError
):
    """Raised when publication fails under strict dispatch policy."""
