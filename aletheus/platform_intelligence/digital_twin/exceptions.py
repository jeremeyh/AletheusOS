"""Exceptions for the Platform Digital Twin."""

from __future__ import annotations


class PlatformDigitalTwinError(Exception):
    """Base exception for Digital Twin failures."""


class TwinObjectNotFoundError(
    PlatformDigitalTwinError
):
    """Raised when a constitutional object cannot be found."""


class TwinSnapshotNotFoundError(
    PlatformDigitalTwinError
):
    """Raised when a retained snapshot cannot be found."""
