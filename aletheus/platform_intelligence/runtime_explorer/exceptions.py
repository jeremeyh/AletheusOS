"""Exceptions for the Runtime Explorer."""

from __future__ import annotations


class RuntimeExplorerError(Exception):
    """Base exception for Runtime Explorer failures."""


class ExplorerQueryError(RuntimeExplorerError):
    """Raised when a constitutional query is invalid."""


class ExplorerObjectNotFoundError(RuntimeExplorerError):
    """Raised when an object cannot be found."""
