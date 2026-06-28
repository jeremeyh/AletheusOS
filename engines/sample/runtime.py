from core.engine_base import EngineBase

class SampleEngine(EngineBase):

    name = "Sample Engine"

    version = "2.0"

    events = [
        "platform.started",
        "asset.created",
    ]

    def handle_event(self, payload):
        print(f"[Sample Engine] Event received -> {payload}")

    def execute(self, payload):
        print(f"[Sample Engine] Execute -> {payload}")

ENGINE = SampleEngine()
