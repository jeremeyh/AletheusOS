from aletheus.core import Event, Result
from aletheus.kernel.memory import LearningRecord

from .evidence import Evidence
from .mission import Mission


class HelloMission(Mission):
    key = "hello.mission"
    name = "Hello Mission"

    def execute(self, context):
        context.events.publish(
            Event(
                "mission.started", self.key, {"name": self.name}, context.correlation_id
            )
        )
        evidence = Evidence(
            "The constitutional mission pipeline executed.",
            self.key,
            1.0,
            {"status": "success"},
        )
        context.events.publish(
            Event(
                "evidence.collected",
                self.key,
                {"evidence_id": str(evidence.id), "confidence": evidence.confidence},
                context.correlation_id,
            )
        )
        context.memory.preserve(
            LearningRecord(
                self.key,
                {
                    "learning": "Mission execution produced evidence and preserved learning.",
                    "evidence_id": str(evidence.id),
                },
                context.correlation_id,
            )
        )
        value = {"status": "success", "message": "Hello from AletheusOS."}
        context.events.publish(
            Event("mission.completed", self.key, value, context.correlation_id)
        )
        return Result.ok(value, "Hello Mission completed.")
