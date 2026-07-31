"""Constitutional Mission Engine."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from threading import RLock

from aletheus.platform_intelligence.event_bus import (
    ConstitutionalEventBus,
)
from aletheus.platform_intelligence.events import (
    ConstitutionalEvent,
    ConstitutionalEventKind,
    ConstitutionalEventSeverity,
)

from .exceptions import (
    MissionAlreadyExistsError,
    MissionDependencyError,
    MissionInUseError,
    MissionNotFoundError,
    MissionTransitionError,
)
from .lifecycle import transition_allowed
from .models import (
    ConstitutionalMission,
    ConstitutionalMissionState,
    MissionEngineStatistics,
)


class ConstitutionalMissionEngine:
    """
    Canonical authority for constitutional mission truth.

    The engine owns mission identity, lifecycle, dependencies, and snapshots.
    It does not schedule, execute, analyze, or orchestrate missions.
    """

    def __init__(
        self,
        *,
        event_bus: ConstitutionalEventBus | None = None,
    ) -> None:
        self._event_bus = event_bus
        self._missions: dict[
            str,
            ConstitutionalMission,
        ] = {}
        self._lock = RLock()

    def register(
        self,
        mission: ConstitutionalMission,
    ) -> ConstitutionalMission:
        with self._lock:
            if mission.address in self._missions:
                raise MissionAlreadyExistsError(
                    f"Mission already exists: {mission.address}"
                )

            missing = sorted(
                dependency
                for dependency in mission.dependencies
                if dependency not in self._missions
            )

            if missing:
                raise MissionDependencyError(
                    "Mission dependencies are not registered: " + ", ".join(missing)
                )

            self._missions[mission.address] = mission

        self._publish(
            ConstitutionalEventKind.OBJECT_REGISTERED,
            mission,
            payload={
                "object_type": "mission",
                "mission": mission.to_snapshot(),
            },
        )

        return self.refresh(mission.address)

    def register_many(
        self,
        missions: Iterable[ConstitutionalMission],
    ) -> tuple[ConstitutionalMission, ...]:
        pending = list(missions)
        registered: list[ConstitutionalMission] = []

        while pending:
            progressed = False

            for mission in tuple(pending):
                if all(
                    dependency in self._missions for dependency in mission.dependencies
                ):
                    registered.append(self.register(mission))
                    pending.remove(mission)
                    progressed = True

            if progressed:
                continue

            unresolved = {
                mission.address: sorted(
                    dependency
                    for dependency in mission.dependencies
                    if dependency not in self._missions
                )
                for mission in pending
            }

            raise MissionDependencyError(
                f"Unable to resolve mission dependency order: {unresolved}"
            )

        return tuple(registered)

    def get(
        self,
        address: str,
    ) -> ConstitutionalMission:
        resolved = self._normalize(address)

        with self._lock:
            mission = self._missions.get(resolved)

        if mission is None:
            raise MissionNotFoundError(f"Mission not found: {resolved}")

        return mission

    def all(
        self,
    ) -> tuple[ConstitutionalMission, ...]:
        with self._lock:
            return tuple(self._missions[address] for address in sorted(self._missions))

    def transition(
        self,
        address: str,
        target: ConstitutionalMissionState,
        *,
        failure_reason: str | None = None,
    ) -> ConstitutionalMission:
        resolved = self._normalize(address)

        with self._lock:
            current = self.get(resolved)

            if not transition_allowed(
                current.state,
                target,
            ):
                raise MissionTransitionError(
                    f"Invalid mission transition: "
                    f"{current.state.value} -> "
                    f"{target.value}"
                )

            if (
                target is ConstitutionalMissionState.READY
                and not self._dependencies_complete(current)
            ):
                raise MissionDependencyError(
                    "Mission cannot become ready until all dependencies are completed."
                )

            if target is ConstitutionalMissionState.FAILED and not failure_reason:
                raise MissionTransitionError(
                    "Failed missions require a failure reason."
                )

            updated = current.with_state(
                target,
                failure_reason=failure_reason,
            )

            self._missions[resolved] = updated

        self._publish(
            ConstitutionalEventKind.STATE_CHANGED,
            updated,
            payload={
                "object_type": "mission",
                "previous_state": (current.state.value),
                "current_state": target.value,
                "failure_reason": failure_reason,
            },
            severity=(
                ConstitutionalEventSeverity.ERROR
                if target is ConstitutionalMissionState.FAILED
                else ConstitutionalEventSeverity.INFO
            ),
        )

        if target is (ConstitutionalMissionState.COMPLETED):
            self.refresh_dependents(resolved)

        return updated

    def refresh(
        self,
        address: str,
    ) -> ConstitutionalMission:
        mission = self.get(address)

        if mission.state not in {
            ConstitutionalMissionState.CREATED,
            ConstitutionalMissionState.BLOCKED,
        }:
            return mission

        target = (
            ConstitutionalMissionState.READY
            if self._dependencies_complete(mission)
            else ConstitutionalMissionState.BLOCKED
        )

        if mission.state is target:
            return mission

        return self.transition(
            mission.address,
            target,
        )

    def refresh_all(
        self,
    ) -> tuple[ConstitutionalMission, ...]:
        return tuple(self.refresh(mission.address) for mission in self.all())

    def refresh_dependents(
        self,
        address: str,
    ) -> tuple[ConstitutionalMission, ...]:
        return tuple(
            self.refresh(mission.address)
            for mission in self.all()
            if address in mission.dependencies
        )

    def ready(
        self,
    ) -> tuple[ConstitutionalMission, ...]:
        return self._by_state(ConstitutionalMissionState.READY)

    def blocked(
        self,
    ) -> tuple[ConstitutionalMission, ...]:
        return self._by_state(ConstitutionalMissionState.BLOCKED)

    def running(
        self,
    ) -> tuple[ConstitutionalMission, ...]:
        return self._by_state(ConstitutionalMissionState.RUNNING)

    def completed(
        self,
    ) -> tuple[ConstitutionalMission, ...]:
        return self._by_state(ConstitutionalMissionState.COMPLETED)

    def failed(
        self,
    ) -> tuple[ConstitutionalMission, ...]:
        return self._by_state(ConstitutionalMissionState.FAILED)

    def dependencies_of(
        self,
        address: str,
    ) -> tuple[ConstitutionalMission, ...]:
        mission = self.get(address)

        return tuple(
            self.get(dependency) for dependency in sorted(mission.dependencies)
        )

    def dependents_of(
        self,
        address: str,
    ) -> tuple[ConstitutionalMission, ...]:
        resolved = self._normalize(address)
        self.get(resolved)

        return tuple(
            mission for mission in self.all() if resolved in mission.dependencies
        )

    def remove(
        self,
        address: str,
        *,
        force: bool = False,
    ) -> ConstitutionalMission:
        resolved = self._normalize(address)
        mission = self.get(resolved)
        dependents = self.dependents_of(resolved)

        if dependents and not force:
            raise MissionInUseError(
                f"Mission {resolved} has dependents: "
                + ", ".join(item.address for item in dependents)
            )

        with self._lock:
            del self._missions[resolved]

        self._publish(
            ConstitutionalEventKind.OBJECT_RETIRED,
            mission,
            payload={
                "object_type": "mission",
                "mission": mission.to_snapshot(),
                "forced": force,
            },
            severity=(
                ConstitutionalEventSeverity.WARNING
                if force
                else ConstitutionalEventSeverity.NOTICE
            ),
        )

        return mission

    def statistics(
        self,
    ) -> MissionEngineStatistics:
        missions = self.all()

        counts = Counter(mission.state.value for mission in missions)

        return MissionEngineStatistics(
            total=len(missions),
            created=counts["created"],
            blocked=counts["blocked"],
            ready=counts["ready"],
            scheduled=counts["scheduled"],
            running=counts["running"],
            completed=counts["completed"],
            failed=counts["failed"],
            cancelled=counts["cancelled"],
            dependency_edges=sum(len(mission.dependencies) for mission in missions),
        )

    def snapshot(
        self,
    ) -> dict[str, object]:
        return {
            "missions": [mission.to_snapshot() for mission in self.all()],
            "statistics": (self.statistics().to_dict()),
        }

    def _dependencies_complete(
        self,
        mission: ConstitutionalMission,
    ) -> bool:
        return all(
            self.get(dependency).state is ConstitutionalMissionState.COMPLETED
            for dependency in mission.dependencies
        )

    def _by_state(
        self,
        state: ConstitutionalMissionState,
    ) -> tuple[ConstitutionalMission, ...]:
        return tuple(mission for mission in self.all() if mission.state is state)

    def _publish(
        self,
        kind: ConstitutionalEventKind,
        mission: ConstitutionalMission,
        *,
        payload: dict[str, object],
        severity: ConstitutionalEventSeverity = (ConstitutionalEventSeverity.INFO),
    ) -> None:
        if self._event_bus is None:
            return

        self._event_bus.publish(
            ConstitutionalEvent.create(
                kind=kind,
                source="service.mission-engine",
                subject=mission.address,
                severity=severity,
                payload=payload,
            )
        )

    @staticmethod
    def _normalize(
        address: str,
    ) -> str:
        return address.strip().lower()
