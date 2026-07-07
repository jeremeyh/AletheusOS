class RuntimeKernel:
    """
    Runtime Kernel™

    Kernel-level facade for runtime orchestration.
    Owns boot handoff through the boot pipeline.
    """

    def __init__(self, orchestrator, boot_pipeline=None):
        self.orchestrator = orchestrator
        self.boot_pipeline = boot_pipeline

    def boot(self, runtime):
        self.orchestrator.lifecycle.initialize()
        self.orchestrator.lifecycle.boot()

        if self.boot_pipeline is not None:
            self.boot_pipeline.run(runtime)

        self.orchestrator.lifecycle.online()

        return runtime

    def health(self, runtime, container):
        return self.orchestrator.health(runtime, container)

    def recover(self, runtime, component, reason):
        return self.orchestrator.recover(
            runtime,
            component,
            reason,
        )
