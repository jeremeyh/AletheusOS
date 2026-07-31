from __future__ import annotations


class SearchStatistics:
    GENESIS = "21.8"
    VERSION = "1.0.0"

    def __init__(self):

        self.reset()

    def reset(self):

        self.requests = 0
        self.plans = 0
        self.routes = 0
        self.consensus = 0

    def record_request(self):
        self.requests += 1

    def record_plan(self):
        self.plans += 1

    def record_route(self):
        self.routes += 1

    def record_consensus(self):
        self.consensus += 1

    def snapshot(self):

        return {
            "requests": self.requests,
            "plans": self.plans,
            "routes": self.routes,
            "consensus": self.consensus,
            "genesis": self.GENESIS,
            "version": self.VERSION,
        }


search_statistics = SearchStatistics()
