class MissionError(Exception):
    """Base class for all mission-related exceptions."""


class MissionValidationError(MissionError):
    """Raised when a mission fails validation or an illegal state transition occurs."""


class MissionExecutionError(MissionError):
    """Raised when mission execution fails."""
