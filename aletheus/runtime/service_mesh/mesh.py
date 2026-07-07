from .models import MeshNode, MeshRouteResult


class RuntimeServiceMesh:
    """
    Runtime Service Mesh™

    Internal topology layer for registering runtime nodes and routing
    requests without forcing runtime/core.py or the Executive Kernel
    to know implementation details.
    """

    def __init__(self):
        self.nodes = {}
        self.handlers = {}
        self.route_history = []

    def register_node(self, name: str, node_type: str = "service", handler=None, metadata=None):
        node = MeshNode(
            name=name,
            node_type=node_type,
            metadata=metadata or {},
        )

        self.nodes[name] = node

        if handler is not None:
            self.handlers[name] = handler

        return node

    def has_node(self, name: str) -> bool:
        return name in self.nodes

    def route(self, source: str, destination: str, payload: dict | None = None):
        payload = payload or {}

        if destination not in self.nodes:
            result = MeshRouteResult(
                source=source,
                destination=destination,
                status="unknown_destination",
                response={"error": f"Destination '{destination}' is not registered in the mesh."},
            )
            self.route_history.append(result)
            return result

        handler = self.handlers.get(destination)

        if handler is None:
            result = MeshRouteResult(
                source=source,
                destination=destination,
                status="no_handler",
                response={"message": f"Destination '{destination}' is registered but has no handler."},
            )
            self.route_history.append(result)
            return result

        try:
            response = handler(payload)
            result = MeshRouteResult(
                source=source,
                destination=destination,
                status="delivered",
                response=response if isinstance(response, dict) else {"result": response},
            )
        except Exception as exc:
            result = MeshRouteResult(
                source=source,
                destination=destination,
                status="failed",
                response={"error": str(exc)},
            )

        self.route_history.append(result)
        return result

    def health(self):
        return {
            "status": "online",
            "nodes": len(self.nodes),
            "handlers": len(self.handlers),
            "routes_processed": len(self.route_history),
            "node_names": sorted(self.nodes.keys()),
        }
