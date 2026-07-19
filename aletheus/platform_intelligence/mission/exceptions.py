"""Canonical Mission exceptions."""

from __future__ import annotations


class ConstitutionalMissionError(Exception):
    """Base class for all constitutional mission errors."""


class MissionAlreadyExistsError(ConstitutionalMissionError):
    """Mission already exists."""


class MissionAlreadyRegisteredError(ConstitutionalMissionError):
    """Mission already registered."""


class MissionDependencyError(ConstitutionalMissionError):
    """Mission dependency violation."""


class MissionInUseError(ConstitutionalMissionError):
    """Mission cannot be removed because it is still referenced."""


class MissionNotFoundError(ConstitutionalMissionError):
    """Mission could not be found."""


class MissionTransitionError(ConstitutionalMissionError):
    """Illegal mission state transition."""


class MissionStateError(ConstitutionalMissionError):
    """Invalid scheduler mission state."""


class ConstitutionalMissionSchedulerError(ConstitutionalMissionError):
    """Scheduler error."""


class ConstitutionalMissionEngineError(ConstitutionalMissionError):
    """Mission engine error."""
