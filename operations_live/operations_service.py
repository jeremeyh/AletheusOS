class LiveOperationsService:
    """CardHawk OS™ 6.0B Live Operations Center™."""

    @staticmethod
    def snapshot(state):
        container = state.get("container")
        snap = container.snapshot() if container else {}
        return {
            "provider_health": {p: "ready" for p in snap.get("providers", [])},
            "services": {s: "online" for s in snap.get("services", [])},
            "engines": {e: "online" for e in snap.get("engines", [])},
            "queue_status": {"queued": 0, "running": 0, "failed": 0},
            "pipeline_execution": "ready",
            "background_services": "ready",
            "event_stream": "ready",
            "runtime_diagnostics": "ready",
            "intelligence_latency_ms": 0,
            "database_health": "ready",
            "errors": snap.get("errors", []),
        }
