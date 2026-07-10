class ClusterDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def join(self, payload):
        return self.runtime.distributed.join(
            node_name=payload.get("node_name", "Unnamed Runtime"),
            capabilities=payload.get("capabilities", []),
            services=payload.get("services", []),
        )

    def leave(self, payload):
        return self.runtime.distributed.leave(
            payload.get("node_id", "")
        )

    def nodes(self, payload=None):
        return self.runtime.distributed.nodes()

    def services(self, payload=None):
        return self.runtime.distributed.services()

    def heartbeat(self, payload=None):
        return self.runtime.distributed.heartbeat()

    def elect_leader(self, payload=None):
        return self.runtime.distributed.elect_leader()

    def statistics(self, payload=None):
        return self.runtime.distributed.statistics()
