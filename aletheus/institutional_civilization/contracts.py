"""Public contracts for constitutional institutions."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from .models import InstitutionRecord


@runtime_checkable
class InstitutionalCapability(Protocol):
    """
    Runtime protocol for a capability that publishes institutional identity.

    Existing engines do not need to inherit from a shared base class.
    Structural typing keeps institutional adoption compositional.
    """

    def institution_record(self) -> InstitutionRecord:
        """Return the capability's canonical institutional definition."""
        ...


@runtime_checkable
class InstitutionHealthProvider(Protocol):
    """Optional health contract for an implemented institution."""

    def health(self) -> dict:
        """Return inspectable institutional health."""
        ...
