from aletheus.runtime.registrations.cluster_commands import register_cluster_commands
from aletheus.runtime.registrations.enterprise_commands import register_enterprise_commands
from aletheus.runtime.registrations.event_commands import register_event_commands
from aletheus.runtime.registrations.federation_commands import register_federation_commands
from aletheus.runtime.registrations.kernel_commands import register_kernel_commands
from aletheus.runtime.registrations.learning_commands import register_learning_commands
from aletheus.runtime.registrations.memory_commands import register_memory_commands
from aletheus.runtime.registrations.mission_v2_commands import register_mission_v2_commands
from aletheus.runtime.registrations.plugin_commands import register_plugin_commands
from aletheus.runtime.registrations.prediction_commands import register_prediction_commands
from aletheus.runtime.registrations.reasoning_commands import register_reasoning_commands
from aletheus.runtime.registrations.runtime_commands import register_runtime_commands
from aletheus.runtime.registrations.state_commands import register_state_commands
from aletheus.runtime.registrations.workflow_v2_commands import register_workflow_v2_commands


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
        register_mission_v2_commands(runtime)
        register_workflow_v2_commands(runtime)
        register_enterprise_commands(runtime)
        register_cluster_commands(runtime)
        register_plugin_commands(runtime)
        register_state_commands(runtime)
        register_event_commands(runtime)
        register_federation_commands(runtime)

        return runtime
