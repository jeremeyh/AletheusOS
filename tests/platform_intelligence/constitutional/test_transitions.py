import pytest

from aletheus.platform_intelligence.constitutional import (
    CANONICAL_TRANSITION_POLICY,
    ConstitutionalHealth,
    ConstitutionalKind,
    ConstitutionalObject,
    ConstitutionalState,
    ConstitutionalTransitionError,
)


def make_service(
    state: ConstitutionalState = ConstitutionalState.REGISTERED,
) -> ConstitutionalObject:
    return ConstitutionalObject.create(
        address="service.workspace",
        kind=ConstitutionalKind.PLATFORM_SERVICE,
        canonical_name="WorkspaceService",
        version="1.0.0",
        authority="Experience Constitution",
        owner="Workspace Engine",
        state=state,
    )


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (
            ConstitutionalState.REGISTERED,
            ConstitutionalState.INITIALIZING,
        ),
        (
            ConstitutionalState.INITIALIZING,
            ConstitutionalState.STARTING,
        ),
        (
            ConstitutionalState.STARTING,
            ConstitutionalState.RUNNING,
        ),
        (
            ConstitutionalState.RUNNING,
            ConstitutionalState.PAUSED,
        ),
        (
            ConstitutionalState.PAUSED,
            ConstitutionalState.RUNNING,
        ),
        (
            ConstitutionalState.RUNNING,
            ConstitutionalState.DEGRADED,
        ),
        (
            ConstitutionalState.DEGRADED,
            ConstitutionalState.RECOVERING,
        ),
        (
            ConstitutionalState.RECOVERING,
            ConstitutionalState.RUNNING,
        ),
        (
            ConstitutionalState.RUNNING,
            ConstitutionalState.STOPPING,
        ),
        (
            ConstitutionalState.STOPPING,
            ConstitutionalState.STOPPED,
        ),
        (
            ConstitutionalState.STOPPED,
            ConstitutionalState.STARTING,
        ),
        (
            ConstitutionalState.STOPPED,
            ConstitutionalState.RETIRED,
        ),
    ],
)
def test_canonical_transition_policy_permits_valid_transitions(
    current: ConstitutionalState,
    target: ConstitutionalState,
) -> None:
    assert CANONICAL_TRANSITION_POLICY.permits(current, target)


@pytest.mark.parametrize(
    ("current", "target"),
    [
        (
            ConstitutionalState.RUNNING,
            ConstitutionalState.REGISTERED,
        ),
        (
            ConstitutionalState.RETIRED,
            ConstitutionalState.RUNNING,
        ),
        (
            ConstitutionalState.REGISTERED,
            ConstitutionalState.RUNNING,
        ),
        (
            ConstitutionalState.STOPPED,
            ConstitutionalState.INITIALIZING,
        ),
    ],
)
def test_canonical_transition_policy_rejects_invalid_transitions(
    current: ConstitutionalState,
    target: ConstitutionalState,
) -> None:
    assert not CANONICAL_TRANSITION_POLICY.permits(current, target)

    with pytest.raises(ConstitutionalTransitionError):
        CANONICAL_TRANSITION_POLICY.require(current, target)


def test_same_state_transition_is_rejected() -> None:
    with pytest.raises(
        ConstitutionalTransitionError,
        match="must change state",
    ):
        CANONICAL_TRANSITION_POLICY.require(
            ConstitutionalState.RUNNING,
            ConstitutionalState.RUNNING,
        )


def test_retired_state_is_terminal() -> None:
    assert (
        CANONICAL_TRANSITION_POLICY.allowed_targets(
            ConstitutionalState.RETIRED
        )
        == frozenset()
    )


def test_object_transition_uses_canonical_policy() -> None:
    service = make_service()

    initializing = service.transition_to(
        ConstitutionalState.INITIALIZING
    )
    starting = initializing.transition_to(
        ConstitutionalState.STARTING
    )
    running = starting.transition_to(
        ConstitutionalState.RUNNING,
        health=ConstitutionalHealth.HEALTHY,
    )

    assert running.state is ConstitutionalState.RUNNING
    assert running.health is ConstitutionalHealth.HEALTHY


def test_object_rejects_illegal_transition() -> None:
    service = make_service(ConstitutionalState.RUNNING)

    with pytest.raises(
        ConstitutionalTransitionError,
        match="running -> registered",
    ):
        service.transition_to(ConstitutionalState.REGISTERED)


def test_failed_transition_does_not_mutate_object() -> None:
    service = make_service(ConstitutionalState.RUNNING)

    with pytest.raises(ConstitutionalTransitionError):
        service.transition_to(ConstitutionalState.REGISTERED)

    assert service.state is ConstitutionalState.RUNNING
