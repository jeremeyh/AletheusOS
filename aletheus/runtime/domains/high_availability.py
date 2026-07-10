class HighAvailabilityDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, payload=None):
        return self.runtime.high_availability_v3.bootstrap()

    def join(self, payload):
        return self.runtime.high_availability_v3.join(
            name=payload.get("name", "Replica Runtime"),
            metadata=payload.get("metadata", {}),
        )

    def leave(self, payload):
        return self.runtime.high_availability_v3.leave(
            payload.get("node_id", "")
        )

    def promote(self, payload):
        return self.runtime.high_availability_v3.promote(
            payload.get("node_id", "")
        )

    def demote(self, payload):
        return self.runtime.high_availability_v3.demote(
            payload.get("node_id", "")
        )

    def failover(self, payload=None):
        return self.runtime.high_availability_v3.failover()

    def recover(self, payload):
        return self.runtime.high_availability_v3.recover(
            payload.get("node_id", "")
        )

    def replicate(self, payload):
        return self.runtime.high_availability_v3.replicate(
            payload.get("payload", {})
        )

    def status(self, payload=None):
        return self.runtime.high_availability_v3.status()

    def statistics(self, payload=None):
        return self.runtime.high_availability_v3.statistics()
