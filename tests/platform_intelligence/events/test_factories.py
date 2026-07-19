from aletheus.platform_intelligence import (
    ConstitutionalHealth,
    ConstitutionalKind,
    ConstitutionalObject,
    ConstitutionalState,
    health_changed_event,
    object_registered_event,
    state_changed_event,
)


def make_service() -> ConstitutionalObject:
    return ConstitutionalObject.create(
        address="service.workspace",
        kind=ConstitutionalKind.PLATFORM_SERVICE,
        canonical_name="WorkspaceService",
        version="1.0.0",
        authority="Experience Constitution",
        owner="Workspace Engine",
    )


def test_object_registered_factory() -> None:
    service = make_service()

    event = object_registered_event(service)

    assert event.kind.value == "object.registered"
    assert str(event.subject) == "service.workspace"
    assert event.payload["object"]["canonical_name"] == (
        "WorkspaceService"
    )


def test_state_changed_factory() -> None:
    service = make_service()
    initializing = service.transition_to(
        ConstitutionalState.INITIALIZING
    )

    event = state_changed_event(
        initializing,
        previous_state=ConstitutionalState.REGISTERED,
    )

    assert event.payload["previous_state"] == "registered"
    assert event.payload["current_state"] == "initializing"


def test_health_changed_factory() -> None:
    service = make_service().report_health(
        ConstitutionalHealth.WARNING,
        metrics={"latency_ms": 51},
    )

    event = health_changed_event(
        service,
        previous_health=ConstitutionalHealth.UNKNOWN,
    )

    assert event.payload["previous_health"] == "unknown"
    assert event.payload["current_health"] == "warning"
    assert event.payload["metrics"]["latency_ms"] == 51
