class RuntimeKernel:
    """
    Runtime Kernel™

    Central kernel-level facade for runtime orchestration.
    """

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def boot(self, runtime):
        return self.orchestrator.boot(runtime)

    def health(self, runtime, container):
        return self.orchestrator.health(runtime, container)

    def recover(self, runtime, component, reason):
        return self.orchestrator.recover(
            runtime,
            component,
            reason,
        )
