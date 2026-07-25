from __future__ import annotations

from typing import Any

from aletheus.missions_v2.models import (
    AutonomousMissionV2,
    MissionTaskV2,
    MissionTelemetryV2,
)


class AletheusAutonomousMissionEngine:
    def __init__(self) -> None:
        self.version = "2.0.0-c"
        self.missions: list[AutonomousMissionV2] = []
        self.telemetry: list[MissionTelemetryV2] = []

    def emit(self, mission_id: str, event_type: str, message: str, payload: dict[str, Any] | None = None) -> MissionTelemetryV2:
        item = MissionTelemetryV2(
            mission_id=mission_id,
            event_type=event_type,
            message=message,
            payload=payload or {},
        )
        self.telemetry.append(item)
        return item

    def create_mission(
        self,
        title: str,
        objective: str,
        application: str = "AletheusOS",
        priority: str = "high",
        tasks: list[dict[str, Any]] | None = None,
    ) -> AutonomousMissionV2:
        mission_tasks = [
            MissionTaskV2(
                title=item.get("title", "Untitled Task"),
                description=item.get("description", ""),
                assigned_agent=item.get("assigned_agent", "Executive Agent"),
                application=item.get("application", application),
            )
            for item in (tasks or self.default_tasks(objective, application))
        ]

        mission = AutonomousMissionV2(
            title=title,
            objective=objective,
            application=application,
            priority=priority,
            status="queued",
            tasks=mission_tasks,
        )

        self.missions.append(mission)
        self.emit(mission.mission_id, "mission.created", f"Mission created: {title}", mission.to_dict())
        return mission

    def default_tasks(self, objective: str, application: str) -> list[dict[str, Any]]:
        lower = objective.lower()

        if "card hawk" in lower or "marketplace" in lower or "asset" in lower:
            return [
                {
                    "title": "Frame mission objective",
                    "description": "Executive Agent summarizes the mission objective and success criteria.",
                    "assigned_agent": "Executive Agent",
                    "application": application,
                },
                {
                    "title": "Recall relevant Card Hawk memory",
                    "description": "Memory Agent retrieves prior Card Hawk decisions, targets, and lessons.",
                    "assigned_agent": "Memory Agent",
                    "application": application,
                },
                {
                    "title": "Expand Card Hawk knowledge context",
                    "description": "Knowledge Agent links applications, services, players, assets, and decisions.",
                    "assigned_agent": "Knowledge Agent",
                    "application": application,
                },
                {
                    "title": "Predict mission risks and opportunities",
                    "description": "Market Agent and predictive intelligence evaluate risks and opportunities.",
                    "assigned_agent": "Market Agent",
                    "application": application,
                },
                {
                    "title": "Generate founder-ready recommendation",
                    "description": "Founder Agent prepares the next action for founder review.",
                    "assigned_agent": "Founder Agent",
                    "application": application,
                },
            ]

        return [
            {
                "title": "Frame mission objective",
                "description": "Executive Agent defines success criteria.",
                "assigned_agent": "Executive Agent",
                "application": application,
            },
            {
                "title": "Gather context",
                "description": "Memory Agent and Knowledge Agent gather context.",
                "assigned_agent": "Memory Agent",
                "application": application,
            },
            {
                "title": "Execute recommendation",
                "description": "Founder Agent prepares the next recommended action.",
                "assigned_agent": "Founder Agent",
                "application": application,
            },
        ]

    def get_mission(self, mission_id: str) -> AutonomousMissionV2 | None:
        return next((mission for mission in self.missions if mission.mission_id == mission_id), None)

    def list_missions(self, status: str | None = None) -> list[dict[str, Any]]:
        missions = self.missions
        if status:
            missions = [mission for mission in missions if mission.status == status]
        return [mission.to_dict() for mission in missions]

    def plan_mission(self, mission_id: str, runtime: Any) -> dict[str, Any]:
        mission = self.get_mission(mission_id)
        if mission is None:
            return {"error": f"Mission not found: {mission_id}"}

        mission.status = "planning"
        self.emit(mission_id, "mission.planning", "Mission entered planning stage.", mission.to_dict())

        plan = runtime.commands.dispatch(
            "planning.create",
            {
                "objective": mission.objective,
                "priority": mission.priority,
            },
        )

        self.emit(mission_id, "mission.plan.generated", "Planning engine generated a plan.", plan.results)
        mission.status = "ready"

        return {
            "mission": mission.to_dict(),
            "planning": plan.results,
        }

    def execute_next(self, mission_id: str, runtime: Any) -> dict[str, Any]:
        mission = self.get_mission(mission_id)
        if mission is None:
            return {"error": f"Mission not found: {mission_id}"}

        if mission.status in {"queued", "ready", "planning"}:
            mission.start()
            self.emit(mission_id, "mission.started", "Mission execution started.", mission.to_dict())

        pending = [task for task in mission.tasks if task.status in {"queued", "pending"}]
        if not pending:
            mission.complete_if_ready()
            return {"mission": mission.to_dict(), "message": "No pending tasks."}

        task = pending[0]
        task.start()
        self.emit(mission_id, "mission.task.started", f"Task started: {task.title}", task.to_dict())

        assignment = runtime.commands.dispatch(
            "agent.task.assign",
            {
                "agent_name": task.assigned_agent,
                "title": task.title,
                "payload": {
                    "mission_id": mission.mission_id,
                    "objective": mission.objective,
                    "task_id": task.task_id,
                    "description": task.description,
                    "application": task.application,
                },
            },
        )

        agent_run = runtime.commands.dispatch(
            "agent.run",
            {"agent_name": task.assigned_agent},
        )

        result = {
            "assignment": assignment.results,
            "agent_run": agent_run.results,
        }

        task.complete(result)
        self.emit(mission_id, "mission.task.completed", f"Task completed: {task.title}", task.to_dict())

        mission.complete_if_ready()
        if mission.status == "completed":
            self.emit(mission_id, "mission.completed", f"Mission completed: {mission.title}", mission.to_dict())

        return {
            "mission": mission.to_dict(),
            "executed_task": task.to_dict(),
            "result": result,
        }

    def execute_mission(self, mission_id: str, runtime: Any) -> dict[str, Any]:
        outputs = []

        while True:
            mission = self.get_mission(mission_id)
            if mission is None:
                return {"error": f"Mission not found: {mission_id}"}

            if mission.status == "completed":
                break

            result = self.execute_next(mission_id, runtime)
            outputs.append(result)

            if "error" in result:
                break

            mission = self.get_mission(mission_id)
            if mission is None or mission.status == "completed":
                break

        mission = self.get_mission(mission_id)

        learning = runtime.commands.dispatch(
            "learn.record",
            {
                "event_type": "mission_execution",
                "description": f"Mission executed: {mission.title if mission else mission_id}",
                "source": "missions_v2",
                "outcome": mission.status if mission else "unknown",
                "confidence": 0.86,
                "metadata": mission.to_dict() if mission else {},
            },
        )

        return {
            "mission": mission.to_dict() if mission else None,
            "outputs": outputs,
            "learning": learning.results,
        }

    def pause_mission(self, mission_id: str) -> dict[str, Any]:
        mission = self.get_mission(mission_id)
        if mission is None:
            return {"error": f"Mission not found: {mission_id}"}
        mission.status = "paused"
        self.emit(mission_id, "mission.paused", f"Mission paused: {mission.title}", mission.to_dict())
        return mission.to_dict()

    def resume_mission(self, mission_id: str) -> dict[str, Any]:
        mission = self.get_mission(mission_id)
        if mission is None:
            return {"error": f"Mission not found: {mission_id}"}
        mission.status = "ready"
        self.emit(mission_id, "mission.resumed", f"Mission resumed: {mission.title}", mission.to_dict())
        return mission.to_dict()

    def cancel_mission(self, mission_id: str) -> dict[str, Any]:
        mission = self.get_mission(mission_id)
        if mission is None:
            return {"error": f"Mission not found: {mission_id}"}
        mission.status = "cancelled"
        self.emit(mission_id, "mission.cancelled", f"Mission cancelled: {mission.title}", mission.to_dict())
        return mission.to_dict()

    def mission_telemetry(self, mission_id: str = "") -> list[dict[str, Any]]:
        data = self.telemetry
        if mission_id:
            data = [item for item in data if item.mission_id == mission_id]
        return [item.to_dict() for item in data]

    def stats(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "missions": len(self.missions),
            "queued": len([mission for mission in self.missions if mission.status == "queued"]),
            "running": len([mission for mission in self.missions if mission.status == "running"]),
            "completed": len([mission for mission in self.missions if mission.status == "completed"]),
            "paused": len([mission for mission in self.missions if mission.status == "paused"]),
            "cancelled": len([mission for mission in self.missions if mission.status == "cancelled"]),
            "telemetry_events": len(self.telemetry),
        }


mission_v2_core = AletheusAutonomousMissionEngine()
