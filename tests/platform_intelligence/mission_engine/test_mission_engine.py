from __future__ import annotations

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalEventBus,
    ConstitutionalMission,
    ConstitutionalMissionEngine,
    ConstitutionalMissionState,
    MissionAlreadyExistsError,
    MissionDependencyError,
    MissionInUseError,
    MissionNotFoundError,
    MissionTransitionError,
)


def mission(
    address: str,
    *,
    dependencies: tuple[str, ...] = (),
) -> ConstitutionalMission:
    return ConstitutionalMission.create(
        address=address,
        title=address,
        objective=f"Complete {address}",
        dependencies=dependencies,
    )


def test_register_root_mission_becomes_ready() -> None:
    engine = ConstitutionalMissionEngine()

    registered = engine.register(mission("mission.root"))

    assert registered.state is (ConstitutionalMissionState.READY)


def test_register_dependent_mission_becomes_blocked() -> None:
    engine = ConstitutionalMissionEngine()

    engine.register(mission("mission.root"))

    dependent = engine.register(
        mission(
            "mission.dependent",
            dependencies=("mission.root",),
        )
    )

    assert dependent.state is (ConstitutionalMissionState.BLOCKED)


def test_duplicate_mission_is_rejected() -> None:
    engine = ConstitutionalMissionEngine()
    value = mission("mission.root")

    engine.register(value)

    with pytest.raises(MissionAlreadyExistsError):
        engine.register(value)


def test_missing_dependency_is_rejected() -> None:
    engine = ConstitutionalMissionEngine()

    with pytest.raises(MissionDependencyError):
        engine.register(
            mission(
                "mission.dependent",
                dependencies=("mission.root",),
            )
        )


def test_register_many_resolves_order() -> None:
    engine = ConstitutionalMissionEngine()

    registered = engine.register_many(
        [
            mission(
                "mission.dependent",
                dependencies=("mission.root",),
            ),
            mission("mission.root"),
        ]
    )

    assert [item.address for item in registered] == [
        "mission.root",
        "mission.dependent",
    ]


def test_unknown_mission_is_rejected() -> None:
    engine = ConstitutionalMissionEngine()

    with pytest.raises(MissionNotFoundError):
        engine.get("mission.missing")


def test_valid_lifecycle() -> None:
    engine = ConstitutionalMissionEngine()

    engine.register(mission("mission.root"))

    scheduled = engine.transition(
        "mission.root",
        ConstitutionalMissionState.SCHEDULED,
    )
    running = engine.transition(
        "mission.root",
        ConstitutionalMissionState.RUNNING,
    )
    completed = engine.transition(
        "mission.root",
        ConstitutionalMissionState.COMPLETED,
    )

    assert scheduled.state is (ConstitutionalMissionState.SCHEDULED)
    assert running.state is (ConstitutionalMissionState.RUNNING)
    assert completed.state is (ConstitutionalMissionState.COMPLETED)


def test_invalid_transition_is_rejected() -> None:
    engine = ConstitutionalMissionEngine()

    engine.register(mission("mission.root"))

    with pytest.raises(MissionTransitionError):
        engine.transition(
            "mission.root",
            ConstitutionalMissionState.COMPLETED,
        )


def test_failed_transition_requires_reason() -> None:
    engine = ConstitutionalMissionEngine()

    engine.register(mission("mission.root"))
    engine.transition(
        "mission.root",
        ConstitutionalMissionState.SCHEDULED,
    )
    engine.transition(
        "mission.root",
        ConstitutionalMissionState.RUNNING,
    )

    with pytest.raises(MissionTransitionError):
        engine.transition(
            "mission.root",
            ConstitutionalMissionState.FAILED,
        )


def test_completion_unblocks_dependent() -> None:
    engine = ConstitutionalMissionEngine()

    engine.register(mission("mission.root"))
    engine.register(
        mission(
            "mission.dependent",
            dependencies=("mission.root",),
        )
    )

    engine.transition(
        "mission.root",
        ConstitutionalMissionState.SCHEDULED,
    )
    engine.transition(
        "mission.root",
        ConstitutionalMissionState.RUNNING,
    )
    engine.transition(
        "mission.root",
        ConstitutionalMissionState.COMPLETED,
    )

    assert engine.get("mission.dependent").state is ConstitutionalMissionState.READY


def test_ready_and_blocked_queries() -> None:
    engine = ConstitutionalMissionEngine()

    engine.register(mission("mission.root"))
    engine.register(
        mission(
            "mission.dependent",
            dependencies=("mission.root",),
        )
    )

    assert [item.address for item in engine.ready()] == ["mission.root"]

    assert [item.address for item in engine.blocked()] == ["mission.dependent"]


def test_remove_depended_upon_mission_is_rejected() -> None:
    engine = ConstitutionalMissionEngine()

    engine.register(mission("mission.root"))
    engine.register(
        mission(
            "mission.dependent",
            dependencies=("mission.root",),
        )
    )

    with pytest.raises(MissionInUseError):
        engine.remove("mission.root")


def test_registration_and_transitions_publish_events() -> None:
    bus = ConstitutionalEventBus()
    engine = ConstitutionalMissionEngine(event_bus=bus)

    engine.register(mission("mission.root"))

    engine.transition(
        "mission.root",
        ConstitutionalMissionState.SCHEDULED,
    )

    assert bus.statistics().published >= 3

    subjects = {str(event.subject) for event in bus.history()}

    assert subjects == {"mission.root"}


def test_statistics_are_consistent() -> None:
    engine = ConstitutionalMissionEngine()

    engine.register(mission("mission.root"))
    engine.register(
        mission(
            "mission.dependent",
            dependencies=("mission.root",),
        )
    )

    stats = engine.statistics()

    assert stats.total == 2
    assert stats.ready == 1
    assert stats.blocked == 1
    assert stats.dependency_edges == 1


def test_snapshot_is_complete() -> None:
    engine = ConstitutionalMissionEngine()

    engine.register(mission("mission.root"))

    snapshot = engine.snapshot()

    assert len(snapshot["missions"]) == 1
    assert snapshot["statistics"]["total"] == 1


def test_engine_does_not_schedule_or_execute() -> None:
    engine = ConstitutionalMissionEngine()

    forbidden = {
        "schedule",
        "enqueue",
        "dequeue",
        "execute",
        "analyze",
        "connect",
        "report_health",
    }

    assert forbidden.isdisjoint(set(dir(engine)))
