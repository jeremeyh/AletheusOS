from core.engine_base import EngineBase
from core.publisher import publisher
from intelligence.events import THORX_COMPLETED, PORTFOLIO_UPDATED

class PortfolioAdapter(EngineBase):

    name = "Portfolio Engine"

    events = [
        THORX_COMPLETED
    ]

    def handle_event(self, payload):

        print("[Portfolio] Updating portfolio...")

        publisher.publish(
            PORTFOLIO_UPDATED,
            payload
        )

    def execute(self, payload):
        self.handle_event(payload)

ENGINE = PortfolioAdapter()
