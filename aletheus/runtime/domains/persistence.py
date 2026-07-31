class PersistenceDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, payload=None):
        return self.runtime.persistence_v3.bootstrap()

    def save(self, payload=None):
        return self.runtime.persistence_v3.save(self.runtime)

    def load(self, payload=None):
        return self.runtime.persistence_v3.load()

    def snapshot(self, payload):
        return self.runtime.persistence_v3.snapshot(
            name=payload.get("name", "Runtime Snapshot"),
            runtime=self.runtime,
        )

    def restore(self, payload):
        return self.runtime.persistence_v3.restore(payload.get("snapshot_id", ""))

    def export(self, payload=None):
        return self.runtime.persistence_v3.export()

    def import_state(self, payload):
        return self.runtime.persistence_v3.import_state(payload.get("state", {}))

    def statistics(self, payload=None):
        return self.runtime.persistence_v3.statistics()
