from .runtime_registry import runtime_registry
from .heartbeat import heartbeat_service
from .protocol import mesh_protocol
from .events import mesh_events


class MeshCore:

    version = "2.0.0-e"

    def diagnostics(self):

        return {

            "version": self.version,

            "registry": runtime_registry.stats(),

            "heartbeat": heartbeat_service.pulse(),

            "status": "online"

        }


mesh_core = MeshCore()
