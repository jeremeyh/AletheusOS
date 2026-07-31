from __future__ import annotations

from .planner import search_planner
from .resolver import search_resolver
from .router import search_router


class AOSSearch:
    GENESIS = "21.8"
    VERSION = "1.0.0"

    def __init__(self):

        self.planner = search_planner
        self.resolver = search_resolver
        self.router = search_router

    def execute(
        self,
        query: str,
    ):

        plan = self.planner.plan(query)

        resolved = self.resolver.resolve(plan)

        results = self.router.execute(
            plan,
            query,
        )

        return {
            "query": query,
            "execution_plan": resolved,
            "results": results,
        }

    def health(self):

        return {
            "status": "healthy",
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


aos_search = AOSSearch()
