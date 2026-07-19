"""Public Constitutional Mission Surface."""

from __future__ import annotations

from aletheus.constitutional_missions import MissionStatus


class MissionSurface:
    """Stable read interface over Constitutional Missions and TIME™."""

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        mission_engine,
        time,
    ) -> None:
        self._engine = mission_engine
        self._time = time

    def get(
        self,
        mission_id: str,
    ):
        return self._engine.registry.get(
            mission_id
        )

    def require(
        self,
        mission_id: str,
    ):
        return self._engine.registry.require(
            mission_id
        )

    def list(self):
        return self._engine.registry.list()

    def by_status(
        self,
        status: MissionStatus | str,
    ):
        resolved = (
            status
            if isinstance(
                status,
                MissionStatus,
            )
            else MissionStatus(status)
        )

        return self._engine.registry.by_status(
            resolved
        )

    def history(
        self,
        mission_id: str,
    ):
        return self._engine.history(
            mission_id
        )

    def temporal_state(
        self,
        mission_id: str,
    ):
        return self._time.state(
            mission_id
        )

    def phase_graph(
        self,
        mission_id: str,
    ):
        return self._time.graph(
            mission_id
        )

    def eligible_phases(
        self,
        mission_id: str,
    ):
        return self._time.eligible_phases(
            mission_id
        )

    def statistics(self) -> dict:
        return self._engine.registry.statistics()

    def health(self) -> dict:
        return {
            "name": (
                "AletheusOS Mission Surface™"
            ),
            "version": self.VERSION,
            "status": "online",
            "missions": (
                self._engine
                .registry
                .statistics()
            ),
            "time": self._time.health(),
        }
