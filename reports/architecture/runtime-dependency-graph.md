# Runtime Dependency Graph

```mermaid
flowchart TD
    aletheus_runtime["aletheus.runtime"]
    aletheus_runtime_adapter["aletheus.runtime.adapter"]
    aletheus_runtime_adapters["aletheus.runtime.adapters"]
    aletheus_runtime_adapters_compatibility_adapter["aletheus.runtime.adapters.compatibility_adapter"]
    aletheus_runtime_adapters_event_adapter["aletheus.runtime.adapters.event_adapter"]
    aletheus_runtime_adapters_graph_adapter["aletheus.runtime.adapters.graph_adapter"]
    aletheus_runtime_adapters_mission_adapter["aletheus.runtime.adapters.mission_adapter"]
    aletheus_runtime_adapters_prediction_adapter["aletheus.runtime.adapters.prediction_adapter"]
    aletheus_runtime_adapters_runtime_adapter["aletheus.runtime.adapters.runtime_adapter"]
    aletheus_runtime_adapters_topology_registry_adapter["aletheus.runtime.adapters.topology_registry_adapter"]
    aletheus_runtime_adapters_universal_intelligence_adapter["aletheus.runtime.adapters.universal_intelligence_adapter"]
    aletheus_runtime_anchors["aletheus.runtime.anchors"]
    aletheus_runtime_anchors_analytics["aletheus.runtime.anchors.analytics"]
    aletheus_runtime_anchors_application["aletheus.runtime.anchors.application"]
    aletheus_runtime_anchors_architecture_council["aletheus.runtime.anchors.architecture_council"]
    aletheus_runtime_anchors_architecture_discovery["aletheus.runtime.anchors.architecture_discovery"]
    aletheus_runtime_anchors_architecture_evolution["aletheus.runtime.anchors.architecture_evolution"]
    aletheus_runtime_anchors_architecture_experiment["aletheus.runtime.anchors.architecture_experiment"]
    aletheus_runtime_anchors_architecture_hypothesis["aletheus.runtime.anchors.architecture_hypothesis"]
    aletheus_runtime_anchors_architecture_innovation["aletheus.runtime.anchors.architecture_innovation"]
    aletheus_runtime_anchors_architecture_intelligence["aletheus.runtime.anchors.architecture_intelligence"]
    aletheus_runtime_anchors_architecture_optimization["aletheus.runtime.anchors.architecture_optimization"]
    aletheus_runtime_anchors_architecture_proof["aletheus.runtime.anchors.architecture_proof"]
    aletheus_runtime_anchors_architecture_research["aletheus.runtime.anchors.architecture_research"]
    aletheus_runtime_anchors_architecture_selection["aletheus.runtime.anchors.architecture_selection"]
    aletheus_runtime_anchors_architecture_simulator["aletheus.runtime.anchors.architecture_simulator"]
    aletheus_runtime_anchors_architecture_steward["aletheus.runtime.anchors.architecture_steward"]
    aletheus_runtime_anchors_architecture_synthesis["aletheus.runtime.anchors.architecture_synthesis"]
    aletheus_runtime_anchors_autonomous_architect["aletheus.runtime.anchors.autonomous_architect"]
    aletheus_runtime_anchors_autonomous_validation["aletheus.runtime.anchors.autonomous_validation"]
    aletheus_runtime_anchors_base["aletheus.runtime.anchors.base"]
    aletheus_runtime_anchors_cognitive_adaptation["aletheus.runtime.anchors.cognitive_adaptation"]
    aletheus_runtime_anchors_cognitive_architect["aletheus.runtime.anchors.cognitive_architect"]
    aletheus_runtime_anchors_cognitive_architecture["aletheus.runtime.anchors.cognitive_architecture"]
    aletheus_runtime_anchors_cognitive_conflict["aletheus.runtime.anchors.cognitive_conflict"]
    aletheus_runtime_anchors_cognitive_consolidation["aletheus.runtime.anchors.cognitive_consolidation"]
    aletheus_runtime_anchors_cognitive_creativity["aletheus.runtime.anchors.cognitive_creativity"]
    aletheus_runtime_anchors_cognitive_dependency_graph["aletheus.runtime.anchors.cognitive_dependency_graph"]
    aletheus_runtime_anchors_cognitive_forecasting["aletheus.runtime.anchors.cognitive_forecasting"]
    aletheus_runtime_anchors_cognitive_governance["aletheus.runtime.anchors.cognitive_governance"]
    aletheus_runtime_anchors_cognitive_learning["aletheus.runtime.anchors.cognitive_learning"]
    aletheus_runtime_anchors_cognitive_memory_optimizer["aletheus.runtime.anchors.cognitive_memory_optimizer"]
    aletheus_runtime_anchors_cognitive_metrics["aletheus.runtime.anchors.cognitive_metrics"]
    aletheus_runtime_anchors_cognitive_monitoring["aletheus.runtime.anchors.cognitive_monitoring"]
    aletheus_runtime_anchors_cognitive_optimization["aletheus.runtime.anchors.cognitive_optimization"]
    aletheus_runtime_anchors_cognitive_pattern_mining["aletheus.runtime.anchors.cognitive_pattern_mining"]
    aletheus_runtime_anchors_cognitive_planning["aletheus.runtime.anchors.cognitive_planning"]
    aletheus_runtime_anchors_cognitive_registry["aletheus.runtime.anchors.cognitive_registry"]
    aletheus_runtime_anchors_cognitive_resources["aletheus.runtime.anchors.cognitive_resources"]
    aletheus_runtime_anchors_cognitive_rollback["aletheus.runtime.anchors.cognitive_rollback"]
    aletheus_runtime_anchors_cognitive_selection["aletheus.runtime.anchors.cognitive_selection"]
    aletheus_runtime_anchors_cognitive_self_improvement["aletheus.runtime.anchors.cognitive_self_improvement"]
    aletheus_runtime_anchors_cognitive_simulation["aletheus.runtime.anchors.cognitive_simulation"]
    aletheus_runtime_anchors_cognitive_strategy["aletheus.runtime.anchors.cognitive_strategy"]
    aletheus_runtime_anchors_cognitive_transfer["aletheus.runtime.anchors.cognitive_transfer"]
    aletheus_runtime_anchors_cognitive_verification["aletheus.runtime.anchors.cognitive_verification"]
    aletheus_runtime_anchors_consensus_memory["aletheus.runtime.anchors.consensus_memory"]
    aletheus_runtime_anchors_constitution["aletheus.runtime.anchors.constitution"]
    aletheus_runtime_anchors_constitutional_intelligence["aletheus.runtime.anchors.constitutional_intelligence"]
    aletheus_runtime_anchors_constitutional_reasoning["aletheus.runtime.anchors.constitutional_reasoning"]
    aletheus_runtime_anchors_continuity["aletheus.runtime.anchors.continuity"]
    aletheus_runtime_anchors_contracts["aletheus.runtime.anchors.contracts"]
    aletheus_runtime_anchors_decision_intelligence["aletheus.runtime.anchors.decision_intelligence"]
    aletheus_runtime_anchors_dependency["aletheus.runtime.anchors.dependency"]
    aletheus_runtime_anchors_deployment_governor["aletheus.runtime.anchors.deployment_governor"]
    aletheus_runtime_anchors_discovery["aletheus.runtime.anchors.discovery"]
    aletheus_runtime_anchors_emergent_detection["aletheus.runtime.anchors.emergent_detection"]
    aletheus_runtime_anchors_ethical_alignment["aletheus.runtime.anchors.ethical_alignment"]
    aletheus_runtime_anchors_evolution_certification["aletheus.runtime.anchors.evolution_certification"]
    aletheus_runtime_anchors_evolution_graph["aletheus.runtime.anchors.evolution_graph"]
    aletheus_runtime_anchors_execution["aletheus.runtime.anchors.execution"]
    aletheus_runtime_anchors_genesis_transition["aletheus.runtime.anchors.genesis_transition"]
    aletheus_runtime_anchors_governance["aletheus.runtime.anchors.governance"]
    aletheus_runtime_anchors_governance_intelligence["aletheus.runtime.anchors.governance_intelligence"]
    aletheus_runtime_anchors_healing["aletheus.runtime.anchors.healing"]
    aletheus_runtime_anchors_improvement_loop["aletheus.runtime.anchors.improvement_loop"]
    aletheus_runtime_anchors_institutional_memory["aletheus.runtime.anchors.institutional_memory"]
    aletheus_runtime_anchors_intelligence["aletheus.runtime.anchors.intelligence"]
    aletheus_runtime_anchors_intelligence_boundary["aletheus.runtime.anchors.intelligence_boundary"]
    aletheus_runtime_anchors_intelligence_continuity["aletheus.runtime.anchors.intelligence_continuity"]
    aletheus_runtime_anchors_judgment_optimization["aletheus.runtime.anchors.judgment_optimization"]
    aletheus_runtime_anchors_judgment_refinement["aletheus.runtime.anchors.judgment_refinement"]
    aletheus_runtime_anchors_knowledge["aletheus.runtime.anchors.knowledge"]
    aletheus_runtime_anchors_learning["aletheus.runtime.anchors.learning"]
    aletheus_runtime_anchors_lifecycle["aletheus.runtime.anchors.lifecycle"]
    aletheus_runtime_anchors_long_term_planning["aletheus.runtime.anchors.long_term_planning"]
    aletheus_runtime_anchors_memory["aletheus.runtime.anchors.memory"]
    aletheus_runtime_anchors_meta_reasoning["aletheus.runtime.anchors.meta_reasoning"]
    aletheus_runtime_anchors_migration["aletheus.runtime.anchors.migration"]
    aletheus_runtime_anchors_negotiation["aletheus.runtime.anchors.negotiation"]
    aletheus_runtime_anchors_optimization["aletheus.runtime.anchors.optimization"]
    aletheus_runtime_anchors_pattern_forecasting["aletheus.runtime.anchors.pattern_forecasting"]
    aletheus_runtime_anchors_pattern_intelligence["aletheus.runtime.anchors.pattern_intelligence"]
    aletheus_runtime_anchors_performance["aletheus.runtime.anchors.performance"]
    aletheus_runtime_anchors_portfolio["aletheus.runtime.anchors.portfolio"]
    aletheus_runtime_anchors_predictive["aletheus.runtime.anchors.predictive"]
    aletheus_runtime_anchors_proposals["aletheus.runtime.anchors.proposals"]
    aletheus_runtime_anchors_purpose_alignment["aletheus.runtime.anchors.purpose_alignment"]
    aletheus_runtime_anchors_registry["aletheus.runtime.anchors.registry"]
    aletheus_runtime_anchors_research["aletheus.runtime.anchors.research"]
    aletheus_runtime_anchors_resource_allocation["aletheus.runtime.anchors.resource_allocation"]
    aletheus_runtime_anchors_self_identity["aletheus.runtime.anchors.self_identity"]
    aletheus_runtime_anchors_simulation["aletheus.runtime.anchors.simulation"]
    aletheus_runtime_anchors_strategic_intelligence["aletheus.runtime.anchors.strategic_intelligence"]
    aletheus_runtime_anchors_strategic_planning["aletheus.runtime.anchors.strategic_planning"]
    aletheus_runtime_anchors_verification["aletheus.runtime.anchors.verification"]
    aletheus_runtime_anchors_wisdom_accumulation["aletheus.runtime.anchors.wisdom_accumulation"]
    aletheus_runtime_applications["aletheus.runtime.applications"]
    aletheus_runtime_applications_application_runtime["aletheus.runtime.applications.application_runtime"]
    aletheus_runtime_architecture["aletheus.runtime.architecture"]
    aletheus_runtime_architecture_validator["aletheus.runtime.architecture.validator"]
    aletheus_runtime_audit_command_surface["aletheus.runtime.audit.command_surface"]
    aletheus_runtime_audit_registry_snapshot["aletheus.runtime.audit.registry_snapshot"]
    aletheus_runtime_boot["aletheus.runtime.boot"]
    aletheus_runtime_boot_director["aletheus.runtime.boot_director"]
    aletheus_runtime_boot_director_director["aletheus.runtime.boot_director.director"]
    aletheus_runtime_boot_director_reporter["aletheus.runtime.boot_director.reporter"]
    aletheus_runtime_boot_phases["aletheus.runtime.boot_phases"]
    aletheus_runtime_boot_phases_agent_boot["aletheus.runtime.boot_phases.agent_boot"]
    aletheus_runtime_boot_phases_application_boot["aletheus.runtime.boot_phases.application_boot"]
    aletheus_runtime_boot_phases_command_bootstrap["aletheus.runtime.boot_phases.command_bootstrap"]
    aletheus_runtime_boot_phases_memory_initialization["aletheus.runtime.boot_phases.memory_initialization"]
    aletheus_runtime_boot_phases_runtime_state["aletheus.runtime.boot_phases.runtime_state"]
    aletheus_runtime_boot_phases_scheduler["aletheus.runtime.boot_phases.scheduler"]
    aletheus_runtime_boot_phases_service_groups["aletheus.runtime.boot_phases.service_groups"]
    aletheus_runtime_boot_phases_service_groups_ai_platform["aletheus.runtime.boot_phases.service_groups.ai_platform"]
    aletheus_runtime_boot_phases_service_groups_core["aletheus.runtime.boot_phases.service_groups.core"]
    aletheus_runtime_boot_phases_service_groups_foundation["aletheus.runtime.boot_phases.service_groups.foundation"]
    aletheus_runtime_boot_phases_service_groups_intelligence["aletheus.runtime.boot_phases.service_groups.intelligence"]
    aletheus_runtime_boot_phases_service_registration["aletheus.runtime.boot_phases.service_registration"]
    aletheus_runtime_boot_pipeline["aletheus.runtime.boot_pipeline"]
    aletheus_runtime_boot_pipeline_conditions["aletheus.runtime.boot_pipeline.conditions"]
    aletheus_runtime_boot_pipeline_context["aletheus.runtime.boot_pipeline.context"]
    aletheus_runtime_boot_pipeline_default_pipeline["aletheus.runtime.boot_pipeline.default_pipeline"]
    aletheus_runtime_boot_pipeline_dependencies["aletheus.runtime.boot_pipeline.dependencies"]
    aletheus_runtime_boot_pipeline_executor["aletheus.runtime.boot_pipeline.executor"]
    aletheus_runtime_boot_pipeline_manifest["aletheus.runtime.boot_pipeline.manifest"]
    aletheus_runtime_boot_pipeline_models["aletheus.runtime.boot_pipeline.models"]
    aletheus_runtime_boot_pipeline_pipeline["aletheus.runtime.boot_pipeline.pipeline"]
    aletheus_runtime_boot_pipeline_report["aletheus.runtime.boot_pipeline.report"]
    aletheus_runtime_boot_pipeline_reporter["aletheus.runtime.boot_pipeline.reporter"]
    aletheus_runtime_boot_pipeline_timing["aletheus.runtime.boot_pipeline.timing"]
    aletheus_runtime_bootstrap["aletheus.runtime.bootstrap"]
    aletheus_runtime_bootstrap_bootstrap_engine["aletheus.runtime.bootstrap.bootstrap_engine"]
    aletheus_runtime_bootstrap_runtime_bootstrap["aletheus.runtime.bootstrap.runtime_bootstrap"]
    aletheus_runtime_bootstrap_runtime_manifest_builder["aletheus.runtime.bootstrap.runtime_manifest_builder"]
    aletheus_runtime_builder["aletheus.runtime.builder"]
    aletheus_runtime_builder_builder["aletheus.runtime.builder.builder"]
    aletheus_runtime_capabilities["aletheus.runtime.capabilities"]
    aletheus_runtime_capabilities_registry["aletheus.runtime.capabilities.registry"]
    aletheus_runtime_capabilities_synchronizer["aletheus.runtime.capabilities.synchronizer"]
    aletheus_runtime_catalyst["aletheus.runtime.catalyst"]
    aletheus_runtime_catalyst_models["aletheus.runtime.catalyst.models"]
    aletheus_runtime_catalyst_optimizer["aletheus.runtime.catalyst.optimizer"]
    aletheus_runtime_catalyst_reporter["aletheus.runtime.catalyst.reporter"]
    aletheus_runtime_certification_boot_certification["aletheus.runtime.certification.boot_certification"]
    aletheus_runtime_certification_certifier["aletheus.runtime.certification.certifier"]
    aletheus_runtime_certification_federation_certifier["aletheus.runtime.certification.federation_certifier"]
    aletheus_runtime_circuits["aletheus.runtime.circuits"]
    aletheus_runtime_circuits_manager["aletheus.runtime.circuits.manager"]
    aletheus_runtime_circuits_models["aletheus.runtime.circuits.models"]
    aletheus_runtime_circuits_reporter["aletheus.runtime.circuits.reporter"]
    aletheus_runtime_command_bootstrap["aletheus.runtime.command_bootstrap"]
    aletheus_runtime_command_bootstrap_bootstrapper["aletheus.runtime.command_bootstrap.bootstrapper"]
    aletheus_runtime_command_handlers["aletheus.runtime.command_handlers"]
    aletheus_runtime_commands["aletheus.runtime.commands"]
    aletheus_runtime_commands_command_bus["aletheus.runtime.commands.command_bus"]
    aletheus_runtime_commands_contracts["aletheus.runtime.commands.contracts"]
    aletheus_runtime_commands_dispatcher["aletheus.runtime.commands.dispatcher"]
    aletheus_runtime_commands_errors["aletheus.runtime.commands.errors"]
    aletheus_runtime_commands_middleware["aletheus.runtime.commands.middleware"]
    aletheus_runtime_commands_models["aletheus.runtime.commands.models"]
    aletheus_runtime_commands_registry["aletheus.runtime.commands.registry"]
    aletheus_runtime_commands_runtime_commands["aletheus.runtime.commands.runtime_commands"]
    aletheus_runtime_commands_tests_test_compiled_registry_dispatcher["aletheus.runtime.commands.tests.test_compiled_registry_dispatcher"]
    aletheus_runtime_commands_tests_test_dispatcher["aletheus.runtime.commands.tests.test_dispatcher"]
    aletheus_runtime_commands_v2["aletheus.runtime.commands_v2"]
    aletheus_runtime_commands_v2_dispatcher["aletheus.runtime.commands_v2.dispatcher"]
    aletheus_runtime_commands_v2_models["aletheus.runtime.commands_v2.models"]
    aletheus_runtime_commands_v2_registry["aletheus.runtime.commands_v2.registry"]
    aletheus_runtime_commands_v2_reporter["aletheus.runtime.commands_v2.reporter"]
    aletheus_runtime_compat["aletheus.runtime.compat"]
    aletheus_runtime_compat_contracts["aletheus.runtime.compat.contracts"]
    aletheus_runtime_compat_registry["aletheus.runtime.compat.registry"]
    aletheus_runtime_compat_resolver["aletheus.runtime.compat.resolver"]
    aletheus_runtime_compatibility_layer["aletheus.runtime.compatibility_layer"]
    aletheus_runtime_compatibility_layer_layer["aletheus.runtime.compatibility_layer.layer"]
    aletheus_runtime_composition["aletheus.runtime.composition"]
    aletheus_runtime_composition_models["aletheus.runtime.composition.models"]
    aletheus_runtime_composition_reporter["aletheus.runtime.composition.reporter"]
    aletheus_runtime_composition_root["aletheus.runtime.composition.root"]
    aletheus_runtime_compression["aletheus.runtime.compression"]
    aletheus_runtime_compression_dashboard["aletheus.runtime.compression.dashboard"]
    aletheus_runtime_compression_models["aletheus.runtime.compression.models"]
    aletheus_runtime_compression_reporter["aletheus.runtime.compression.reporter"]
    aletheus_runtime_container["aletheus.runtime.container"]
    aletheus_runtime_container_container["aletheus.runtime.container.container"]
    aletheus_runtime_context["aletheus.runtime.context"]
    aletheus_runtime_contracts["aletheus.runtime.contracts"]
    aletheus_runtime_contracts_component["aletheus.runtime.contracts.component"]
    aletheus_runtime_contracts_components["aletheus.runtime.contracts.components"]
    aletheus_runtime_contracts_components_base["aletheus.runtime.contracts.components.base"]
    aletheus_runtime_contracts_errors["aletheus.runtime.contracts.errors"]
    aletheus_runtime_contracts_health["aletheus.runtime.contracts.health"]
    aletheus_runtime_contracts_lifecycle["aletheus.runtime.contracts.lifecycle"]
    aletheus_runtime_contracts_lifecycle_manager["aletheus.runtime.contracts.lifecycle_manager"]
    aletheus_runtime_contracts_managers["aletheus.runtime.contracts.managers"]
    aletheus_runtime_contracts_managers_registration_manager["aletheus.runtime.contracts.managers.registration_manager"]
    aletheus_runtime_contracts_manifest["aletheus.runtime.contracts.manifest"]
    aletheus_runtime_contracts_registration["aletheus.runtime.contracts.registration"]
    aletheus_runtime_convergence["aletheus.runtime.convergence"]
    aletheus_runtime_convergence_application_registry["aletheus.runtime.convergence.application_registry"]
    aletheus_runtime_convergence_capability_topology["aletheus.runtime.convergence.capability_topology"]
    aletheus_runtime_convergence_engine["aletheus.runtime.convergence.engine"]
    aletheus_runtime_convergence_genesis_registry["aletheus.runtime.convergence.genesis_registry"]
    aletheus_runtime_convergence_health_matrix["aletheus.runtime.convergence.health_matrix"]
    aletheus_runtime_core["aletheus.runtime.core"]
    aletheus_runtime_council_council["aletheus.runtime.council.council"]
    aletheus_runtime_dashboard["aletheus.runtime.dashboard"]
    aletheus_runtime_dashboard_dashboard["aletheus.runtime.dashboard.dashboard"]
    aletheus_runtime_decomposition["aletheus.runtime.decomposition"]
    aletheus_runtime_decomposition_analyzer["aletheus.runtime.decomposition.analyzer"]
    aletheus_runtime_decomposition_models["aletheus.runtime.decomposition.models"]
    aletheus_runtime_decomposition_planner["aletheus.runtime.decomposition.planner"]
    aletheus_runtime_decomposition_reporter["aletheus.runtime.decomposition.reporter"]
    aletheus_runtime_decomposition_responsibility["aletheus.runtime.decomposition.responsibility"]
    aletheus_runtime_diagnostics["aletheus.runtime.diagnostics"]
    aletheus_runtime_discovery["aletheus.runtime.discovery"]
    aletheus_runtime_discovery_discovery["aletheus.runtime.discovery.discovery"]
    aletheus_runtime_domains["aletheus.runtime.domains"]
    aletheus_runtime_domains_agent["aletheus.runtime.domains.agent"]
    aletheus_runtime_domains_application["aletheus.runtime.domains.application"]
    aletheus_runtime_domains_cluster["aletheus.runtime.domains.cluster"]
    aletheus_runtime_domains_copilot["aletheus.runtime.domains.copilot"]
    aletheus_runtime_domains_decision["aletheus.runtime.domains.decision"]
    aletheus_runtime_domains_enterprise["aletheus.runtime.domains.enterprise"]
    aletheus_runtime_domains_event_bus["aletheus.runtime.domains.event_bus"]
    aletheus_runtime_domains_executive["aletheus.runtime.domains.executive"]
    aletheus_runtime_domains_federation["aletheus.runtime.domains.federation"]
    aletheus_runtime_domains_high_availability["aletheus.runtime.domains.high_availability"]
    aletheus_runtime_domains_kernel["aletheus.runtime.domains.kernel"]
    aletheus_runtime_domains_knowledge_graph["aletheus.runtime.domains.knowledge_graph"]
    aletheus_runtime_domains_learning["aletheus.runtime.domains.learning"]
    aletheus_runtime_domains_memory["aletheus.runtime.domains.memory"]
    aletheus_runtime_domains_memory_mesh["aletheus.runtime.domains.memory_mesh"]
    aletheus_runtime_domains_mission["aletheus.runtime.domains.mission"]
    aletheus_runtime_domains_persistence["aletheus.runtime.domains.persistence"]
    aletheus_runtime_domains_planning["aletheus.runtime.domains.planning"]
    aletheus_runtime_domains_plugin["aletheus.runtime.domains.plugin"]
    aletheus_runtime_domains_prediction["aletheus.runtime.domains.prediction"]
    aletheus_runtime_domains_reasoning["aletheus.runtime.domains.reasoning"]
    aletheus_runtime_domains_runtime["aletheus.runtime.domains.runtime"]
    aletheus_runtime_domains_security["aletheus.runtime.domains.security"]
    aletheus_runtime_domains_semantic["aletheus.runtime.domains.semantic"]
    aletheus_runtime_domains_state["aletheus.runtime.domains.state"]
    aletheus_runtime_domains_telemetry["aletheus.runtime.domains.telemetry"]
    aletheus_runtime_domains_tenancy["aletheus.runtime.domains.tenancy"]
    aletheus_runtime_domains_workflow["aletheus.runtime.domains.workflow"]
    aletheus_runtime_events["aletheus.runtime.events"]
    aletheus_runtime_executive["aletheus.runtime.executive"]
    aletheus_runtime_executive_kernel["aletheus.runtime.executive.kernel"]
    aletheus_runtime_executive_models["aletheus.runtime.executive.models"]
    aletheus_runtime_executive_reporter["aletheus.runtime.executive.reporter"]
    aletheus_runtime_extraction["aletheus.runtime.extraction"]
    aletheus_runtime_extraction_models["aletheus.runtime.extraction.models"]
    aletheus_runtime_extraction_planner["aletheus.runtime.extraction.planner"]
    aletheus_runtime_extraction_reporter["aletheus.runtime.extraction.reporter"]
    aletheus_runtime_extraction_missions["aletheus.runtime.extraction_missions"]
    aletheus_runtime_extraction_missions_manager["aletheus.runtime.extraction_missions.manager"]
    aletheus_runtime_extraction_missions_models["aletheus.runtime.extraction_missions.models"]
    aletheus_runtime_extraction_missions_reporter["aletheus.runtime.extraction_missions.reporter"]
    aletheus_runtime_governance["aletheus.runtime.governance"]
    aletheus_runtime_governance_architecture_rules["aletheus.runtime.governance.architecture_rules"]
    aletheus_runtime_governance_governance_core["aletheus.runtime.governance.governance_core"]
    aletheus_runtime_governance_history["aletheus.runtime.governance.history"]
    aletheus_runtime_governance_principle_x["aletheus.runtime.governance.principle_x"]
    aletheus_runtime_governance_registry_rules["aletheus.runtime.governance.registry_rules"]
    aletheus_runtime_handlers["aletheus.runtime.handlers"]
    aletheus_runtime_handlers_compatibility_handlers["aletheus.runtime.handlers.compatibility_handlers"]
    aletheus_runtime_handlers_event_handlers["aletheus.runtime.handlers.event_handlers"]
    aletheus_runtime_handlers_graph_handlers["aletheus.runtime.handlers.graph_handlers"]
    aletheus_runtime_handlers_mission_handlers["aletheus.runtime.handlers.mission_handlers"]
    aletheus_runtime_hardening["aletheus.runtime.hardening"]
    aletheus_runtime_health["aletheus.runtime.health"]
    aletheus_runtime_health_monitor["aletheus.runtime.health.monitor"]
    aletheus_runtime_inspector["aletheus.runtime.inspector"]
    aletheus_runtime_inspector_runtime_inspector["aletheus.runtime.inspector.runtime_inspector"]
    aletheus_runtime_integrity["aletheus.runtime.integrity"]
    aletheus_runtime_integrity_boot_validator["aletheus.runtime.integrity.boot_validator"]
    aletheus_runtime_integrity_doctor["aletheus.runtime.integrity.doctor"]
    aletheus_runtime_integrity_invariants["aletheus.runtime.integrity.invariants"]
    aletheus_runtime_intelligence_spa_bridge["aletheus.runtime.intelligence.spa_bridge"]
    aletheus_runtime_job_queue["aletheus.runtime.job_queue"]
    aletheus_runtime_kernel["aletheus.runtime.kernel"]
    aletheus_runtime_kernel_dispatcher["aletheus.runtime.kernel.dispatcher"]
    aletheus_runtime_kernel_executor["aletheus.runtime.kernel.executor"]
    aletheus_runtime_kernel_kernel["aletheus.runtime.kernel.kernel"]
    aletheus_runtime_kernel_orchestrator["aletheus.runtime.kernel.orchestrator"]
    aletheus_runtime_kernel_scheduler["aletheus.runtime.kernel.scheduler"]
    aletheus_runtime_kernel_supervisor["aletheus.runtime.kernel.supervisor"]
    aletheus_runtime_lifecycle["aletheus.runtime.lifecycle"]
    aletheus_runtime_lifecycle_event_bus["aletheus.runtime.lifecycle.event_bus"]
    aletheus_runtime_lifecycle_events["aletheus.runtime.lifecycle.events"]
    aletheus_runtime_lifecycle_manager["aletheus.runtime.lifecycle.manager"]
    aletheus_runtime_lifecycle_models["aletheus.runtime.lifecycle.models"]
    aletheus_runtime_lifecycle_reporter["aletheus.runtime.lifecycle.reporter"]
    aletheus_runtime_lifecycle_resolver["aletheus.runtime.lifecycle.resolver"]
    aletheus_runtime_lifecycle_state["aletheus.runtime.lifecycle.state"]
    aletheus_runtime_managers["aletheus.runtime.managers"]
    aletheus_runtime_managers_certification_manager["aletheus.runtime.managers.certification_manager"]
    aletheus_runtime_managers_command_manager["aletheus.runtime.managers.command_manager"]
    aletheus_runtime_managers_governance_manager["aletheus.runtime.managers.governance_manager"]
    aletheus_runtime_managers_health_manager["aletheus.runtime.managers.health_manager"]
    aletheus_runtime_managers_invariant_manager["aletheus.runtime.managers.invariant_manager"]
    aletheus_runtime_managers_lifecycle_manager["aletheus.runtime.managers.lifecycle_manager"]
    aletheus_runtime_managers_observability_manager["aletheus.runtime.managers.observability_manager"]
    aletheus_runtime_managers_registration_manager["aletheus.runtime.managers.registration_manager"]
    aletheus_runtime_managers_registry_federation_manager["aletheus.runtime.managers.registry_federation_manager"]
    aletheus_runtime_managers_registry_manager["aletheus.runtime.managers.registry_manager"]
    aletheus_runtime_managers_runtime_facade["aletheus.runtime.managers.runtime_facade"]
    aletheus_runtime_managers_runtime_inspector["aletheus.runtime.managers.runtime_inspector"]
    aletheus_runtime_managers_snapshot_manager["aletheus.runtime.managers.snapshot_manager"]
    aletheus_runtime_managers_validation_manager["aletheus.runtime.managers.validation_manager"]
    aletheus_runtime_manifest["aletheus.runtime.manifest"]
    aletheus_runtime_metrics["aletheus.runtime.metrics"]
    aletheus_runtime_migration["aletheus.runtime.migration"]
    aletheus_runtime_migration_models["aletheus.runtime.migration.models"]
    aletheus_runtime_migration_reporter["aletheus.runtime.migration.reporter"]
    aletheus_runtime_migration_tracker["aletheus.runtime.migration.tracker"]
    aletheus_runtime_modules["aletheus.runtime.modules"]
    aletheus_runtime_orchestration["aletheus.runtime.orchestration"]
    aletheus_runtime_orchestration_orchestrator["aletheus.runtime.orchestration.orchestrator"]
    aletheus_runtime_patches_core_goal_list_fix["aletheus.runtime.patches.core.goal_list_fix"]
    aletheus_runtime_pipeline["aletheus.runtime.pipeline"]
    aletheus_runtime_policy["aletheus.runtime.policy"]
    aletheus_runtime_policy_engine["aletheus.runtime.policy.engine"]
    aletheus_runtime_providers["aletheus.runtime.providers"]
    aletheus_runtime_providers_service_provider["aletheus.runtime.providers.service_provider"]
    aletheus_runtime_readiness_federation_readiness_check["aletheus.runtime.readiness.federation_readiness_check"]
    aletheus_runtime_readiness_snapshot["aletheus.runtime.readiness.snapshot"]
    aletheus_runtime_recovery["aletheus.runtime.recovery"]
    aletheus_runtime_recovery_manager["aletheus.runtime.recovery.manager"]
    aletheus_runtime_registration["aletheus.runtime.registration"]
    aletheus_runtime_registration_manager["aletheus.runtime.registration.manager"]
    aletheus_runtime_registration_models["aletheus.runtime.registration.models"]
    aletheus_runtime_registration_reporter["aletheus.runtime.registration.reporter"]
    aletheus_runtime_registrations["aletheus.runtime.registrations"]
    aletheus_runtime_registrations_agent_commands["aletheus.runtime.registrations.agent_commands"]
    aletheus_runtime_registrations_application_commands["aletheus.runtime.registrations.application_commands"]
    aletheus_runtime_registrations_architecture_commands["aletheus.runtime.registrations.architecture_commands"]
    aletheus_runtime_registrations_cluster_commands["aletheus.runtime.registrations.cluster_commands"]
    aletheus_runtime_registrations_compatibility_alias_commands["aletheus.runtime.registrations.compatibility_alias_commands"]
    aletheus_runtime_registrations_compatibility_commands["aletheus.runtime.registrations.compatibility_commands"]
    aletheus_runtime_registrations_copilot_commands["aletheus.runtime.registrations.copilot_commands"]
    aletheus_runtime_registrations_decision_commands["aletheus.runtime.registrations.decision_commands"]
    aletheus_runtime_registrations_enterprise_commands["aletheus.runtime.registrations.enterprise_commands"]
    aletheus_runtime_registrations_event_commands["aletheus.runtime.registrations.event_commands"]
    aletheus_runtime_registrations_executive_commands["aletheus.runtime.registrations.executive_commands"]
    aletheus_runtime_registrations_federation_commands["aletheus.runtime.registrations.federation_commands"]
    aletheus_runtime_registrations_governance_architecture_commands["aletheus.runtime.registrations.governance_architecture_commands"]
    aletheus_runtime_registrations_governance_commands["aletheus.runtime.registrations.governance_commands"]
    aletheus_runtime_registrations_graph_commands["aletheus.runtime.registrations.graph_commands"]
    aletheus_runtime_registrations_ha_commands["aletheus.runtime.registrations.ha_commands"]
    aletheus_runtime_registrations_kernel_commands["aletheus.runtime.registrations.kernel_commands"]
    aletheus_runtime_registrations_kernel_compatibility_commands["aletheus.runtime.registrations.kernel_compatibility_commands"]
    aletheus_runtime_registrations_knowledge_graph_commands["aletheus.runtime.registrations.knowledge_graph_commands"]
    aletheus_runtime_registrations_learning_commands["aletheus.runtime.registrations.learning_commands"]
    aletheus_runtime_registrations_memory_commands["aletheus.runtime.registrations.memory_commands"]
    aletheus_runtime_registrations_memory_mesh_commands["aletheus.runtime.registrations.memory_mesh_commands"]
    aletheus_runtime_registrations_mission_commands["aletheus.runtime.registrations.mission_commands"]
    aletheus_runtime_registrations_mission_v2_commands["aletheus.runtime.registrations.mission_v2_commands"]
    aletheus_runtime_registrations_planning_commands["aletheus.runtime.registrations.planning_commands"]
    aletheus_runtime_registrations_plugin_commands["aletheus.runtime.registrations.plugin_commands"]
    aletheus_runtime_registrations_prediction_commands["aletheus.runtime.registrations.prediction_commands"]
    aletheus_runtime_registrations_reasoning_commands["aletheus.runtime.registrations.reasoning_commands"]
    aletheus_runtime_registrations_registry_commands["aletheus.runtime.registrations.registry_commands"]
    aletheus_runtime_registrations_release_commands["aletheus.runtime.registrations.release_commands"]
    aletheus_runtime_registrations_runtime_commands["aletheus.runtime.registrations.runtime_commands"]
    aletheus_runtime_registrations_security_commands["aletheus.runtime.registrations.security_commands"]
    aletheus_runtime_registrations_semantic_commands["aletheus.runtime.registrations.semantic_commands"]
    aletheus_runtime_registrations_state_commands["aletheus.runtime.registrations.state_commands"]
    aletheus_runtime_registrations_telemetry_commands["aletheus.runtime.registrations.telemetry_commands"]
    aletheus_runtime_registrations_tenancy_commands["aletheus.runtime.registrations.tenancy_commands"]
    aletheus_runtime_registrations_uil_commands["aletheus.runtime.registrations.uil_commands"]
    aletheus_runtime_registrations_workflow_commands["aletheus.runtime.registrations.workflow_commands"]
    aletheus_runtime_registrations_workflow_v2_commands["aletheus.runtime.registrations.workflow_v2_commands"]
    aletheus_runtime_registrations_workspace_commands["aletheus.runtime.registrations.workspace_commands"]
    aletheus_runtime_registries["aletheus.runtime.registries"]
    aletheus_runtime_registry["aletheus.runtime.registry"]
    aletheus_runtime_registry_compatibility["aletheus.runtime.registry.compatibility"]
    aletheus_runtime_registry_runtime_registry["aletheus.runtime.registry.runtime_registry"]
    aletheus_runtime_relay["aletheus.runtime.relay"]
    aletheus_runtime_relay_models["aletheus.runtime.relay.models"]
    aletheus_runtime_relay_network["aletheus.runtime.relay.network"]
    aletheus_runtime_relay_reporter["aletheus.runtime.relay.reporter"]
    aletheus_runtime_release_genesis6_report["aletheus.runtime.release.genesis6_report"]
    aletheus_runtime_release_genesis6_review["aletheus.runtime.release.genesis6_review"]
    aletheus_runtime_release_genesis6_validator["aletheus.runtime.release.genesis6_validator"]
    aletheus_runtime_release_manifest["aletheus.runtime.release.manifest"]
    aletheus_runtime_scheduler["aletheus.runtime.scheduler"]
    aletheus_runtime_service_mesh["aletheus.runtime.service_mesh"]
    aletheus_runtime_service_mesh_mesh["aletheus.runtime.service_mesh.mesh"]
    aletheus_runtime_service_mesh_models["aletheus.runtime.service_mesh.models"]
    aletheus_runtime_service_mesh_reporter["aletheus.runtime.service_mesh.reporter"]
    aletheus_runtime_services["aletheus.runtime.services"]
    aletheus_runtime_services_registry_federation_bootstrap["aletheus.runtime.services.registry_federation_bootstrap"]
    aletheus_runtime_services_registry_federation_registration["aletheus.runtime.services.registry_federation_registration"]
    aletheus_runtime_services_registry_federation_service["aletheus.runtime.services.registry_federation_service"]
    aletheus_runtime_services_service_registry["aletheus.runtime.services.service_registry"]
    aletheus_runtime_spa["aletheus.runtime.spa"]
    aletheus_runtime_spa_anchor_analysis["aletheus.runtime.spa.anchor_analysis"]
    aletheus_runtime_universal["aletheus.runtime.universal"]
    aletheus_runtime_universal_application_binding["aletheus.runtime.universal.application_binding"]
    aletheus_runtime_universal_capability_registry["aletheus.runtime.universal.capability_registry"]
    aletheus_runtime_universal_engine["aletheus.runtime.universal.engine"]
    aletheus_runtime_universal_runtime_topology["aletheus.runtime.universal.runtime_topology"]
    aletheus_runtime_workflow["aletheus.runtime.workflow"]
    aletheus_runtime --> aletheus_runtime_context
    aletheus_runtime --> aletheus_runtime_core
    aletheus_runtime --> aletheus_runtime_pipeline
    aletheus_runtime --> aletheus_runtime_workflow
    aletheus_runtime_anchors --> aletheus_runtime_anchors_analytics
    aletheus_runtime_anchors --> aletheus_runtime_anchors_application
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_council
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_discovery
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_evolution
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_experiment
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_hypothesis
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_innovation
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_intelligence
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_optimization
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_proof
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_research
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_selection
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_simulator
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_steward
    aletheus_runtime_anchors --> aletheus_runtime_anchors_architecture_synthesis
    aletheus_runtime_anchors --> aletheus_runtime_anchors_autonomous_architect
    aletheus_runtime_anchors --> aletheus_runtime_anchors_autonomous_validation
    aletheus_runtime_anchors --> aletheus_runtime_anchors_base
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_adaptation
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_architect
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_architecture
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_conflict
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_consolidation
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_creativity
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_dependency_graph
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_forecasting
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_governance
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_learning
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_memory_optimizer
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_metrics
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_monitoring
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_optimization
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_pattern_mining
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_planning
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_registry
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_resources
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_rollback
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_selection
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_self_improvement
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_simulation
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_strategy
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_transfer
    aletheus_runtime_anchors --> aletheus_runtime_anchors_cognitive_verification
    aletheus_runtime_anchors --> aletheus_runtime_anchors_consensus_memory
    aletheus_runtime_anchors --> aletheus_runtime_anchors_constitution
    aletheus_runtime_anchors --> aletheus_runtime_anchors_constitutional_intelligence
    aletheus_runtime_anchors --> aletheus_runtime_anchors_constitutional_reasoning
    aletheus_runtime_anchors --> aletheus_runtime_anchors_continuity
    aletheus_runtime_anchors --> aletheus_runtime_anchors_contracts
    aletheus_runtime_anchors --> aletheus_runtime_anchors_decision_intelligence
    aletheus_runtime_anchors --> aletheus_runtime_anchors_dependency
    aletheus_runtime_anchors --> aletheus_runtime_anchors_deployment_governor
    aletheus_runtime_anchors --> aletheus_runtime_anchors_discovery
    aletheus_runtime_anchors --> aletheus_runtime_anchors_emergent_detection
    aletheus_runtime_anchors --> aletheus_runtime_anchors_ethical_alignment
    aletheus_runtime_anchors --> aletheus_runtime_anchors_evolution_certification
    aletheus_runtime_anchors --> aletheus_runtime_anchors_evolution_graph
    aletheus_runtime_anchors --> aletheus_runtime_anchors_execution
    aletheus_runtime_anchors --> aletheus_runtime_anchors_genesis_transition
    aletheus_runtime_anchors --> aletheus_runtime_anchors_governance
    aletheus_runtime_anchors --> aletheus_runtime_anchors_governance_intelligence
    aletheus_runtime_anchors --> aletheus_runtime_anchors_healing
    aletheus_runtime_anchors --> aletheus_runtime_anchors_improvement_loop
    aletheus_runtime_anchors --> aletheus_runtime_anchors_institutional_memory
    aletheus_runtime_anchors --> aletheus_runtime_anchors_intelligence
    aletheus_runtime_anchors --> aletheus_runtime_anchors_intelligence_boundary
    aletheus_runtime_anchors --> aletheus_runtime_anchors_intelligence_continuity
    aletheus_runtime_anchors --> aletheus_runtime_anchors_judgment_optimization
    aletheus_runtime_anchors --> aletheus_runtime_anchors_judgment_refinement
    aletheus_runtime_anchors --> aletheus_runtime_anchors_knowledge
    aletheus_runtime_anchors --> aletheus_runtime_anchors_learning
    aletheus_runtime_anchors --> aletheus_runtime_anchors_lifecycle
    aletheus_runtime_anchors --> aletheus_runtime_anchors_long_term_planning
    aletheus_runtime_anchors --> aletheus_runtime_anchors_memory
    aletheus_runtime_anchors --> aletheus_runtime_anchors_meta_reasoning
    aletheus_runtime_anchors --> aletheus_runtime_anchors_migration
    aletheus_runtime_anchors --> aletheus_runtime_anchors_negotiation
    aletheus_runtime_anchors --> aletheus_runtime_anchors_optimization
    aletheus_runtime_anchors --> aletheus_runtime_anchors_pattern_forecasting
    aletheus_runtime_anchors --> aletheus_runtime_anchors_pattern_intelligence
    aletheus_runtime_anchors --> aletheus_runtime_anchors_performance
    aletheus_runtime_anchors --> aletheus_runtime_anchors_portfolio
    aletheus_runtime_anchors --> aletheus_runtime_anchors_predictive
    aletheus_runtime_anchors --> aletheus_runtime_anchors_proposals
    aletheus_runtime_anchors --> aletheus_runtime_anchors_purpose_alignment
    aletheus_runtime_anchors --> aletheus_runtime_anchors_registry
    aletheus_runtime_anchors --> aletheus_runtime_anchors_research
    aletheus_runtime_anchors --> aletheus_runtime_anchors_resource_allocation
    aletheus_runtime_anchors --> aletheus_runtime_anchors_self_identity
    aletheus_runtime_anchors --> aletheus_runtime_anchors_simulation
    aletheus_runtime_anchors --> aletheus_runtime_anchors_strategic_intelligence
    aletheus_runtime_anchors --> aletheus_runtime_anchors_strategic_planning
    aletheus_runtime_anchors --> aletheus_runtime_anchors_verification
    aletheus_runtime_anchors --> aletheus_runtime_anchors_wisdom_accumulation
    aletheus_runtime_anchors_application --> aletheus_runtime_anchors_base
    aletheus_runtime_anchors_intelligence --> aletheus_runtime_anchors_base
    aletheus_runtime_anchors_knowledge --> aletheus_runtime_anchors_base
    aletheus_runtime_anchors_memory --> aletheus_runtime_anchors_base
    aletheus_runtime_applications --> aletheus_runtime_applications_application_runtime
    aletheus_runtime_architecture --> aletheus_runtime_architecture_validator
    aletheus_runtime_boot_director --> aletheus_runtime_boot_director_director
    aletheus_runtime_boot_director --> aletheus_runtime_boot_director_reporter
    aletheus_runtime_boot_phases --> aletheus_runtime_boot_phases_agent_boot
    aletheus_runtime_boot_phases --> aletheus_runtime_boot_phases_application_boot
    aletheus_runtime_boot_phases --> aletheus_runtime_boot_phases_command_bootstrap
    aletheus_runtime_boot_phases --> aletheus_runtime_boot_phases_memory_initialization
    aletheus_runtime_boot_phases --> aletheus_runtime_boot_phases_runtime_state
    aletheus_runtime_boot_phases --> aletheus_runtime_boot_phases_scheduler
    aletheus_runtime_boot_phases --> aletheus_runtime_boot_phases_service_registration
    aletheus_runtime_boot_phases_command_bootstrap --> aletheus_runtime_command_bootstrap_bootstrapper
    aletheus_runtime_boot_phases_service_groups --> aletheus_runtime_boot_phases_service_groups_ai_platform
    aletheus_runtime_boot_phases_service_groups --> aletheus_runtime_boot_phases_service_groups_core
    aletheus_runtime_boot_phases_service_groups --> aletheus_runtime_boot_phases_service_groups_foundation
    aletheus_runtime_boot_phases_service_groups --> aletheus_runtime_boot_phases_service_groups_intelligence
    aletheus_runtime_boot_phases_service_registration --> aletheus_runtime_boot_phases_service_groups
    aletheus_runtime_boot_pipeline --> aletheus_runtime_boot_pipeline_default_pipeline
    aletheus_runtime_boot_pipeline --> aletheus_runtime_boot_pipeline_pipeline
    aletheus_runtime_boot_pipeline_context --> aletheus_runtime_boot_pipeline_report
    aletheus_runtime_boot_pipeline_default_pipeline --> aletheus_runtime_boot_phases
    aletheus_runtime_boot_pipeline_default_pipeline --> aletheus_runtime_boot_pipeline_pipeline
    aletheus_runtime_boot_pipeline_pipeline --> aletheus_runtime_boot_pipeline_conditions
    aletheus_runtime_boot_pipeline_pipeline --> aletheus_runtime_boot_pipeline_context
    aletheus_runtime_boot_pipeline_pipeline --> aletheus_runtime_boot_pipeline_timing
    aletheus_runtime_bootstrap --> aletheus_runtime_bootstrap_runtime_bootstrap
    aletheus_runtime_bootstrap --> aletheus_runtime_bootstrap_runtime_manifest_builder
    aletheus_runtime_bootstrap_bootstrap_engine --> aletheus_runtime_managers
    aletheus_runtime_builder --> aletheus_runtime_builder_builder
    aletheus_runtime_builder_builder --> aletheus_runtime_container
    aletheus_runtime_capabilities --> aletheus_runtime_capabilities_registry
    aletheus_runtime_capabilities --> aletheus_runtime_capabilities_synchronizer
    aletheus_runtime_capabilities_synchronizer --> aletheus_runtime_discovery
    aletheus_runtime_catalyst --> aletheus_runtime_catalyst_models
    aletheus_runtime_catalyst --> aletheus_runtime_catalyst_optimizer
    aletheus_runtime_catalyst --> aletheus_runtime_catalyst_reporter
    aletheus_runtime_catalyst_optimizer --> aletheus_runtime_catalyst_models
    aletheus_runtime_circuits --> aletheus_runtime_circuits_manager
    aletheus_runtime_circuits --> aletheus_runtime_circuits_models
    aletheus_runtime_circuits --> aletheus_runtime_circuits_reporter
    aletheus_runtime_circuits_manager --> aletheus_runtime_circuits_models
    aletheus_runtime_command_bootstrap --> aletheus_runtime_command_bootstrap_bootstrapper
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_agent_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_application_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_architecture_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_cluster_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_compatibility_alias_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_compatibility_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_copilot_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_decision_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_enterprise_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_event_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_executive_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_federation_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_governance_architecture_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_governance_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_graph_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_ha_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_kernel_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_kernel_compatibility_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_knowledge_graph_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_learning_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_memory_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_memory_mesh_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_mission_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_mission_v2_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_planning_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_plugin_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_prediction_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_reasoning_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_registry_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_release_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_runtime_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_security_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_semantic_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_state_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_telemetry_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_tenancy_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_uil_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_workflow_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_workflow_v2_commands
    aletheus_runtime_command_bootstrap_bootstrapper --> aletheus_runtime_registrations_workspace_commands
    aletheus_runtime_commands --> aletheus_runtime_commands_command_bus
    aletheus_runtime_commands --> aletheus_runtime_commands_contracts
    aletheus_runtime_commands --> aletheus_runtime_commands_dispatcher
    aletheus_runtime_commands --> aletheus_runtime_commands_errors
    aletheus_runtime_commands --> aletheus_runtime_commands_models
    aletheus_runtime_commands --> aletheus_runtime_commands_registry
    aletheus_runtime_commands_command_bus --> aletheus_runtime_commands_runtime_commands
    aletheus_runtime_commands_command_bus --> aletheus_runtime_commands_v2_registry
    aletheus_runtime_commands_command_bus --> aletheus_runtime_context
    aletheus_runtime_commands_dispatcher --> aletheus_runtime_commands_contracts
    aletheus_runtime_commands_dispatcher --> aletheus_runtime_commands_errors
    aletheus_runtime_commands_dispatcher --> aletheus_runtime_commands_models
    aletheus_runtime_commands_dispatcher --> aletheus_runtime_commands_registry
    aletheus_runtime_commands_middleware --> aletheus_runtime_commands_contracts
    aletheus_runtime_commands_middleware --> aletheus_runtime_commands_errors
    aletheus_runtime_commands_models --> aletheus_runtime_commands_contracts
    aletheus_runtime_commands_registry --> aletheus_runtime_commands_errors
    aletheus_runtime_commands_registry --> aletheus_runtime_commands_models
    aletheus_runtime_commands_tests_test_compiled_registry_dispatcher --> aletheus_runtime_commands_v2_registry
    aletheus_runtime_commands_tests_test_dispatcher --> aletheus_runtime_commands
    aletheus_runtime_commands_v2 --> aletheus_runtime_commands_v2_models
    aletheus_runtime_commands_v2 --> aletheus_runtime_commands_v2_registry
    aletheus_runtime_commands_v2 --> aletheus_runtime_commands_v2_reporter
    aletheus_runtime_commands_v2_dispatcher --> aletheus_runtime_commands_v2_models
    aletheus_runtime_commands_v2_dispatcher --> aletheus_runtime_context
    aletheus_runtime_commands_v2_registry --> aletheus_runtime_commands_v2_dispatcher
    aletheus_runtime_commands_v2_registry --> aletheus_runtime_commands_v2_models
    aletheus_runtime_compat --> aletheus_runtime_compat_contracts
    aletheus_runtime_compat --> aletheus_runtime_compat_registry
    aletheus_runtime_compat --> aletheus_runtime_compat_resolver
    aletheus_runtime_compat_resolver --> aletheus_runtime_compat_registry
    aletheus_runtime_compatibility_layer --> aletheus_runtime_compatibility_layer_layer
    aletheus_runtime_composition --> aletheus_runtime_composition_root
    aletheus_runtime_composition_root --> aletheus_runtime_boot_pipeline
    aletheus_runtime_composition_root --> aletheus_runtime_capabilities
    aletheus_runtime_composition_root --> aletheus_runtime_health
    aletheus_runtime_composition_root --> aletheus_runtime_kernel
    aletheus_runtime_composition_root --> aletheus_runtime_lifecycle
    aletheus_runtime_composition_root --> aletheus_runtime_orchestration
    aletheus_runtime_composition_root --> aletheus_runtime_policy
    aletheus_runtime_composition_root --> aletheus_runtime_providers
    aletheus_runtime_composition_root --> aletheus_runtime_recovery
    aletheus_runtime_compression --> aletheus_runtime_compression_dashboard
    aletheus_runtime_compression --> aletheus_runtime_compression_reporter
    aletheus_runtime_compression_dashboard --> aletheus_runtime_compression_models
    aletheus_runtime_container --> aletheus_runtime_container_container
    aletheus_runtime_contracts_component --> aletheus_runtime_contracts_health
    aletheus_runtime_contracts_component --> aletheus_runtime_contracts_manifest
    aletheus_runtime_contracts_components_base --> aletheus_runtime_contracts_component
    aletheus_runtime_contracts_components_base --> aletheus_runtime_contracts_health
    aletheus_runtime_contracts_components_base --> aletheus_runtime_contracts_lifecycle
    aletheus_runtime_contracts_components_base --> aletheus_runtime_contracts_manifest
    aletheus_runtime_contracts_lifecycle_manager --> aletheus_runtime_contracts_component
    aletheus_runtime_contracts_managers_registration_manager --> aletheus_runtime_contracts_component
    aletheus_runtime_contracts_managers_registration_manager --> aletheus_runtime_contracts_errors
    aletheus_runtime_contracts_managers_registration_manager --> aletheus_runtime_contracts_registration
    aletheus_runtime_contracts_registration --> aletheus_runtime_contracts_component
    aletheus_runtime_convergence --> aletheus_runtime_convergence_engine
    aletheus_runtime_convergence_engine --> aletheus_runtime_convergence_application_registry
    aletheus_runtime_convergence_engine --> aletheus_runtime_convergence_capability_topology
    aletheus_runtime_convergence_engine --> aletheus_runtime_convergence_genesis_registry
    aletheus_runtime_convergence_engine --> aletheus_runtime_convergence_health_matrix
    aletheus_runtime_core --> aletheus_runtime_adapters_compatibility_adapter
    aletheus_runtime_core --> aletheus_runtime_adapters_event_adapter
    aletheus_runtime_core --> aletheus_runtime_adapters_graph_adapter
    aletheus_runtime_core --> aletheus_runtime_adapters_mission_adapter
    aletheus_runtime_core --> aletheus_runtime_adapters_prediction_adapter
    aletheus_runtime_core --> aletheus_runtime_adapters_runtime_adapter
    aletheus_runtime_core --> aletheus_runtime_adapters_universal_intelligence_adapter
    aletheus_runtime_core --> aletheus_runtime_anchors
    aletheus_runtime_core --> aletheus_runtime_architecture_validator
    aletheus_runtime_core --> aletheus_runtime_audit_command_surface
    aletheus_runtime_core --> aletheus_runtime_boot_pipeline
    aletheus_runtime_core --> aletheus_runtime_certification_boot_certification
    aletheus_runtime_core --> aletheus_runtime_command_bootstrap_bootstrapper
    aletheus_runtime_core --> aletheus_runtime_commands
    aletheus_runtime_core --> aletheus_runtime_compat
    aletheus_runtime_core --> aletheus_runtime_compatibility_layer
    aletheus_runtime_core --> aletheus_runtime_context
    aletheus_runtime_core --> aletheus_runtime_diagnostics
    aletheus_runtime_core --> aletheus_runtime_events
    aletheus_runtime_core --> aletheus_runtime_governance
    aletheus_runtime_core --> aletheus_runtime_governance_architecture_rules
    aletheus_runtime_core --> aletheus_runtime_governance_history
    aletheus_runtime_core --> aletheus_runtime_governance_registry_rules
    aletheus_runtime_core --> aletheus_runtime_hardening
    aletheus_runtime_core --> aletheus_runtime_integrity
    aletheus_runtime_core --> aletheus_runtime_intelligence_spa_bridge
    aletheus_runtime_core --> aletheus_runtime_job_queue
    aletheus_runtime_core --> aletheus_runtime_kernel
    aletheus_runtime_core --> aletheus_runtime_managers
    aletheus_runtime_core --> aletheus_runtime_managers_runtime_facade
    aletheus_runtime_core --> aletheus_runtime_metrics
    aletheus_runtime_core --> aletheus_runtime_pipeline
    aletheus_runtime_core --> aletheus_runtime_providers
    aletheus_runtime_core --> aletheus_runtime_readiness_snapshot
    aletheus_runtime_core --> aletheus_runtime_registries
    aletheus_runtime_core --> aletheus_runtime_registry_compatibility
    aletheus_runtime_core --> aletheus_runtime_registry_runtime_registry
    aletheus_runtime_core --> aletheus_runtime_release_genesis6_report
    aletheus_runtime_core --> aletheus_runtime_release_genesis6_review
    aletheus_runtime_core --> aletheus_runtime_release_genesis6_validator
    aletheus_runtime_core --> aletheus_runtime_scheduler
    aletheus_runtime_core --> aletheus_runtime_services
    aletheus_runtime_core --> aletheus_runtime_workflow
    aletheus_runtime_dashboard --> aletheus_runtime_dashboard_dashboard
    aletheus_runtime_decomposition --> aletheus_runtime_decomposition_analyzer
    aletheus_runtime_decomposition --> aletheus_runtime_decomposition_models
    aletheus_runtime_decomposition --> aletheus_runtime_decomposition_planner
    aletheus_runtime_decomposition --> aletheus_runtime_decomposition_reporter
    aletheus_runtime_decomposition --> aletheus_runtime_decomposition_responsibility
    aletheus_runtime_decomposition_analyzer --> aletheus_runtime_decomposition_models
    aletheus_runtime_decomposition_planner --> aletheus_runtime_decomposition_analyzer
    aletheus_runtime_decomposition_planner --> aletheus_runtime_decomposition_models
    aletheus_runtime_decomposition_planner --> aletheus_runtime_decomposition_responsibility
    aletheus_runtime_decomposition_responsibility --> aletheus_runtime_decomposition_models
    aletheus_runtime_discovery --> aletheus_runtime_discovery_discovery
    aletheus_runtime_domains --> aletheus_runtime_domains_agent
    aletheus_runtime_domains --> aletheus_runtime_domains_cluster
    aletheus_runtime_domains --> aletheus_runtime_domains_copilot
    aletheus_runtime_domains --> aletheus_runtime_domains_decision
    aletheus_runtime_domains --> aletheus_runtime_domains_enterprise
    aletheus_runtime_domains --> aletheus_runtime_domains_event_bus
    aletheus_runtime_domains --> aletheus_runtime_domains_federation
    aletheus_runtime_domains --> aletheus_runtime_domains_high_availability
    aletheus_runtime_domains --> aletheus_runtime_domains_kernel
    aletheus_runtime_domains --> aletheus_runtime_domains_knowledge_graph
    aletheus_runtime_domains --> aletheus_runtime_domains_learning
    aletheus_runtime_domains --> aletheus_runtime_domains_memory
    aletheus_runtime_domains --> aletheus_runtime_domains_memory_mesh
    aletheus_runtime_domains --> aletheus_runtime_domains_mission
    aletheus_runtime_domains --> aletheus_runtime_domains_persistence
    aletheus_runtime_domains --> aletheus_runtime_domains_planning
    aletheus_runtime_domains --> aletheus_runtime_domains_plugin
    aletheus_runtime_domains --> aletheus_runtime_domains_prediction
    aletheus_runtime_domains --> aletheus_runtime_domains_reasoning
    aletheus_runtime_domains --> aletheus_runtime_domains_runtime
    aletheus_runtime_domains --> aletheus_runtime_domains_security
    aletheus_runtime_domains --> aletheus_runtime_domains_telemetry
    aletheus_runtime_domains --> aletheus_runtime_domains_tenancy
    aletheus_runtime_domains --> aletheus_runtime_domains_workflow
    aletheus_runtime_executive --> aletheus_runtime_executive_kernel
    aletheus_runtime_executive --> aletheus_runtime_executive_models
    aletheus_runtime_executive --> aletheus_runtime_executive_reporter
    aletheus_runtime_executive_kernel --> aletheus_runtime_executive_models
    aletheus_runtime_extraction --> aletheus_runtime_extraction_planner
    aletheus_runtime_extraction --> aletheus_runtime_extraction_reporter
    aletheus_runtime_extraction_planner --> aletheus_runtime_extraction_models
    aletheus_runtime_extraction_missions --> aletheus_runtime_extraction_missions_manager
    aletheus_runtime_extraction_missions --> aletheus_runtime_extraction_missions_reporter
    aletheus_runtime_extraction_missions_manager --> aletheus_runtime_extraction_missions_models
    aletheus_runtime_governance --> aletheus_runtime_governance_governance_core
    aletheus_runtime_governance --> aletheus_runtime_governance_principle_x
    aletheus_runtime_handlers --> aletheus_runtime_handlers_compatibility_handlers
    aletheus_runtime_handlers_compatibility_handlers --> aletheus_runtime_context
    aletheus_runtime_handlers_event_handlers --> aletheus_runtime_context
    aletheus_runtime_handlers_graph_handlers --> aletheus_runtime_context
    aletheus_runtime_handlers_mission_handlers --> aletheus_runtime_context
    aletheus_runtime_health --> aletheus_runtime_health_monitor
    aletheus_runtime_inspector --> aletheus_runtime_inspector_runtime_inspector
    aletheus_runtime_integrity --> aletheus_runtime_integrity_boot_validator
    aletheus_runtime_integrity --> aletheus_runtime_integrity_doctor
    aletheus_runtime_integrity --> aletheus_runtime_integrity_invariants
    aletheus_runtime_kernel --> aletheus_runtime_kernel_dispatcher
    aletheus_runtime_kernel --> aletheus_runtime_kernel_executor
    aletheus_runtime_kernel --> aletheus_runtime_kernel_kernel
    aletheus_runtime_kernel --> aletheus_runtime_kernel_orchestrator
    aletheus_runtime_kernel --> aletheus_runtime_kernel_scheduler
    aletheus_runtime_kernel --> aletheus_runtime_kernel_supervisor
    aletheus_runtime_lifecycle --> aletheus_runtime_lifecycle_event_bus
    aletheus_runtime_lifecycle --> aletheus_runtime_lifecycle_events
    aletheus_runtime_lifecycle --> aletheus_runtime_lifecycle_manager
    aletheus_runtime_lifecycle --> aletheus_runtime_lifecycle_state
    aletheus_runtime_lifecycle_event_bus --> aletheus_runtime_lifecycle_events
    aletheus_runtime_lifecycle_manager --> aletheus_runtime_lifecycle_state
    aletheus_runtime_managers --> aletheus_runtime_managers_certification_manager
    aletheus_runtime_managers --> aletheus_runtime_managers_command_manager
    aletheus_runtime_managers --> aletheus_runtime_managers_governance_manager
    aletheus_runtime_managers --> aletheus_runtime_managers_health_manager
    aletheus_runtime_managers --> aletheus_runtime_managers_invariant_manager
    aletheus_runtime_managers --> aletheus_runtime_managers_registration_manager
    aletheus_runtime_managers --> aletheus_runtime_managers_registry_manager
    aletheus_runtime_managers --> aletheus_runtime_managers_snapshot_manager
    aletheus_runtime_managers --> aletheus_runtime_managers_validation_manager
    aletheus_runtime_managers_command_manager --> aletheus_runtime_command_bootstrap_bootstrapper
    aletheus_runtime_managers_health_manager --> aletheus_runtime_lifecycle_resolver
    aletheus_runtime_managers_registration_manager --> aletheus_runtime_command_bootstrap_bootstrapper
    aletheus_runtime_managers_registry_federation_manager --> aletheus_runtime_services_registry_federation_bootstrap
    aletheus_runtime_migration --> aletheus_runtime_migration_reporter
    aletheus_runtime_migration --> aletheus_runtime_migration_tracker
    aletheus_runtime_migration_tracker --> aletheus_runtime_migration_models
    aletheus_runtime_modules --> aletheus_runtime_services_service_registry
    aletheus_runtime_orchestration --> aletheus_runtime_orchestration_orchestrator
    aletheus_runtime_pipeline --> aletheus_runtime_context
    aletheus_runtime_policy --> aletheus_runtime_policy_engine
    aletheus_runtime_providers --> aletheus_runtime_providers_service_provider
    aletheus_runtime_recovery --> aletheus_runtime_recovery_manager
    aletheus_runtime_registration --> aletheus_runtime_registration_manager
    aletheus_runtime_registration --> aletheus_runtime_registration_reporter
    aletheus_runtime_registration_manager --> aletheus_runtime_registration_models
    aletheus_runtime_registrations --> aletheus_runtime_registrations_agent_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_application_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_copilot_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_decision_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_executive_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_graph_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_memory_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_mission_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_planning_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_reasoning_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_runtime_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_semantic_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_uil_commands
    aletheus_runtime_registrations --> aletheus_runtime_registrations_workspace_commands
    aletheus_runtime_registrations_agent_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_copilot_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_decision_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_enterprise_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_federation_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_ha_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_kernel_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_knowledge_graph_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_learning_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_memory_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_memory_mesh_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_plugin_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_prediction_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_reasoning_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_security_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_state_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_telemetry_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_tenancy_commands --> aletheus_runtime_domains
    aletheus_runtime_registrations_workflow_commands --> aletheus_runtime_domains
    aletheus_runtime_registries --> aletheus_runtime_context
    aletheus_runtime_registry --> aletheus_runtime_registry_runtime_registry
    aletheus_runtime_relay --> aletheus_runtime_relay_models
    aletheus_runtime_relay --> aletheus_runtime_relay_network
    aletheus_runtime_relay --> aletheus_runtime_relay_reporter
    aletheus_runtime_relay_network --> aletheus_runtime_relay_models
    aletheus_runtime_service_mesh --> aletheus_runtime_service_mesh_mesh
    aletheus_runtime_service_mesh --> aletheus_runtime_service_mesh_models
    aletheus_runtime_service_mesh --> aletheus_runtime_service_mesh_reporter
    aletheus_runtime_service_mesh_mesh --> aletheus_runtime_service_mesh_models
    aletheus_runtime_services --> aletheus_runtime_services_service_registry
    aletheus_runtime_services_registry_federation_bootstrap --> aletheus_runtime_services_registry_federation_registration
    aletheus_runtime_services_registry_federation_registration --> aletheus_runtime_services_registry_federation_service
    aletheus_runtime_spa --> aletheus_runtime_spa_anchor_analysis
    aletheus_runtime_universal --> aletheus_runtime_universal_engine
    aletheus_runtime_universal_engine --> aletheus_runtime_universal_application_binding
    aletheus_runtime_universal_engine --> aletheus_runtime_universal_capability_registry
    aletheus_runtime_universal_engine --> aletheus_runtime_universal_runtime_topology
    aletheus_runtime_workflow --> aletheus_runtime_context
```

## Summary

- Modules: 417
- Internal dependency edges: 437
- Dependency cycles: 0
