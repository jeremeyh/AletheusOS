from .state import RuntimeLifecycleState


class RuntimeLifecycleManager:
    """
    Runtime Lifecycle Manager™

    Owns the canonical lifecycle of the runtime.
    """

    def __init__(self):

        self._state = RuntimeLifecycleState.CREATED

    @property
    def state(self):
        return self._state

    def transition(self, state: RuntimeLifecycleState):

        self._state = state

        return self._state

    def initialize(self):
        return self.transition(RuntimeLifecycleState.INITIALIZING)

    def boot(self):
        return self.transition(RuntimeLifecycleState.BOOTING)

    def online(self):
        return self.transition(RuntimeLifecycleState.ONLINE)

    def degrade(self):
        return self.transition(RuntimeLifecycleState.DEGRADED)

    def recover(self):
        return self.transition(RuntimeLifecycleState.RECOVERING)

    def shutdown(self):
        return self.transition(RuntimeLifecycleState.SHUTTING_DOWN)

    def offline(self):
        return self.transition(RuntimeLifecycleState.OFFLINE)
