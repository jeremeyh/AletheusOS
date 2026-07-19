"""Exceptions raised by the Constitutional Knowledge Model."""

from __future__ import annotations

from .enums import ConstitutionalState


class ConstitutionalError(Exception):
    """Base exception for constitutional model failures."""


class ConstitutionalTransitionError(ConstitutionalError):
    """Raised when a lifecycle transition violates constitutional policy."""

    def __init__(
        self,
        current_state: ConstitutionalState,
        target_state: ConstitutionalState,
        *,
        reason: str | None = None,
    ) -> None:
        self.current_state = current_state
        self.target_state = target_state
        self.reason = reason

        message = (
            "Illegal constitutional lifecycle transition: "
            f"{current_state.value} -> {target_state.value}"
        )

        if reason:
            message = f"{message}. {reason}"

        super().__init__(message)
