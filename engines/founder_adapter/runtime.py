from core.engine_base import EngineBase
from intelligence.events import PORTFOLIO_UPDATED

class FounderAdapter(EngineBase):

    name = "Founder AI"

    events = [
        PORTFOLIO_UPDATED
    ]

    def handle_event(self, payload):

        print("[Founder AI] Founder Brief™ updated.")

    def execute(self, payload):
        self.handle_event(payload)

ENGINE = FounderAdapter()
