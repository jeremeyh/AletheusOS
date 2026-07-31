"""Exceptions for the Constitutional Graph."""

from __future__ import annotations


class ConstitutionalGraphError(Exception):
    """Base exception for graph failures."""


class GraphNodeAlreadyExistsError(ConstitutionalGraphError):
    """Raised when a constitutional address already exists."""


class GraphNodeNotFoundError(ConstitutionalGraphError):
    """Raised when a requested graph node does not exist."""


class GraphRelationshipAlreadyExistsError(ConstitutionalGraphError):
    """Raised when an equivalent relationship already exists."""


class GraphRelationshipNotFoundError(ConstitutionalGraphError):
    """Raised when a requested relationship does not exist."""


class GraphNodeInUseError(ConstitutionalGraphError):
    """Raised when removing a connected node without force."""


class ConstitutionalCycleError(ConstitutionalGraphError):
    """Raised when a relationship would violate acyclic policy."""
