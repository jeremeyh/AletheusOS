from __future__ import annotations

from dataclasses import dataclass, field

from .core import aletheus_foundation


@dataclass(slots=True)
class ExecutionPlan:

    identity: str

    application: str

    intent: str

    query: str

    engines: list[str] = field(default_factory=list)

    context: dict = field(default_factory=dict)

    def to_dict(self):

        return {
            "identity": self.identity,
            "application": self.application,
            "intent": self.intent,
            "query": self.query,
            "engines": self.engines,
            "context": self.context,
        }


class FoundationOrchestrator:

    GENESIS = "22.1"

    VERSION = "1.0.0"

    def create_plan(
        self,
        identity: str,
        application: str,
        intent: str,
        query: str,
    ) -> ExecutionPlan:

        plan = ExecutionPlan(
            identity=identity,
            application=application,
            intent=intent,
            query=query,
        )

        if intent == "marketplace_analysis":

            plan.engines.extend(
                [
                    "foundation.marketplace",
                    "foundation.forecast",
                    "foundation.evaluation",
                ]
            )

        elif intent == "inventory_lookup":

            plan.engines.append(
                "foundation.monitoring"
            )

        else:

            plan.engines.append(
                "foundation.evaluation"
            )

        return plan

    def health(self):

        return {
            "status": "healthy",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "foundation": aletheus_foundation.health(),
        }


foundation_orchestrator = FoundationOrchestrator()
