class RuntimeOrchestrator:
    """
    Runtime Orchestrator™

    Coordinates runtime orchestration components.
    """

    def __init__(
        self,
        lifecycle,
        service_provider,
        health_monitor,
        recovery_manager,
        capability_registry,
        policy_engine=None,
    ):

        self.lifecycle = lifecycle
        self.service_provider = service_provider
        self.health_monitor = health_monitor
        self.recovery_manager = recovery_manager
        self.capability_registry = capability_registry
        self.policy = policy_engine

    def _allowed(self, runtime, policy):

        if self.policy is None:
            return True

        return self.policy.evaluate(runtime, policy)

    def boot(self, runtime):

        if not self._allowed(runtime, "runtime.boot"):
            return False

        self.lifecycle.initialize()
        self.lifecycle.boot()

        self.service_provider.register(runtime)

        self.lifecycle.online()

        return True

    def health(self, runtime, container):

        if not self._allowed(runtime, "runtime.health"):
            return None

        return self.health_monitor.collect(
            self.lifecycle,
            container,
            self.capability_registry,
        )

    def recover(
        self,
        runtime,
        component,
        reason,
    ):

        if not self._allowed(runtime, "runtime.recover"):
            return None

        self.lifecycle.degrade()

        event = self.recovery_manager.recover(
            component,
            reason,
        )

        self.lifecycle.recover()
        self.lifecycle.online()

        return event
