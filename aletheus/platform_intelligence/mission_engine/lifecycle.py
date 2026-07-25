"""Lifecycle policy for constitutional missions."""

from __future__ import annotations

from .models import ConstitutionalMissionState

_ALLOWED_TRANSITIONS = {
    ConstitutionalMissionState.CREATED: {
        ConstitutionalMissionState.BLOCKED,
        ConstitutionalMissionState.READY,
        ConstitutionalMissionState.CANCELLED,
    },
    ConstitutionalMissionState.BLOCKED: {
        ConstitutionalMissionState.READY,
        ConstitutionalMissionState.CANCELLED,
    },
    ConstitutionalMissionState.READY: {
        ConstitutionalMissionState.BLOCKED,
        ConstitutionalMissionState.SCHEDULED,
        ConstitutionalMissionState.CANCELLED,
    },
    ConstitutionalMissionState.SCHEDULED: {
        ConstitutionalMissionState.RUNNING,
        ConstitutionalMissionState.CANCELLED,
    },
    ConstitutionalMissionState.RUNNING: {
        ConstitutionalMissionState.COMPLETED,
        ConstitutionalMissionState.FAILED,
        ConstitutionalMissionState.CANCELLED,
    },
    ConstitutionalMissionState.COMPLETED: set(),
    ConstitutionalMissionState.FAILED: {
        ConstitutionalMissionState.READY,
        ConstitutionalMissionState.CANCELLED,
    },
    ConstitutionalMissionState.CANCELLED: set(),
}


def transition_allowed(
    current: ConstitutionalMissionState,
    target: ConstitutionalMissionState,
) -> bool:
    """Return whether a lifecycle transition is constitutional."""

    return target in _ALLOWED_TRANSITIONS[current]
