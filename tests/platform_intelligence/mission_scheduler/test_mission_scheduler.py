from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalMissionScheduler,
    MissionAlreadyRegisteredError,
    MissionDefinition,
    MissionDependencyError,
    MissionNotFoundError,
    MissionPriority,
    MissionState,
    MissionStateError,
    MissionTrigger,
    RetryPolicy,
)

NOW = datetime(
    2026,
    7,
    13,
    12,
    0,
    tzinfo=UTC,
)


def mission(
    mission_id: str,
    *,
    run_at: datetime = NOW,
    priority: MissionPriority = (MissionPriority.NORMAL),
    dependencies: tuple[str, ...] = (),
    retry_policy: RetryPolicy | None = None,
    cooldown: timedelta = timedelta(0),
    interval: timedelta | None = None,
) -> MissionDefinition:
    trigger = (
        MissionTrigger.recurring(
            interval=interval,
            first_run_at=run_at,
        )
        if interval is not None
        else MissionTrigger.once(run_at)
    )

    return MissionDefinition.create(
        mission_id=mission_id,
        name=mission_id,
        trigger=trigger,
        priority=priority,
        dependencies=dependencies,
        retry_policy=retry_policy,
        cooldown=cooldown,
    )


def test_register_mission() -> None:
    scheduler = ConstitutionalMissionScheduler()

    record = scheduler.register(mission("mission.health"))

    assert record.definition.mission_id == ("mission.health")
    assert record.state is MissionState.WAITING


def test_duplicate_mission_is_rejected() -> None:
    scheduler = ConstitutionalMissionScheduler()
    definition = mission("mission.health")

    scheduler.register(definition)

    with pytest.raises(MissionAlreadyRegisteredError):
        scheduler.register(definition)


def test_unknown_mission_is_rejected() -> None:
    scheduler = ConstitutionalMissionScheduler()

    with pytest.raises(MissionNotFoundError):
        scheduler.get("mission.missing")


def test_missing_dependency_is_rejected() -> None:
    scheduler = ConstitutionalMissionScheduler()

    with pytest.raises(MissionDependencyError):
        scheduler.register(
            mission(
                "mission.explorer",
                dependencies=("mission.health",),
            )
        )


def test_register_many_resolves_dependencies() -> None:
    scheduler = ConstitutionalMissionScheduler()

    records = scheduler.register_many(
        [
            mission(
                "mission.explorer",
                dependencies=("mission.health",),
            ),
            mission("mission.health"),
        ]
    )

    assert [record.definition.mission_id for record in records] == [
        "mission.health",
        "mission.explorer",
    ]


def test_ready_respects_schedule() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(
        mission(
            "mission.future",
            run_at=NOW + timedelta(hours=1),
        )
    )

    assert scheduler.ready(NOW) == ()

    ready = scheduler.ready(NOW + timedelta(hours=1))

    assert [record.definition.mission_id for record in ready] == ["mission.future"]


def test_priority_orders_ready_missions() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(
        mission(
            "mission.low",
            priority=MissionPriority.LOW,
        )
    )
    scheduler.register(
        mission(
            "mission.critical",
            priority=MissionPriority.CRITICAL,
        )
    )

    ready = scheduler.ready(NOW)

    assert [record.definition.mission_id for record in ready] == [
        "mission.critical",
        "mission.low",
    ]


def test_enqueue_and_dequeue() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(mission("mission.health"))

    queued = scheduler.enqueue_ready(NOW)

    assert len(queued) == 1
    assert scheduler.statistics().queue_depth == 1

    item = scheduler.dequeue()

    assert item is not None
    assert item.mission_id == "mission.health"
    assert scheduler.statistics().queue_depth == 0


def test_dependency_waits_for_completion() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(mission("mission.health"))
    scheduler.register(
        mission(
            "mission.explorer",
            dependencies=("mission.health",),
        )
    )

    ready = scheduler.ready(NOW)

    assert [record.definition.mission_id for record in ready] == ["mission.health"]


def test_dependency_unlocks_after_success() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(mission("mission.health"))
    scheduler.register(
        mission(
            "mission.explorer",
            dependencies=("mission.health",),
        )
    )

    scheduler.enqueue_ready(NOW)
    scheduler.dequeue()

    scheduler.mark_succeeded(
        "mission.health",
        completed_at=NOW,
    )

    ready = scheduler.ready(NOW)

    assert [record.definition.mission_id for record in ready] == ["mission.explorer"]


def test_one_shot_success_is_terminal() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(mission("mission.health"))
    scheduler.enqueue_ready(NOW)
    scheduler.dequeue()

    record = scheduler.mark_succeeded(
        "mission.health",
        completed_at=NOW,
    )

    assert record.state is MissionState.SUCCEEDED
    assert record.next_run_at is None


def test_recurring_success_schedules_next_run() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(
        mission(
            "mission.health",
            interval=timedelta(minutes=5),
        )
    )
    scheduler.enqueue_ready(NOW)
    scheduler.dequeue()

    record = scheduler.mark_succeeded(
        "mission.health",
        completed_at=NOW,
    )

    assert record.state is MissionState.WAITING
    assert record.next_run_at == (NOW + timedelta(minutes=5))


def test_retry_is_scheduled_after_failure() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(
        mission(
            "mission.health",
            retry_policy=RetryPolicy(
                max_attempts=3,
                initial_delay=timedelta(minutes=1),
                backoff_multiplier=2.0,
            ),
        )
    )
    scheduler.enqueue_ready(NOW)
    scheduler.dequeue()

    record = scheduler.mark_failed(
        "mission.health",
        error="failure",
        failed_at=NOW,
    )

    assert record.state is MissionState.WAITING
    assert record.attempt == 2
    assert record.next_run_at == (NOW + timedelta(minutes=2))


def test_retry_exhaustion_is_terminal() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(
        mission(
            "mission.health",
            retry_policy=RetryPolicy(
                max_attempts=1,
            ),
        )
    )
    scheduler.enqueue_ready(NOW)
    scheduler.dequeue()

    record = scheduler.mark_failed(
        "mission.health",
        error="failure",
        failed_at=NOW,
    )

    assert record.state is MissionState.EXHAUSTED
    assert record.next_run_at is None


def test_cancel_removes_queued_mission() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(mission("mission.health"))
    scheduler.enqueue_ready(NOW)

    record = scheduler.cancel("mission.health")

    assert record.state is MissionState.CANCELLED
    assert scheduler.statistics().queue_depth == 0


def test_invalid_success_transition_is_rejected() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(mission("mission.health"))

    with pytest.raises(MissionStateError):
        scheduler.mark_succeeded(
            "mission.health",
            completed_at=NOW,
        )


def test_dependent_mission_prevents_unregister() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(mission("mission.health"))
    scheduler.register(
        mission(
            "mission.explorer",
            dependencies=("mission.health",),
        )
    )

    with pytest.raises(MissionDependencyError):
        scheduler.unregister("mission.health")


def test_statistics_are_consistent() -> None:
    scheduler = ConstitutionalMissionScheduler()

    scheduler.register(mission("mission.health"))
    scheduler.register(
        mission(
            "mission.future",
            run_at=NOW + timedelta(hours=1),
        )
    )

    scheduler.enqueue_ready(NOW)

    stats = scheduler.statistics()

    assert stats.registered == 2
    assert stats.enabled == 2
    assert stats.queued == 1
    assert stats.queue_depth == 1


def test_scheduler_does_not_execute_or_publish() -> None:
    scheduler = ConstitutionalMissionScheduler()

    forbidden = {
        "execute",
        "publish",
        "connect",
        "transition",
        "report_health",
        "analyze",
    }

    assert forbidden.isdisjoint(set(dir(scheduler)))
