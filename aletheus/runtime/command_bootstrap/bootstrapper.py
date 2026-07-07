from aletheus.runtime.registrations.runtime_commands import register_runtime_commands
from aletheus.runtime.registrations.memory_commands import register_memory_commands
from aletheus.runtime.registrations.reasoning_commands import register_reasoning_commands


class RuntimeCommandBootstrapper:
    """
    Runtime Command Bootstrapper™

    Coordinates registration of runtime command domains.
    """

    def bootstrap(self, runtime):

        register_runtime_commands(runtime)
        register_memory_commands(runtime)
        register_reasoning_commands(runtime)

        return runtime
