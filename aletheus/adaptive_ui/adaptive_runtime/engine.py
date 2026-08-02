from .models import *


class Engine:
    def hydrate(self, scene, telemetry):
        return {
            "sessionId": scene.session_id,
            "density": scene.density.value,
            "rootNodeId": scene.root.node_id,
            "telemetry": telemetry.clamped(),
            "status": "HYDRATED",
        }
