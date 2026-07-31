"""Constitutional Mission Registry."""

from __future__ import annotations

from .models import ConstitutionalMission, MissionStatus
from .validation import validate_mission


class DuplicateMissionError(ValueError):
    pass


class ConstitutionalMissionRegistry:
    def __init__(self) -> None:
        self._missions: dict[str, ConstitutionalMission] = {}

    def register(
        self,
        mission: ConstitutionalMission,
    ) -> ConstitutionalMission:
        validate_mission(mission)

        if mission.mission_id in self._missions:
            raise DuplicateMissionError(
                f"Mission {mission.mission_id!r} already exists."
            )

        self._missions[mission.mission_id] = mission
        return mission

    def get(
        self,
        mission_id: str,
    ) -> ConstitutionalMission | None:
        return self._missions.get(mission_id)

    def require(
        self,
        mission_id: str,
    ) -> ConstitutionalMission:
        mission = self.get(mission_id)

        if mission is None:
            raise KeyError(f"Unknown mission: {mission_id}")

        return mission

    def list(
        self,
    ) -> tuple[ConstitutionalMission, ...]:
        return tuple(self._missions.values())

    def by_status(
        self,
        status: MissionStatus,
    ) -> tuple[ConstitutionalMission, ...]:
        return tuple(
            mission for mission in self._missions.values() if mission.status == status
        )

    def statistics(self) -> dict:
        return {
            "missions": len(self._missions),
            "statuses": {
                status.value: len(self.by_status(status)) for status in MissionStatus
            },
        }

    def health(self) -> dict:
        return {
            "name": "Constitutional Mission Registry",
            "status": "online",
            **self.statistics(),
        }
