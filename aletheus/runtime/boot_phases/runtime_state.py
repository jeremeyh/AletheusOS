class RuntimeStateBootPhase:
    """
    Runtime State Boot Phase™

    Owns the initial runtime status, boot metrics, and boot event.
    """

    def run(self, runtime):
        runtime.status = "online"

        runtime.metrics.record("runtime.version", runtime.version)
        runtime.metrics.record("runtime.status", runtime.status)

        runtime.events.publish(
            "runtime.booted",
            {"version": runtime.version},
            source="runtime",
        )

        return {
            "status": runtime.status,
            "version": runtime.version,
        }
