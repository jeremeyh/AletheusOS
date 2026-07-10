"""
Aletheus v2 Autonomous Mission Command Registration.

Binds the public mission.v2 command contract directly to the bounded
AletheusAutonomousMissionEngine.
"""

from __future__ import annotations

from typing import Any


def _serialize(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return value


def register_mission_v2_commands(runtime):
    commands = runtime.commands
    engine = runtime.mission_v2

    def create(payload=None):
        payload = payload or {}

        mission = engine.create_mission(
            title=payload.get("title", "Untitled Mission"),
            objective=payload.get("objective", ""),
            application=payload.get(
                "application",
                "AletheusOS",
            ),
            priority=payload.get("priority", "high"),
            tasks=payload.get("tasks"),
        )

        return _serialize(mission)

    def plan(payload=None):
        payload = payload or {}

        return engine.plan_mission(
            mission_id=payload.get("mission_id", ""),
            runtime=runtime,
        )

    def execute(payload=None):
        payload = payload or {}

        return engine.execute_mission(
            mission_id=payload.get("mission_id", ""),
            runtime=runtime,
        )

    def execute_next(payload=None):
        payload = payload or {}

        return engine.execute_next(
            mission_id=payload.get("mission_id", ""),
            runtime=runtime,
        )

    def telemetry(payload=None):
        payload = payload or {}

        return engine.mission_telemetry(
            mission_id=payload.get("mission_id", ""),
        )

    def statistics(payload=None):
        return engine.stats()

    commands.register(
        "mission.v2.create",
        create,
        replace=True,
    )

    commands.register(
        "mission.v2.plan",
        plan,
        replace=True,
    )

    commands.register(
        "mission.v2.execute",
        execute,
        replace=True,
    )

    commands.register(
        "mission.v2.execute_next",
        execute_next,
        replace=True,
    )

    commands.register(
        "mission.v2.telemetry",
        telemetry,
        replace=True,
    )

    commands.register(
        "mission.v2.stats",
        statistics,
        replace=True,
    )
