from core.engine_base import EngineBase
from core.publisher import publisher
from intelligence.events import DNA_COMPLETED, THORX_COMPLETED

class THORXAdapter(EngineBase):

    name = "THORᵡ"

    events = [
        DNA_COMPLETED
    ]

    def handle_event(self, payload):

        print("[THORᵡ] Computing intelligence...")

        score = {
            "score": 92,
            "confidence": 0.96,
            "asset": payload.get("asset")
        }

        publisher.publish(
            THORX_COMPLETED,
            score
        )

    def execute(self, payload):
        self.handle_event(payload)

ENGINE = THORXAdapter()
