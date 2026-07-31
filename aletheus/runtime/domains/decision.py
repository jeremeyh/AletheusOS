from __future__ import annotations


class DecisionDomain:
    """
    Runtime Decision capability domain.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, context):
        context.add_result(
            "decision",
            self.runtime.decision.bootstrap(),
        )
        return context

    def policy_add(self, context):
        payload = context.payload

        result = self.runtime.decision.add_policy(
            name=payload.get("name", "Untitled Policy"),
            description=payload.get("description", ""),
            policy_type=payload.get("policy_type", "general"),
            weight=float(payload.get("weight", 1.0)),
        )

        context.add_result("policy", result)
        return context

    def evaluate(self, context):
        payload = context.payload

        result = self.runtime.decision.evaluate(
            title=payload.get("title", "Untitled Decision"),
            objective=payload.get("objective", ""),
            options=payload.get("options", []),
            policy=payload.get("policy", "maximize_value"),
            runtime=self.runtime,
        )

        context.add_result("decision", result)
        return context

    def execute(self, context):
        result = self.runtime.decision.execute(context.payload.get("decision_id", ""))

        context.add_result("decision", result)
        return context

    def rollback(self, context):
        result = self.runtime.decision.rollback(context.payload.get("decision_id", ""))

        context.add_result("decision", result)
        return context

    def explain(self, context):
        result = self.runtime.decision.explain(context.payload.get("decision_id", ""))

        context.add_result("explanation", result)
        return context

    def history(self, context):
        history = self.runtime.decision.history()

        context.add_result("history", history)
        context.add_result("decisions", history)

        return context

    def statistics(self, context):
        context.add_result(
            "decision_stats",
            (
                self.runtime.decision.stats()
                if hasattr(self.runtime.decision, "stats")
                else self.runtime.decision.statistics()
                if hasattr(self.runtime.decision, "statistics")
                else {
                    "status": getattr(
                        self.runtime.decision,
                        "status",
                        "unknown",
                    )
                }
            ),
        )

        return context
