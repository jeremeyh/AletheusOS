from __future__ import annotations


class PlanningDomain:
    """
    Runtime Planning capability domain.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def create(self, context):
        payload = context.payload

        plan = self.runtime.planning.create_plan(
            objective=payload.get("objective", "Untitled Objective"),
            strategy=payload.get("strategy", ""),
            priority=payload.get("priority", "high"),
            steps=payload.get("steps"),
        )

        self.runtime.memory.remember(
            key="autonomous_plan_created",
            value=plan.to_dict(),
            namespace="aletheus.planning",
            memory_type="decision",
            tags=[
                "planning",
                "autonomous",
                "agents",
            ],
        )

        context.add_result(
            "plan",
            plan.to_dict(),
        )

        return context

    def list(self, context):
        context.add_result(
            "plans",
            self.runtime.planning.list_plans(
                context.payload.get("status"),
            ),
        )

        return context

    def execute_next(self, context):
        result = self.runtime.planning.execute_next_step(
            plan_id=context.payload.get("plan_id", ""),
            runtime=self.runtime,
        )

        self.runtime.memory.remember(
            key="autonomous_plan_step_executed",
            value=result,
            namespace="aletheus.planning",
            memory_type="episodic",
            tags=[
                "planning",
                "execution",
            ],
        )

        context.add_result(
            "execution",
            result,
        )

        return context

    def execute(self, context):
        result = self.runtime.planning.execute_plan(
            plan_id=context.payload.get("plan_id", ""),
            runtime=self.runtime,
        )

        self.runtime.memory.remember(
            key="autonomous_plan_executed",
            value=result,
            namespace="aletheus.planning",
            memory_type="decision",
            tags=[
                "planning",
                "execution",
                "autonomous",
            ],
        )

        context.add_result(
            "execution",
            result,
        )

        return context

    def statistics(self, context):
        context.add_result(
            "planning_stats",
            (
                self.runtime.planning.stats()
                if hasattr(self.runtime.planning, "stats")
                else self.runtime.planning.statistics()
                if hasattr(self.runtime.planning, "statistics")
                else {
                    "status": getattr(
                        self.runtime.planning,
                        "status",
                        "unknown",
                    )
                }
            ),
        )

        return context
