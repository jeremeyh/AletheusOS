"""Constitutional Runtime Observatory exceptions."""

from __future__ import annotations


class ConstitutionalRuntimeObservatoryError(Exception):
    """Base CRO exception."""


class ObservatorySnapshotNotFoundError(
    ConstitutionalRuntimeObservatoryError
):
    """Requested observatory snapshot does not exist."""
