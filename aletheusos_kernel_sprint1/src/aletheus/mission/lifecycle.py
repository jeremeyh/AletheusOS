from .enums import MissionState
from .exceptions import MissionValidationError

_ALLOWED = {
    MissionState.CREATED: {MissionState.VALIDATED, MissionState.FAILED},
    MissionState.VALIDATED: {MissionState.PLANNED},
    MissionState.PLANNED: {MissionState.APPROVED},
    MissionState.APPROVED: {MissionState.EXECUTING},
    MissionState.EXECUTING: {
        MissionState.COMPLETED,
        MissionState.PAUSED,
        MissionState.FAILED,
    },
    MissionState.PAUSED: {
        MissionState.EXECUTING,
        MissionState.FAILED,
    },
    MissionState.COMPLETED: {
        MissionState.ARCHIVED,
    },
    MissionState.FAILED: {
        MissionState.ARCHIVED,
    },
    MissionState.ARCHIVED: set(),
}


class MissionLifecycle:
    @staticmethod
    def transition(execution, target):
        current = execution.state

        if target not in _ALLOWED[current]:
            raise MissionValidationError(
                f"Illegal transition: {current.value} -> {target.value}"
            )

        execution.state = target
        return execution
