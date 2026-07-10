from __future__ import annotations


class ReasoningDomain:
    """
    Runtime Reasoning capability domain.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, context):
        context.add_result(
            "reasoning",
            self.runtime.reasoning.bootstrap_rules(),
        )
        return context

    def rule_add(self, context):
        payload = context.payload

        result = self.runtime.reasoning.add_rule(
            name=payload.get("name", "Untitled Rule"),
            description=payload.get("description", ""),
            rule_type=payload.get("rule_type", "general"),
            weight=float(payload.get("weight", 0.75)),
        )

        context.add_result("rule", result)
        return context

    def evaluate(self, context):
        payload = context.payload

        result = self.runtime.reasoning.evaluate(
            question=payload.get("question", ""),
            runtime=self.runtime,
            context=payload.get("context", {}),
        )

        context.add_result("evaluation", result)
        context.add_result("reasoning", result)
        return context

    def explain(self, context):
        result = self.runtime.reasoning.explain(
            context.payload.get("trace_id", "")
        )

        context.add_result("explanation", result)
        return context

    def trace(self, context):
        result = self.runtime.reasoning.trace(
            context.payload.get("trace_id", "")
        )

        context.add_result("trace", result)
        return context

    def decision(self, context):
        payload = context.payload

        result = self.runtime.reasoning.decision(
            question=payload.get("question", ""),
            runtime=self.runtime,
            context=payload.get("context", {}),
        )

        context.add_result("decision", result)
        return context

    def confidence(self, context):
        context.add_result(
            "confidence",
            self.runtime.reasoning.confidence(),
        )

        return context

    def statistics(self, context):
        context.add_result(
            "reasoning_stats",
            (
                self.runtime.reasoning.stats()
                if hasattr(self.runtime.reasoning, "stats")
                else self.runtime.reasoning.statistics()
                if hasattr(self.runtime.reasoning, "statistics")
                else {
                    "status": getattr(
                        self.runtime.reasoning,
                        "status",
                        "unknown",
                    )
                }
            ),
        )

        return context
