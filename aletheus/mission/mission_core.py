from __future__ import annotations

from typing import Any

from aletheus.mission.models import Mission, MissionRun, MissionTask


class AletheusMissionCore:
    def __init__(self) -> None:
        self.version = "0.7.0-genesis"
        self.missions: list[Mission] = []
        self.runs: list[MissionRun] = []

    def create_mission(
        self,
        title: str,
        objective: str,
        application: str = "system",
        priority: str = "medium",
        tasks: list[dict[str, Any]] | None = None,
    ) -> Mission:
        mission_tasks = [
            MissionTask(
                title=task.get("title", "Untitled Task"),
                description=task.get("description", ""),
            )
            for task in (tasks or [])
        ]

        mission = Mission(
            title=title,
            objective=objective,
            application=application,
            priority=priority,
            tasks=mission_tasks,
        )
        self.missions.append(mission)
        return mission

    def list_missions(self, status: str | None = None) -> list[dict[str, Any]]:
        results = self.missions
        if status:
            results = [mission for mission in results if mission.status == status]
        return [mission.to_dict() for mission in results]

    def get_mission(self, mission_id: str) -> Mission | None:
        return next((mission for mission in self.missions if mission.mission_id == mission_id), None)

    def complete_mission(self, mission_id: str) -> dict[str, Any]:
        mission = self.get_mission(mission_id)
        if mission is None:
            return {"error": f"Mission not found: {mission_id}"}
        mission.complete()
        return mission.to_dict()

    def complete_task(self, mission_id: str, task_id: str) -> dict[str, Any]:
        mission = self.get_mission(mission_id)
        if mission is None:
            return {"error": f"Mission not found: {mission_id}"}

        for task in mission.tasks:
            if task.task_id == task_id:
                task.complete()
                return mission.to_dict()

        return {"error": f"Task not found: {task_id}"}

    def generate_mission_from_goal(
        self,
        goal_title: str,
        goal_description: str = "",
        application: str = "system",
        priority: str = "high",
    ) -> Mission:
        lower_title = goal_title.lower()

        if "portfolio" in lower_title or "card" in lower_title:
            tasks = [
                {"title": "Refresh marketplace intelligence", "description": "Collect current listings and comps."},
                {"title": "Run opportunity scoring", "description": "Apply THORᵡ and DEF scoring."},
                {"title": "Rank acquisition candidates", "description": "Prioritize assets by opportunity and risk."},
                {"title": "Record founder decision", "description": "Capture rationale and confidence."},
                {"title": "Update knowledge graph", "description": "Connect asset, player, decision, and mission entities."},
            ]
        else:
            tasks = [
                {"title": "Clarify mission objective", "description": "Define success criteria."},
                {"title": "Gather evidence", "description": "Collect relevant facts and constraints."},
                {"title": "Generate plan", "description": "Build an ordered execution path."},
                {"title": "Execute first action", "description": "Move the mission forward."},
                {"title": "Record outcome", "description": "Store result and rationale."},
            ]

        return self.create_mission(
            title=goal_title,
            objective=goal_description or goal_title,
            application=application,
            priority=priority,
            tasks=tasks,
        )

    def run_mission(self, mission_id: str) -> MissionRun:
        mission = self.get_mission(mission_id)
        actions: list[dict[str, Any]] = []

        if mission is None:
            run = MissionRun(
                mission_id=mission_id,
                status="failed",
                actions=[{"error": f"Mission not found: {mission_id}"}],
            )
            self.runs.append(run)
            return run

        for task in mission.tasks:
            if task.status != "completed":
                task.complete()
                actions.append(
                    {
                        "task_id": task.task_id,
                        "title": task.title,
                        "status": "completed",
                    }
                )
                break

        if mission.tasks and all(task.status == "completed" for task in mission.tasks):
            mission.complete()

        run = MissionRun(
            mission_id=mission_id,
            status="completed",
            actions=actions or [{"message": "No pending tasks."}],
        )
        self.runs.append(run)
        return run

    def history(self) -> list[dict[str, Any]]:
        return [run.to_dict() for run in self.runs]

    def stats(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "missions": len(self.missions),
            "active_missions": len([mission for mission in self.missions if mission.status == "active"]),
            "completed_missions": len([mission for mission in self.missions if mission.status == "completed"]),
            "runs": len(self.runs),
        }


mission_core = AletheusMissionCore()
