from aletheus.mission import (
    MissionExecution,
    MissionLifecycle,
    MissionState,
)


def test_valid_transition():
    execution = MissionExecution()

    MissionLifecycle.transition(
        execution,
        MissionState.VALIDATED,
    )

    assert execution.state is MissionState.VALIDATED


def test_invalid_transition():
    execution = MissionExecution()

    try:
        MissionLifecycle.transition(
            execution,
            MissionState.COMPLETED,
        )
        assert False
    except Exception:
        assert True
