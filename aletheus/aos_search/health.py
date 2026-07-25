from __future__ import annotations

from .consensus import search_consensus
from .providers import provider_registry
from .resolver import search_resolver
from .router import search_router


class SearchHealth:

    GENESIS = "21.8"
    VERSION = "1.0.0"

    def report(self):

        return {

            "subsystem": "AOS Search",

            "status": "healthy",

            "genesis": self.GENESIS,

            "version": self.VERSION,

            "planner": {

                "status": "healthy",

            },

            "router": search_router.statistics(),

            "providers": provider_registry.statistics(),

            "resolver": search_resolver.health(),

            "consensus": search_consensus.health(),

        }


search_health = SearchHealth()
