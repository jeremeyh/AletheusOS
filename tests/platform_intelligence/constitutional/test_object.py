from aletheus.platform_intelligence.constitutional import (
    ConstitutionalHealth,
    ConstitutionalKind,
    ConstitutionalObject,
    ConstitutionalState,
)


def make_service() -> ConstitutionalObject:
    return ConstitutionalObject.create(
        address="service.workspace",
        kind=ConstitutionalKind.PLATFORM_SERVICE,
        canonical_name="WorkspaceService",
        version="1.0.0",
        authority="Experience Constitution",
        owner="Workspace Engine",
        description="Coordinates constitutional workspaces.",
    )


def test_object_creation() -> None:
    service = make_service()

    assert service.address == "service.workspace"
    assert service.state is ConstitutionalState.REGISTERED
    assert service.health is ConstitutionalHealth.UNKNOWN


def test_state_transition_returns_new_representation() -> None:
    service = make_service()

    initializing = service.transition_to(
        ConstitutionalState.INITIALIZING
    )

    assert service.state is ConstitutionalState.REGISTERED
    assert initializing.state is ConstitutionalState.INITIALIZING
    assert initializing.identity == service.identity


def test_health_reporting_preserves_identity() -> None:
    service = make_service()

    updated = service.report_health(
        ConstitutionalHealth.WARNING,
        metrics={"latency_ms": 48},
    )

    assert updated.identity == service.identity
    assert updated.metrics["latency_ms"] == 48


def test_integrity_hash_is_deterministic() -> None:
    service = make_service()

    assert service.integrity_hash() == service.integrity_hash()


def test_snapshot_contains_constitutional_identity() -> None:
    service = make_service()

    snapshot = service.to_snapshot()

    assert snapshot["identity"]["address"] == "service.workspace"
    assert snapshot["identity"]["kind"] == "platform_service"
    assert len(snapshot["integrity_hash"]) == 64
