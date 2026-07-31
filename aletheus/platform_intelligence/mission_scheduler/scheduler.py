"""Constitutional Mission Scheduler."""

from __future__ import annotations

import heapq
from collections import Counter
from dataclasses import replace
from datetime import UTC, datetime
from threading import RLock

from .exceptions import (
    MissionAlreadyRegisteredError,
    MissionDependencyError,
    MissionNotFoundError,
    MissionStateError,
)
from .models import (
    MissionDefinition,
    MissionRecord,
    MissionSchedulerStatistics,
    MissionState,
    ScheduledMission,
)


class ConstitutionalMissionScheduler:
    """
    Deterministic scheduler for constitutional missions.

    The scheduler determines readiness and ordering only. It does not execute
    missions, publish events, mutate services, or perform runtime analysis.
    """

    def __init__(self) -> None:
        self._records: dict[
            str,
            MissionRecord,
        ] = {}

        self._queue: list[
            tuple[
                int,
                datetime,
                int,
                ScheduledMission,
            ]
        ] = []

        self._queue_counter = 0
        self._lock = RLock()

    def register(
        self,
        definition: MissionDefinition,
    ) -> MissionRecord:
        mission_id = definition.mission_id

        with self._lock:
            if mission_id in self._records:
                raise MissionAlreadyRegisteredError(
                    f"Mission already registered: {mission_id}"
                )

            missing = sorted(
                dependency
                for dependency in definition.dependencies
                if dependency not in self._records
            )

            if missing:
                raise MissionDependencyError(
                    "Mission dependencies are not registered: " + ", ".join(missing)
                )

            next_run_at = self._initial_run_at(
                definition,
            )

            record = MissionRecord(
                definition=definition,
                state=(
                    MissionState.WAITING
                    if definition.enabled
                    else MissionState.CANCELLED
                ),
                attempt=1,
                next_run_at=next_run_at,
            )

            self._records[mission_id] = record

        return record

    def register_many(
        self,
        definitions: list[MissionDefinition] | tuple[MissionDefinition, ...],
    ) -> tuple[MissionRecord, ...]:
        pending = list(definitions)
        registered: list[MissionRecord] = []

        while pending:
            progressed = False

            for definition in tuple(pending):
                if all(
                    dependency in self._records
                    for dependency in definition.dependencies
                ):
                    registered.append(self.register(definition))
                    pending.remove(definition)
                    progressed = True

            if progressed:
                continue

            unresolved = {
                definition.mission_id: sorted(
                    dependency
                    for dependency in definition.dependencies
                    if dependency not in self._records
                )
                for definition in pending
            }

            raise MissionDependencyError(
                f"Unable to resolve mission dependency order: {unresolved}"
            )

        return tuple(registered)

    def unregister(
        self,
        mission_id: str,
    ) -> MissionRecord:
        resolved = self._normalize_id(mission_id)

        with self._lock:
            record = self._require_record(resolved)

            dependents = sorted(
                item.definition.mission_id
                for item in self._records.values()
                if resolved in item.definition.dependencies
            )

            if dependents:
                raise MissionDependencyError(
                    f"Mission {resolved} has dependents: " + ", ".join(dependents)
                )

            del self._records[resolved]

            self._queue = [
                item for item in self._queue if item[3].mission_id != resolved
            ]
            heapq.heapify(self._queue)

        return record

    def get(
        self,
        mission_id: str,
    ) -> MissionRecord:
        resolved = self._normalize_id(mission_id)

        with self._lock:
            return self._require_record(resolved)

    def all(
        self,
    ) -> tuple[MissionRecord, ...]:
        with self._lock:
            return tuple(
                self._records[mission_id] for mission_id in sorted(self._records)
            )

    def ready(
        self,
        now: datetime | None = None,
    ) -> tuple[MissionRecord, ...]:
        current = self._normalize_time(now or datetime.now(UTC))

        with self._lock:
            ready_records: list[MissionRecord] = []

            for mission_id in sorted(self._records):
                record = self._records[mission_id]

                if not self._is_ready(
                    record,
                    current,
                ):
                    continue

                updated = replace(
                    record,
                    state=MissionState.READY,
                )

                self._records[mission_id] = updated
                ready_records.append(updated)

            return tuple(
                sorted(
                    ready_records,
                    key=lambda item: (
                        -item.definition.priority_weight,
                        item.next_run_at or current,
                        item.definition.mission_id,
                    ),
                )
            )

    def enqueue_ready(
        self,
        now: datetime | None = None,
    ) -> tuple[ScheduledMission, ...]:
        current = self._normalize_time(now or datetime.now(UTC))

        ready_records = self.ready(current)
        scheduled: list[ScheduledMission] = []

        with self._lock:
            for record in ready_records:
                item = ScheduledMission.create(
                    record=record,
                    scheduled_for=(record.next_run_at or current),
                )

                self._queue_counter += 1

                heapq.heappush(
                    self._queue,
                    (
                        -record.definition.priority_weight,
                        item.scheduled_for,
                        self._queue_counter,
                        item,
                    ),
                )

                self._records[record.definition.mission_id] = replace(
                    record,
                    state=MissionState.QUEUED,
                )

                scheduled.append(item)

        return tuple(scheduled)

    def dequeue(
        self,
    ) -> ScheduledMission | None:
        with self._lock:
            if not self._queue:
                return None

            _, _, _, item = heapq.heappop(self._queue)

            record = self._require_record(item.mission_id)

            self._records[item.mission_id] = replace(
                record,
                last_started_at=datetime.now(UTC),
            )

            return item

    def mark_succeeded(
        self,
        mission_id: str,
        *,
        completed_at: datetime | None = None,
    ) -> MissionRecord:
        resolved = self._normalize_id(mission_id)
        completed = self._normalize_time(completed_at or datetime.now(UTC))

        with self._lock:
            record = self._require_record(resolved)

            if record.state not in {
                MissionState.QUEUED,
                MissionState.READY,
            }:
                raise MissionStateError(
                    "Only queued or ready missions can be marked succeeded."
                )

            next_run_at = self._next_recurring_run(
                record,
                completed,
            )

            updated = replace(
                record,
                state=(
                    MissionState.WAITING
                    if next_run_at is not None
                    else MissionState.SUCCEEDED
                ),
                attempt=1,
                next_run_at=next_run_at,
                last_completed_at=completed,
                last_error=None,
            )

            self._records[resolved] = updated

        return updated

    def mark_failed(
        self,
        mission_id: str,
        *,
        error: str,
        failed_at: datetime | None = None,
    ) -> MissionRecord:
        resolved = self._normalize_id(mission_id)
        failed = self._normalize_time(failed_at or datetime.now(UTC))

        with self._lock:
            record = self._require_record(resolved)

            if record.state not in {
                MissionState.QUEUED,
                MissionState.READY,
            }:
                raise MissionStateError(
                    "Only queued or ready missions can be marked failed."
                )

            policy = record.definition.retry_policy

            if record.attempt >= policy.max_attempts:
                updated = replace(
                    record,
                    state=MissionState.EXHAUSTED,
                    last_completed_at=failed,
                    last_error=error,
                    next_run_at=None,
                )
            else:
                next_attempt = record.attempt + 1
                delay = policy.delay_for_attempt(
                    next_attempt,
                )

                updated = replace(
                    record,
                    state=MissionState.WAITING,
                    attempt=next_attempt,
                    next_run_at=failed + delay,
                    last_completed_at=failed,
                    last_error=error,
                )

            self._records[resolved] = updated

        return updated

    def cancel(
        self,
        mission_id: str,
    ) -> MissionRecord:
        resolved = self._normalize_id(mission_id)

        with self._lock:
            record = self._require_record(resolved)

            updated = replace(
                record,
                state=MissionState.CANCELLED,
                next_run_at=None,
            )

            self._records[resolved] = updated
            self._queue = [
                item for item in self._queue if item[3].mission_id != resolved
            ]
            heapq.heapify(self._queue)

        return updated

    def statistics(
        self,
    ) -> MissionSchedulerStatistics:
        with self._lock:
            records = tuple(self._records.values())
            queue_depth = len(self._queue)

        state_counts = Counter(record.state.value for record in records)

        return MissionSchedulerStatistics(
            registered=len(records),
            enabled=sum(record.definition.enabled for record in records),
            ready=state_counts[MissionState.READY.value],
            queued=state_counts[MissionState.QUEUED.value],
            succeeded=state_counts[MissionState.SUCCEEDED.value],
            failed=state_counts[MissionState.FAILED.value],
            cancelled=state_counts[MissionState.CANCELLED.value],
            exhausted=state_counts[MissionState.EXHAUSTED.value],
            queue_depth=queue_depth,
        )

    def _is_ready(
        self,
        record: MissionRecord,
        now: datetime,
    ) -> bool:
        if not record.definition.enabled:
            return False

        if record.state in {
            MissionState.CANCELLED,
            MissionState.SUCCEEDED,
            MissionState.EXHAUSTED,
            MissionState.QUEUED,
        }:
            return False

        if record.next_run_at is not None and now < record.next_run_at:
            return False

        for dependency_id in record.definition.dependencies:
            dependency = self._records[dependency_id]

            if dependency.state not in {
                MissionState.SUCCEEDED,
                MissionState.WAITING,
            }:
                return False

            if dependency.last_completed_at is None:
                return False

        if (
            record.last_completed_at is not None
            and record.definition.cooldown > now - record.last_completed_at
        ):
            return False

        return True

    @staticmethod
    def _initial_run_at(
        definition: MissionDefinition,
    ) -> datetime:
        trigger = definition.trigger

        if trigger.run_at is not None:
            return trigger.run_at

        return datetime.now(UTC)

    @staticmethod
    def _next_recurring_run(
        record: MissionRecord,
        completed_at: datetime,
    ) -> datetime | None:
        interval = record.definition.trigger.interval

        if interval is None:
            return None

        cooldown = record.definition.cooldown

        return completed_at + max(
            interval,
            cooldown,
        )

    def _require_record(
        self,
        mission_id: str,
    ) -> MissionRecord:
        record = self._records.get(mission_id)

        if record is None:
            raise MissionNotFoundError(f"Mission not found: {mission_id}")

        return record

    @staticmethod
    def _normalize_id(
        mission_id: str,
    ) -> str:
        return mission_id.strip().lower()

    @staticmethod
    def _normalize_time(
        value: datetime,
    ) -> datetime:
        if value.tzinfo is None:
            raise ValueError("Scheduler timestamps require timezone.")

        return value.astimezone(UTC)
