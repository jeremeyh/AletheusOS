from aletheus.runtime.registrations.kernel_commands import register_kernel_commands
from aletheus.runtime.registrations.learning_commands import register_learning_commands
from aletheus.runtime.registrations.memory_commands import register_memory_commands
from aletheus.runtime.registrations.prediction_commands import register_prediction_commands
from aletheus.runtime.registrations.reasoning_commands import register_reasoning_commands
from aletheus.runtime.registrations.runtime_commands import register_runtime_commands


class RuntimeCommandBootstrapper:
    """
    Runtime Command Bootstrapper™

    Coordinates registration of runtime command domains.
    """

    def bootstrap(self, runtime):

        register_runtime_commands(runtime)
        register_memory_commands(runtime)
        register_reasoning_commands(runtime)
        register_prediction_commands(runtime)
        register_learning_commands(runtime)
        register_kernel_commands(runtime)

        return runtime
