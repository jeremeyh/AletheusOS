from __future__ import annotations

from typing import Any

from aletheus.planning.models import AutonomousPlan, PlanningStep


class AletheusPlanningCore:
    def __init__(self) -> None:
        self.version = "1.4.0"
        self.plans: list[AutonomousPlan] = []

    def create_plan(
        self,
        objective: str,
        strategy: str = "",
        priority: str = "high",
        steps: list[dict[str, Any]] | None = None,
    ) -> AutonomousPlan:
        plan_steps = [
            PlanningStep(
                title=item.get("title", "Untitled Step"),
                description=item.get("description", ""),
                assigned_agent=item.get("assigned_agent", "Executive Agent"),
            )
            for item in (steps or self.default_steps(objective))
        ]

        plan = AutonomousPlan(
            objective=objective,
            strategy=strategy or self.default_strategy(objective),
            priority=priority,
            steps=plan_steps,
        )
        self.plans.append(plan)
        return plan

    def default_strategy(self, objective: str) -> str:
        lower = objective.lower()
        if "card hawk" in lower or "portfolio" in lower:
            return "Use agents to inspect current state, enrich knowledge, generate recommendations, and produce founder-ready actions."
        return "Clarify objective, assign specialist agents, execute the first useful step, and record outcomes."

    def default_steps(self, objective: str) -> list[dict[str, Any]]:
        lower = objective.lower()

        if "card hawk" in lower or "portfolio" in lower:
            return [
                {
                    "title": "Summarize current objective",
                    "description": "Executive Agent creates strategic framing.",
                    "assigned_agent": "Executive Agent",
                },
                {
                    "title": "Recall relevant history",
                    "description": "Memory Agent retrieves related prior decisions and records.",
                    "assigned_agent": "Memory Agent",
                },
                {
                    "title": "Expand entity context",
                    "description": "Knowledge Agent maps related graph and semantic concepts.",
                    "assigned_agent": "Knowledge Agent",
                },
                {
                    "title": "Scout opportunity path",
                    "description": "Scout Agent identifies acquisition or integration opportunities.",
                    "assigned_agent": "Scout Agent",
                },
                {
                    "title": "Assess market impact",
                    "description": "Market Agent evaluates pricing, valuation, and risk.",
                    "assigned_agent": "Market Agent",
                },
                {
                    "title": "Prepare founder recommendation",
                    "description": "Founder Agent summarizes decision-ready next action.",
                    "assigned_agent": "Founder Agent",
                },
            ]

        return [
            {
                "title": "Frame objective",
                "description": "Define the desired outcome.",
                "assigned_agent": "Executive Agent",
            },
            {
                "title": "Gather context",
                "description": "Collect relevant memory and knowledge.",
                "assigned_agent": "Memory Agent",
            },
            {
                "title": "Evaluate options",
                "description": "Assess possible paths.",
                "assigned_agent": "Knowledge Agent",
            },
            {
                "title": "Recommend action",
                "description": "Produce founder-ready next step.",
                "assigned_agent": "Founder Agent",
            },
        ]

    def list_plans(self, status: str | None = None) -> list[dict[str, Any]]:
        results = self.plans
        if status:
            results = [plan for plan in results if plan.status == status]
        return [plan.to_dict() for plan in results]

    def get_plan(self, plan_id: str) -> AutonomousPlan | None:
        return next((plan for plan in self.plans if plan.plan_id == plan_id), None)

    def execute_next_step(self, plan_id: str, runtime: Any) -> dict[str, Any]:
        plan = self.get_plan(plan_id)
        if plan is None:
            return {"error": f"Plan not found: {plan_id}"}

        pending = [step for step in plan.steps if step.status == "pending"]
        if not pending:
            plan.complete_if_finished()
            return {"message": "No pending steps.", "plan": plan.to_dict()}

        step = pending[0]

        assignment = runtime.commands.dispatch(
            "agent.task.assign",
            {
                "agent_name": step.assigned_agent,
                "title": step.title,
                "payload": {
                    "plan_id": plan.plan_id,
                    "objective": plan.objective,
                    "step_id": step.step_id,
                    "description": step.description,
                },
            },
        )

        run = runtime.commands.dispatch(
            "agent.run",
            {"agent_name": step.assigned_agent},
        )

        step.complete()
        plan.complete_if_finished()

        return {
            "plan": plan.to_dict(),
            "executed_step": step.to_dict(),
            "assignment": assignment.results,
            "agent_run": run.results,
        }

    def execute_plan(self, plan_id: str, runtime: Any) -> dict[str, Any]:
        outputs = []
        while True:
            result = self.execute_next_step(plan_id, runtime)
            outputs.append(result)

            plan = self.get_plan(plan_id)
            if plan is None or plan.status == "completed":
                break

            if "error" in result:
                break

        return {
            "plan_id": plan_id,
            "outputs": outputs,
            "final_plan": self.get_plan(plan_id).to_dict()
            if self.get_plan(plan_id)
            else None,
        }

    def stats(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "plans": len(self.plans),
            "active_plans": len(
                [plan for plan in self.plans if plan.status == "active"]
            ),
            "completed_plans": len(
                [plan for plan in self.plans if plan.status == "completed"]
            ),
            "steps": sum(len(plan.steps) for plan in self.plans),
        }


planning_core = AletheusPlanningCore()
