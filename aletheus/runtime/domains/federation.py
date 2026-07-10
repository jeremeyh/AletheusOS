class FederationDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, payload=None):
        return self.runtime.federation_v3.bootstrap()

    def join(self, payload):
        return self.runtime.federation_v3.join(
            name=payload.get("name", "Remote Runtime"),
            address=payload.get("address", "localhost"),
            capabilities=payload.get("capabilities", []),
            services=payload.get("services", []),
        )

    def leave(self, payload):
        return self.runtime.federation_v3.leave(
            payload.get("node_id", "")
        )

    def discover(self, payload=None):
        return self.runtime.federation_v3.discover()

    def query(self, payload=None):
        return self.runtime.federation_v3.query()

    def broadcast(self, payload):
        return self.runtime.federation_v3.broadcast(
            payload.get("message", "")
        )

    def statistics(self, payload=None):
        return self.runtime.federation_v3.statistics()
