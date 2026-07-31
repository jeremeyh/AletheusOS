from __future__ import annotations

from dataclasses import dataclass, field

from .intent import intent_engine


@dataclass(slots=True)
class ExecutionPlan:
    name: str

    providers: list[str] = field(default_factory=list)

    consensus: bool = False
    internet: bool = False
    marketplace: bool = False
    enterprise: bool = False
    memory: bool = False
    visual: bool = False

    constitutional_articles: list[str] = field(default_factory=list)

    def to_dict(self):

        return {
            "name": self.name,
            "providers": self.providers,
            "consensus": self.consensus,
            "internet": self.internet,
            "marketplace": self.marketplace,
            "enterprise": self.enterprise,
            "memory": self.memory,
            "visual": self.visual,
            "constitutional_articles": self.constitutional_articles,
        }


class SearchPlanner:
    GENESIS = "21.8.2"
    VERSION = "1.1.0"

    def plan(self, query: str) -> ExecutionPlan:

        intent = intent_engine.classify(query)

        if intent.intent == "marketplace_analysis":
            return ExecutionPlan(
                name="Marketplace Intelligence",
                providers=[
                    "vault",
                    "marketplace",
                    "internet",
                ],
                marketplace=True,
                internet=True,
                consensus=True,
                constitutional_articles=[
                    "Article LXXIX",
                    "Article LXXX",
                    "Article LXXXVI",
                ],
            )

        if intent.intent == "inventory_lookup":
            return ExecutionPlan(
                name="Enterprise Inventory",
                providers=[
                    "enterprise",
                ],
                enterprise=True,
                constitutional_articles=[
                    "Article LXXIX",
                    "Article LXXXVI",
                ],
            )

        return ExecutionPlan(
            name="General Knowledge",
            providers=[
                "memory",
                "knowledge",
            ],
            memory=True,
            constitutional_articles=[
                "Article LXXX",
                "Article LXXXVI",
            ],
        )


search_planner = SearchPlanner()
