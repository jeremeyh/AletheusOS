from .models import RelayPacket, RelayResult


class RelayNetwork:
    """
    Runtime Relay Network™

    Lightweight routing layer for moving packets between runtime services
    without forcing runtime/core.py to know every implementation detail.
    """

    def __init__(self):
        self.routes = {}
        self.history = []

    def register(self, target: str, handler):
        self.routes[target] = handler
        return {
            "registered": True,
            "target": target,
        }

    def dispatch(self, packet: RelayPacket):
        handler = self.routes.get(packet.target)

        if handler is None:
            result = RelayResult(
                packet_id=packet.packet_id,
                status="unroutable",
                target=packet.target,
                response={
                    "error": f"No relay route registered for '{packet.target}'."
                },
            )
            self.history.append(result)
            return result

        try:
            response = handler(packet.payload)
            result = RelayResult(
                packet_id=packet.packet_id,
                status="delivered",
                target=packet.target,
                response=response if isinstance(response, dict) else {"result": response},
            )

        except Exception as exc:
            result = RelayResult(
                packet_id=packet.packet_id,
                status="failed",
                target=packet.target,
                response={"error": str(exc)},
            )

        self.history.append(result)
        return result

    def send(self, source: str, target: str, payload: dict, route: str = "default"):
        packet = RelayPacket(
            source=source,
            target=target,
            payload=payload,
            route=route,
        )
        return self.dispatch(packet)

    def health(self):
        return {
            "status": "online",
            "routes": sorted(self.routes.keys()),
            "history_count": len(self.history),
        }
