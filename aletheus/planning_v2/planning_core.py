from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from aletheus.time_utils import utc_now, utc_now_iso


def utc_now() -> str:
    return utc_now_iso()


@dataclass
class PlanTask:
    title: str
    status: str = "pending"
    priority: int = 5

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
            "priority": self.priority,
        }


@dataclass
class PlanMilestone:
    title: str
    status: str = "pending"

    def to_dict(self):
        return {
            "title": self.title,
            "status": self.status,
        }


@dataclass
class Plan:
    goal: str

    objectives: list[str] = field(default_factory=list)

    milestones: list[PlanMilestone] = field(default_factory=list)

    tasks: list[PlanTask] = field(default_factory=list)

    dependencies: list[str] = field(default_factory=list)

    priority: int = 5

    status: str = "planned"

    progress: float = 0.0

    created_at: str = field(default_factory=utc_now)

    updated_at: str = field(default_factory=utc_now)

    completed_at: str | None = None

    plan_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def execute(self):

        self.status = "running"

        self.updated_at = utc_now()

    def complete(self):

        self.status = "completed"

        self.progress = 100.0

        self.completed_at = utc_now()

        self.updated_at = utc_now()

    def update_progress(self):

        if len(self.tasks) == 0:
            self.progress = 100.0
            return

        completed = sum(task.status == "completed" for task in self.tasks)

        self.progress = round(
            completed / len(self.tasks) * 100,
            2,
        )

        self.updated_at = utc_now()

    def to_dict(self):

        return {
            "plan_id": self.plan_id,
            "goal": self.goal,
            "objectives": self.objectives,
            "milestones": [m.to_dict() for m in self.milestones],
            "tasks": [t.to_dict() for t in self.tasks],
            "dependencies": self.dependencies,
            "priority": self.priority,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed_at": self.completed_at,
        }


class AletheusPlanningEngine:
    VERSION = "2.9.0"

    def __init__(self):

        self.plans: dict[str, Plan] = {}

        self.strategies = []

    def bootstrap(self):

        self.strategies = [
            "Sequential",
            "Parallel",
            "Priority First",
            "Risk Optimized",
            "Fastest Completion",
            "Founder Directed",
        ]

        return self.statistics()

    def create(self, goal: str):

        plan = Plan(goal=goal)

        plan.objectives.extend(
            [
                "Research",
                "Analyze",
                "Decide",
                "Execute",
            ]
        )

        plan.milestones.extend(
            [
                PlanMilestone("Research Complete"),
                PlanMilestone("Decision Complete"),
                PlanMilestone("Execution Complete"),
            ]
        )

        plan.tasks.extend(
            [
                PlanTask("Research"),
                PlanTask("Marketplace Scan"),
                PlanTask("Portfolio Review"),
                PlanTask("Decision Engine"),
                PlanTask("Founder Approval"),
            ]
        )

        self.plans[plan.plan_id] = plan

        return plan.to_dict()

    def execute(self, plan_id):

        plan = self.plans[plan_id]

        plan.execute()

        return plan.to_dict()

    def complete(self, plan_id):

        plan = self.plans[plan_id]

        for task in plan.tasks:
            task.status = "completed"

        plan.update_progress()

        plan.complete()

        return plan.to_dict()

    def progress(self, plan_id):

        plan = self.plans[plan_id]

        plan.update_progress()

        return plan.to_dict()

    def replan(self, plan_id):

        plan = self.plans[plan_id]

        plan.status = "replanned"

        plan.updated_at = utc_now()

        return plan.to_dict()

    def status(self):

        return {"plans": [p.to_dict() for p in self.plans.values()]}

    # ----------------------------------------------------
    # Runtime Compatibility API
    # ----------------------------------------------------

    def register_default_plans(self):
        return self.bootstrap()

    def version(self):
        return self.VERSION

    def list_plans(self):
        return [plan.to_dict() for plan in self.plans.values()]

    def statistics(self):

        plans = len(self.plans)

        running = sum(p.status == "running" for p in self.plans.values())

        completed = sum(p.status == "completed" for p in self.plans.values())

        replanned = sum(p.status == "replanned" for p in self.plans.values())

        return {
            "version": self.VERSION,
            # Native v2 statistics
            "strategies": len(self.strategies),
            "plans": plans,
            "running": running,
            "completed": completed,
            "replanned": replanned,
            # Genesis 7.10 Contract Convergence™
            "active_plans": running,
        }


planning_core = AletheusPlanningEngine()
