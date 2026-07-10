class MissionDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def create(self, payload):
        return self.runtime.missions_v2.create(
            title=payload.get("title", "Untitled Mission"),
            description=payload.get("description", ""),
            priority=payload.get("priority", "medium"),
            metadata=payload.get("metadata", {}),
        )

    def list(self, payload=None):
        return self.runtime.missions_v2.list()

    def execute(self, payload):
        return self.runtime.missions_v2.execute(
            payload.get("mission_id", "")
        )

    def complete(self, payload):
        return self.runtime.missions_v2.complete(
            payload.get("mission_id", "")
        )

    def statistics(self, payload=None):
        return self.runtime.missions_v2.statistics()
