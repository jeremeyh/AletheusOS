from aletheus.runtime.registrations.governance_architecture_commands import register_architecture_governance_commands
from aletheus.runtime.registrations.architecture_commands import register_architecture_commands
from aletheus.runtime.registrations.registry_commands import register_registry_commands
from aletheus.runtime.registrations.governance_commands import register_governance_commands
from aletheus.runtime.registrations.cluster_commands import register_cluster_commands
from aletheus.runtime.registrations.enterprise_commands import register_enterprise_commands
from aletheus.runtime.registrations.event_commands import register_event_commands
from aletheus.runtime.registrations.federation_commands import register_federation_commands
from aletheus.runtime.registrations.ha_commands import register_ha_commands
from aletheus.runtime.registrations.kernel_commands import register_kernel_commands
from aletheus.runtime.registrations.knowledge_graph_commands import register_knowledge_graph_commands
from aletheus.runtime.registrations.learning_commands import register_learning_commands
from aletheus.runtime.registrations.memory_commands import register_memory_commands
from aletheus.runtime.registrations.memory_mesh_commands import register_memory_mesh_commands
from aletheus.runtime.registrations.mission_v2_commands import register_mission_v2_commands
from aletheus.runtime.registrations.plugin_commands import register_plugin_commands
from aletheus.runtime.registrations.prediction_commands import register_prediction_commands
from aletheus.runtime.registrations.reasoning_commands import register_reasoning_commands
from aletheus.runtime.registrations.runtime_commands import register_runtime_commands
from aletheus.runtime.registrations.security_commands import register_security_commands
from aletheus.runtime.registrations.state_commands import register_state_commands
from aletheus.runtime.registrations.telemetry_commands import register_telemetry_commands
from aletheus.runtime.registrations.tenancy_commands import register_tenancy_commands
from aletheus.runtime.registrations.workflow_v2_commands import register_workflow_v2_commands
from aletheus.runtime.registrations.agent_commands import register_agent_commands
from aletheus.runtime.registrations.application_commands import register_application_commands
from aletheus.runtime.registrations.compatibility_commands import register_compatibility_commands
from aletheus.runtime.registrations.copilot_commands import register_copilot_commands
from aletheus.runtime.registrations.decision_commands import register_decision_commands
from aletheus.runtime.registrations.executive_commands import register_executive_commands
from aletheus.runtime.registrations.graph_commands import register_graph_commands
from aletheus.runtime.registrations.mission_commands import register_mission_commands
from aletheus.runtime.registrations.planning_commands import register_planning_commands
from aletheus.runtime.registrations.semantic_commands import register_semantic_commands
from aletheus.runtime.registrations.uil_commands import register_uil_commands
from aletheus.runtime.registrations.workspace_commands import register_workspace_commands


class RuntimeCommandBootstrapper:
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
        register_telemetry_commands(runtime)
        register_ha_commands(runtime)
        register_security_commands(runtime)
        register_tenancy_commands(runtime)
        register_memory_mesh_commands(runtime)
        register_knowledge_graph_commands(runtime)
        register_registry_commands(runtime)
        register_architecture_commands(runtime)
        register_architecture_governance_commands(runtime)
        register_governance_commands(runtime)
        # Legacy and compatibility command families.
        # These remain first-class bootstrap registrations
        # until their public contracts are formally retired.
        register_graph_commands(runtime)
        register_mission_commands(runtime)
        register_workspace_commands(runtime)
        register_application_commands(runtime)
        register_semantic_commands(runtime)
        register_executive_commands(runtime)
        register_agent_commands(runtime)
        register_planning_commands(runtime)
        register_copilot_commands(runtime)
        register_uil_commands(runtime)
        register_decision_commands(runtime)
        register_compatibility_commands(runtime)

        return runtime
