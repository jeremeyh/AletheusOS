from __future__ import annotations

from aletheus.constitutional_graph import constitutional_graph
from aletheus.constitutional_ledger import constitutional_ledger
from aletheus.constitutional_memory import constitutional_memory


class ServiceClient:
    def __init__(self, app):
        self.app = app

    def ledger(self):
        return constitutional_ledger

    def memory(self):
        return constitutional_memory

    def graph(self):
        return constitutional_graph

    def reason(self):
        return {
            "service": "constitutional_reasoning",
            "status": "planned",
        }

    def simulate(self):
        return {
            "service": "constitutional_simulation",
            "status": "planned",
        }

    def digital_twin(self):
        return {
            "service": "constitutional_digital_twin",
            "status": "planned",
        }
