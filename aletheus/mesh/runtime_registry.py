

class RuntimeRegistry:

    def __init__(self):

        self.version = "2.0.0-e"

        self.nodes = {}

    def register(self, runtime):

        self.nodes[runtime.node_id] = runtime

        return runtime.to_dict()

    def unregister(self, node_id):

        if node_id in self.nodes:

            return self.nodes.pop(node_id).to_dict()

        return None

    def discover(self):

        return [node.to_dict() for node in self.nodes.values()]

    def heartbeat(self, node_id):

        if node_id in self.nodes:

            self.nodes[node_id].ping()

            return self.nodes[node_id].to_dict()

        return None

    def stats(self):

        return {

            "version": self.version,

            "connected_nodes": len(self.nodes),

            "online": len(self.nodes),

            "mesh_status": "online"

        }


runtime_registry = RuntimeRegistry()
