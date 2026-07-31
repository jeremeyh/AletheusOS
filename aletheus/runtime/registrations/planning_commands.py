"""
Cognition and Planning Command Registration.

Provides compatibility command surfaces over two bounded components:

- runtime.cognition:
  goals, generated plans, reasoning records, decisions

- runtime.planning_v2:
  executable autonomous plan lifecycle
"""

from __future__ import annotations

from typing import Any


def _serialize(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return value


def register_planning_commands(runtime):
    commands = runtime.commands
    cognition = runtime.cognition
    planning = runtime.planning_v2

    # ---------------------------------------------------------
    # Genesis 0.5 cognition compatibility
    # ---------------------------------------------------------

    def create_goal(payload=None):
        payload = payload or {}

        goal = cognition.create_goal(
            title=payload.get("title", "Untitled Goal"),
            description=payload.get("description", ""),
            priority=payload.get("priority", "medium"),
            owner=payload.get("owner", "Founder"),
            application=payload.get("application", "system"),
        )

        return _serialize(goal)

    def complete_goal(payload=None):
        payload = payload or {}

        return cognition.complete_goal(
            goal_id=payload.get("goal_id", ""),
        )

    def list_goals(payload=None):
        payload = payload or {}

        return cognition.list_goals(
            status=payload.get("status"),
        )

    def generate_plan(payload=None):
        payload = payload or {}

        plan = cognition.generate_plan(
            goal_id=payload.get("goal_id", ""),
            goal_title=payload.get(
                "goal_title",
                payload.get("title", ""),
            ),
        )

        return _serialize(plan)

    def list_generated_plans(payload=None):
        return cognition.list_plans()

    def record_decision(payload=None):
        payload = payload or {}

        decision = cognition.record_decision(
            title=payload.get("title", "Untitled Decision"),
            decision=payload.get("decision", ""),
            rationale=payload.get("rationale", ""),
            confidence=payload.get("confidence", 0.75),
            evidence=payload.get("evidence"),
        )

        return _serialize(decision)

    # ---------------------------------------------------------
    # v1.4 autonomous-planning compatibility
    # ---------------------------------------------------------

    def create_autonomous_plan(payload=None):
        payload = payload or {}

        plan = planning.create(
            goal=payload.get(
                "objective",
                payload.get("goal", "Untitled Objective"),
            )
        )

        # v1.4 called these steps. The canonical v2.9 model calls
        # them tasks. Preserve both names at the command boundary.
        plan.setdefault(
            "steps",
            list(plan.get("tasks", [])),
        )

        return plan

    def execute_next_step(payload=None):
        payload = payload or {}
        plan_id = payload.get("plan_id", "")

        plan = planning.plans.get(plan_id)

        if plan is None:
            raise KeyError(f"Plan not found: {plan_id}")

        executed_step = None

        for task in plan.tasks:
            if task.status != "completed":
                task.status = "completed"
                executed_step = task
                break

        plan.update_progress()

        if executed_step is None:
            executed_step = {
                "title": "No pending steps",
                "status": "completed",
                "priority": 0,
            }
        else:
            executed_step = executed_step.to_dict()

        return {
            "executed_step": executed_step,
            "plan": plan.to_dict(),
        }

    def execute_full_plan(payload=None):
        payload = payload or {}
        plan_id = payload.get("plan_id", "")

        final_plan = planning.complete(plan_id)

        return {
            "final_plan": final_plan,
        }

    def planning_statistics(payload=None):
        return planning.statistics()

    # ---------------------------------------------------------
    # v2.9 canonical planning lifecycle
    # ---------------------------------------------------------

    def bootstrap_planning(payload=None):
        return planning.bootstrap()

    def create_plan(payload=None):
        payload = payload or {}

        return planning.create(
            goal=payload.get(
                "goal",
                payload.get("objective", "Untitled Goal"),
            )
        )

    def execute_plan(payload=None):
        payload = payload or {}

        return planning.execute(
            plan_id=payload.get("plan_id", ""),
        )

    def plan_progress(payload=None):
        payload = payload or {}

        return planning.progress(
            plan_id=payload.get("plan_id", ""),
        )

    def replan(payload=None):
        payload = payload or {}

        return planning.replan(
            plan_id=payload.get("plan_id", ""),
        )

    def complete_plan(payload=None):
        payload = payload or {}

        return planning.complete(
            plan_id=payload.get("plan_id", ""),
        )

    def plan_status(payload=None):
        return planning.status()

    def plan_statistics(payload=None):
        return planning.statistics()

    # Genesis cognition surface
    commands.register(
        "goal.create",
        create_goal,
        replace=True,
    )
    commands.register(
        "goal.complete",
        complete_goal,
        replace=True,
    )
    commands.register(
        "goal.list",
        list_goals,
        replace=True,
    )
    commands.register(
        "plan.generate",
        generate_plan,
        replace=True,
    )
    commands.register(
        "plan.list",
        list_generated_plans,
        replace=True,
    )
    commands.register(
        "decision.record",
        record_decision,
        replace=True,
    )

    # v1.4 autonomous-planning surface
    commands.register(
        "planning.create",
        create_autonomous_plan,
        replace=True,
    )
    commands.register(
        "planning.execute_next",
        execute_next_step,
        replace=True,
    )
    commands.register(
        "planning.execute",
        execute_full_plan,
        replace=True,
    )
    commands.register(
        "planning.statistics",
        planning_statistics,
        replace=True,
    )

    # v2.9 canonical lifecycle
    commands.register(
        "plan.bootstrap",
        bootstrap_planning,
        replace=True,
    )
    commands.register(
        "plan.create",
        create_plan,
        replace=True,
    )
    commands.register(
        "plan.execute",
        execute_plan,
        replace=True,
    )
    commands.register(
        "plan.progress",
        plan_progress,
        replace=True,
    )
    commands.register(
        "plan.replan",
        replan,
        replace=True,
    )
    commands.register(
        "plan.complete",
        complete_plan,
        replace=True,
    )
    commands.register(
        "plan.status",
        plan_status,
        replace=True,
    )
    commands.register(
        "plan.statistics",
        plan_statistics,
        replace=True,
    )
