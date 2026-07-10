from __future__ import annotations


class CopilotDomain:
    """
    Runtime Copilot capability domain.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def ask(self, context):
        exchange = self.runtime.copilot.ask(
            prompt=context.payload.get("prompt", ""),
            runtime=self.runtime,
        )

        self.runtime.memory.remember(
            key="copilot_exchange",
            value=exchange.to_dict(),
            namespace="aletheus.copilot",
            memory_type="persistent",
            tags=[
                "copilot",
                "founder",
            ],
        )

        context.add_result(
            "exchange",
            exchange.to_dict(),
        )

        return context

    def brief(self, context):
        brief = self.runtime.copilot.brief(self.runtime)

        context.add_result(
            "brief",
            brief,
        )

        return context

    def recommend(self, context):
        context.add_result(
            "recommendations",
            self.runtime.copilot.recommend(self.runtime),
        )

        return context

    def timeline(self, context):
        context.add_result(
            "timeline",
            self.runtime.copilot.timeline(self.runtime),
        )

        return context

    def history(self, context):
        context.add_result(
            "history",
            self.runtime.copilot.history(),
        )

        return context

    def statistics(self, context):
        context.add_result(
            "copilot_stats",
            (
                self.runtime.copilot.stats()
                if hasattr(self.runtime.copilot, "stats")
                else self.runtime.copilot.statistics()
                if hasattr(self.runtime.copilot, "statistics")
                else {
                    "status": getattr(
                        self.runtime.copilot,
                        "status",
                        "unknown",
                    )
                }
            ),
        )

        return context
