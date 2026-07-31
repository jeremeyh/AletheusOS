# Runtime Architecture Audit

Generated: `2026-07-31T08:05:18.418712+00:00`

## Architecture Health

- Score: **85/100**
- Grade: **B+**
- Errors: **0**
- Warnings: **8**
- Informational findings: **1**

### Score Deductions

- Syntax Errors: -0
- Dependency Cycles: -0
- Legacy References: -0
- Ownership Errors: -0
- Other Errors: -0
- Warnings: -15

## Runtime Module Inventory

- Modules: **417**
- Total lines: **26884**
- Average module size: **64.47 lines**
- Largest module: **aletheus.runtime.core** (1027 lines)
- Internal import edges: **440**
- Dependency cycles: **0**
- Orphan modules: **32**
- Kernel constructors: **1**
- Boot pipeline paths: **2**
- Legacy references: **0**

## Runtime Package Tree

```text
runtime
├── adapters
│   ├── __init__.py
│   ├── compatibility_adapter.py
│   ├── event_adapter.py
│   ├── graph_adapter.py
│   ├── mission_adapter.py
│   ├── prediction_adapter.py
│   ├── runtime_adapter.py
│   ├── topology_registry_adapter.py
│   └── universal_intelligence_adapter.py
├── anchors
│   ├── __init__.py
│   ├── analytics.py
│   ├── application.py
│   ├── architecture_council.py
│   ├── architecture_discovery.py
│   ├── architecture_evolution.py
│   ├── architecture_experiment.py
│   ├── architecture_hypothesis.py
│   ├── architecture_innovation.py
│   ├── architecture_intelligence.py
│   ├── architecture_optimization.py
│   ├── architecture_proof.py
│   ├── architecture_research.py
│   ├── architecture_selection.py
│   ├── architecture_simulator.py
│   ├── architecture_steward.py
│   ├── architecture_synthesis.py
│   ├── autonomous_architect.py
│   ├── autonomous_validation.py
│   ├── base.py
│   ├── cognitive_adaptation.py
│   ├── cognitive_architect.py
│   ├── cognitive_architecture.py
│   ├── cognitive_conflict.py
│   ├── cognitive_consolidation.py
│   ├── cognitive_creativity.py
│   ├── cognitive_dependency_graph.py
│   ├── cognitive_forecasting.py
│   ├── cognitive_governance.py
│   ├── cognitive_learning.py
│   ├── cognitive_memory_optimizer.py
│   ├── cognitive_metrics.py
│   ├── cognitive_monitoring.py
│   ├── cognitive_optimization.py
│   ├── cognitive_pattern_mining.py
│   ├── cognitive_planning.py
│   ├── cognitive_registry.py
│   ├── cognitive_resources.py
│   ├── cognitive_rollback.py
│   ├── cognitive_selection.py
│   ├── cognitive_self_improvement.py
│   ├── cognitive_simulation.py
│   ├── cognitive_strategy.py
│   ├── cognitive_transfer.py
│   ├── cognitive_verification.py
│   ├── consensus_memory.py
│   ├── constitution.py
│   ├── constitutional_intelligence.py
│   ├── constitutional_reasoning.py
│   ├── continuity.py
│   ├── contracts.py
│   ├── decision_intelligence.py
│   ├── dependency.py
│   ├── deployment_governor.py
│   ├── discovery.py
│   ├── emergent_detection.py
│   ├── ethical_alignment.py
│   ├── evolution_certification.py
│   ├── evolution_graph.py
│   ├── execution.py
│   ├── genesis_transition.py
│   ├── governance.py
│   ├── governance_intelligence.py
│   ├── healing.py
│   ├── improvement_loop.py
│   ├── institutional_memory.py
│   ├── intelligence.py
│   ├── intelligence_boundary.py
│   ├── intelligence_continuity.py
│   ├── judgment_optimization.py
│   ├── judgment_refinement.py
│   ├── knowledge.py
│   ├── learning.py
│   ├── lifecycle.py
│   ├── long_term_planning.py
│   ├── memory.py
│   ├── meta_reasoning.py
│   ├── migration.py
│   ├── negotiation.py
│   ├── optimization.py
│   ├── pattern_forecasting.py
│   ├── pattern_intelligence.py
│   ├── performance.py
│   ├── portfolio.py
│   ├── predictive.py
│   ├── proposals.py
│   ├── purpose_alignment.py
│   ├── registry.py
│   ├── research.py
│   ├── resource_allocation.py
│   ├── self_identity.py
│   ├── simulation.py
│   ├── strategic_intelligence.py
│   ├── strategic_planning.py
│   ├── verification.py
│   └── wisdom_accumulation.py
├── applications
│   ├── __init__.py
│   └── application_runtime.py
├── architecture
│   ├── __init__.py
│   └── validator.py
├── audit
│   ├── command_surface.py
│   └── registry_snapshot.py
├── boot
│   └── __init__.py
├── boot_director
│   ├── __init__.py
│   ├── director.py
│   └── reporter.py
├── boot_phases
│   ├── service_groups
│   │   ├── __init__.py
│   │   ├── ai_platform.py
│   │   ├── core.py
│   │   ├── foundation.py
│   │   └── intelligence.py
│   ├── __init__.py
│   ├── agent_boot.py
│   ├── application_boot.py
│   ├── command_bootstrap.py
│   ├── memory_initialization.py
│   ├── runtime_state.py
│   ├── scheduler.py
│   └── service_registration.py
├── boot_pipeline
│   ├── __init__.py
│   ├── conditions.py
│   ├── context.py
│   ├── default_pipeline.py
│   ├── dependencies.py
│   ├── executor.py
│   ├── manifest.py
│   ├── models.py
│   ├── pipeline.py
│   ├── report.py
│   ├── reporter.py
│   └── timing.py
├── bootstrap
│   ├── __init__.py
│   ├── bootstrap_engine.py
│   ├── runtime_bootstrap.py
│   └── runtime_manifest_builder.py
├── builder
│   ├── __init__.py
│   └── builder.py
├── capabilities
│   ├── __init__.py
│   ├── registry.py
│   └── synchronizer.py
├── catalyst
│   ├── __init__.py
│   ├── models.py
│   ├── optimizer.py
│   └── reporter.py
├── certification
│   ├── boot_certification.py
│   ├── certifier.py
│   └── federation_certifier.py
├── circuits
│   ├── __init__.py
│   ├── manager.py
│   ├── models.py
│   └── reporter.py
├── command_bootstrap
│   ├── __init__.py
│   └── bootstrapper.py
├── command_handlers
│   └── __init__.py
├── commands
│   ├── tests
│   │   ├── test_compiled_registry_dispatcher.py
│   │   └── test_dispatcher.py
│   ├── __init__.py
│   ├── command_bus.py
│   ├── contracts.py
│   ├── dispatcher.py
│   ├── errors.py
│   ├── middleware.py
│   ├── models.py
│   ├── pyproject.toml
│   ├── README.md
│   ├── registry.py
│   └── runtime_commands.py
├── commands_v2
│   ├── __init__.py
│   ├── dispatcher.py
│   ├── models.py
│   ├── registry.py
│   └── reporter.py
├── compat
│   ├── __init__.py
│   ├── contracts.py
│   ├── registry.py
│   └── resolver.py
├── compatibility_layer
│   ├── __init__.py
│   └── layer.py
├── composition
│   ├── __init__.py
│   ├── models.py
│   ├── reporter.py
│   └── root.py
├── compression
│   ├── __init__.py
│   ├── dashboard.py
│   ├── models.py
│   └── reporter.py
├── container
│   ├── __init__.py
│   └── container.py
├── contracts
│   ├── components
│   │   ├── __init__.py
│   │   └── base.py
│   ├── managers
│   │   ├── __init__.py
│   │   └── registration_manager.py
│   ├── __init__.py
│   ├── component.py
│   ├── errors.py
│   ├── health.py
│   ├── lifecycle.py
│   ├── lifecycle_manager.py
│   ├── manifest.py
│   └── registration.py
├── convergence
│   ├── __init__.py
│   ├── application_registry.py
│   ├── capability_topology.py
│   ├── engine.py
│   ├── genesis_registry.py
│   └── health_matrix.py
├── council
│   └── council.py
├── dashboard
│   ├── __init__.py
│   └── dashboard.py
├── decomposition
│   ├── __init__.py
│   ├── analyzer.py
│   ├── models.py
│   ├── planner.py
│   ├── reporter.py
│   └── responsibility.py
├── discovery
│   ├── __init__.py
│   └── discovery.py
├── domains
│   ├── __init__.py
│   ├── agent.py
│   ├── application.py
│   ├── cluster.py
│   ├── copilot.py
│   ├── decision.py
│   ├── enterprise.py
│   ├── event_bus.py
│   ├── executive.py
│   ├── federation.py
│   ├── high_availability.py
│   ├── kernel.py
│   ├── knowledge_graph.py
│   ├── learning.py
│   ├── memory.py
│   ├── memory_mesh.py
│   ├── mission.py
│   ├── persistence.py
│   ├── planning.py
│   ├── plugin.py
│   ├── prediction.py
│   ├── reasoning.py
│   ├── runtime.py
│   ├── security.py
│   ├── semantic.py
│   ├── state.py
│   ├── telemetry.py
│   ├── tenancy.py
│   └── workflow.py
├── executive
│   ├── __init__.py
│   ├── kernel.py
│   ├── models.py
│   └── reporter.py
├── extraction
│   ├── __init__.py
│   ├── models.py
│   ├── planner.py
│   └── reporter.py
├── extraction_missions
│   ├── __init__.py
│   ├── manager.py
│   ├── models.py
│   └── reporter.py
├── governance
│   ├── __init__.py
│   ├── architecture_rules.py
│   ├── governance_core.py
│   ├── history.py
│   ├── principle_x.py
│   └── registry_rules.py
├── handlers
│   ├── __init__.py
│   ├── compatibility_handlers.py
│   ├── event_handlers.py
│   ├── graph_handlers.py
│   └── mission_handlers.py
├── health
│   ├── __init__.py
│   └── monitor.py
├── inspector
│   ├── __init__.py
│   └── runtime_inspector.py
├── integrity
│   ├── __init__.py
│   ├── boot_validator.py
│   ├── doctor.py
│   └── invariants.py
├── intelligence
│   └── spa_bridge.py
├── kernel
│   ├── __init__.py
│   ├── dispatcher.py
│   ├── executor.py
│   ├── kernel.py
│   ├── orchestrator.py
│   ├── scheduler.py
│   └── supervisor.py
├── lifecycle
│   ├── __init__.py
│   ├── event_bus.py
│   ├── events.py
│   ├── manager.py
│   ├── models.py
│   ├── reporter.py
│   ├── resolver.py
│   └── state.py
├── managers
│   ├── __init__.py
│   ├── certification_manager.py
│   ├── command_manager.py
│   ├── governance_manager.py
│   ├── health_manager.py
│   ├── invariant_manager.py
│   ├── lifecycle_manager.py
│   ├── observability_manager.py
│   ├── registration_manager.py
│   ├── registry_federation_manager.py
│   ├── registry_manager.py
│   ├── runtime_facade.py
│   ├── runtime_inspector.py
│   ├── snapshot_manager.py
│   └── validation_manager.py
├── manifest
│   └── __init__.py
├── manifests
│   └── runtime_composition_manifest.yaml
├── migration
│   ├── __init__.py
│   ├── models.py
│   ├── reporter.py
│   └── tracker.py
├── orchestration
│   ├── __init__.py
│   └── orchestrator.py
├── patches
│   └── core
│       └── goal_list_fix.py
├── policy
│   ├── __init__.py
│   └── engine.py
├── providers
│   ├── __init__.py
│   └── service_provider.py
├── readiness
│   ├── federation_readiness_check.py
│   └── snapshot.py
├── recovery
│   ├── __init__.py
│   └── manager.py
├── registration
│   ├── __init__.py
│   ├── manager.py
│   ├── models.py
│   └── reporter.py
├── registrations
│   ├── __init__.py
│   ├── agent_commands.py
│   ├── application_commands.py
│   ├── architecture_commands.py
│   ├── cluster_commands.py
│   ├── compatibility_alias_commands.py
│   ├── compatibility_commands.py
│   ├── copilot_commands.py
│   ├── decision_commands.py
│   ├── enterprise_commands.py
│   ├── event_commands.py
│   ├── executive_commands.py
│   ├── federation_commands.py
│   ├── governance_architecture_commands.py
│   ├── governance_commands.py
│   ├── graph_commands.py
│   ├── ha_commands.py
│   ├── kernel_commands.py
│   ├── kernel_compatibility_commands.py
│   ├── knowledge_graph_commands.py
│   ├── learning_commands.py
│   ├── memory_commands.py
│   ├── memory_mesh_commands.py
│   ├── mission_commands.py
│   ├── mission_v2_commands.py
│   ├── planning_commands.py
│   ├── plugin_commands.py
│   ├── prediction_commands.py
│   ├── reasoning_commands.py
│   ├── registry_commands.py
│   ├── release_commands.py
│   ├── runtime_commands.py
│   ├── security_commands.py
│   ├── semantic_commands.py
│   ├── state_commands.py
│   ├── telemetry_commands.py
│   ├── tenancy_commands.py
│   ├── uil_commands.py
│   ├── workflow_commands.py
│   ├── workflow_v2_commands.py
│   └── workspace_commands.py
├── registry
│   ├── __init__.py
│   ├── compatibility.py
│   └── runtime_registry.py
├── relay
│   ├── __init__.py
│   ├── models.py
│   ├── network.py
│   └── reporter.py
├── release
│   ├── genesis6_report.py
│   ├── genesis6_review.py
│   ├── genesis6_validator.py
│   └── manifest.py
├── service_mesh
│   ├── __init__.py
│   ├── mesh.py
│   ├── models.py
│   └── reporter.py
├── services
│   ├── __init__.py
│   ├── registry_federation_bootstrap.py
│   ├── registry_federation_registration.py
│   ├── registry_federation_service.py
│   └── service_registry.py
├── spa
│   ├── __init__.py
│   └── anchor_analysis.py
├── universal
│   ├── __init__.py
│   ├── application_binding.py
│   ├── capability_registry.py
│   ├── engine.py
│   └── runtime_topology.py
├── __init__.py
├── adapter.py
├── context.py
├── core.py
├── diagnostics.py
├── events.py
├── hardening.py
├── job_queue.py
├── metrics.py
├── modules.py
├── pipeline.py
├── README.md
├── registries.py
├── scheduler.py
└── workflow.py
```

## RuntimeKernel Construction

- `aletheus/runtime/composition/root.py:48` — `RuntimeKernel`

## Boot Pipeline Construction

- `aletheus/runtime/composition/root.py:50` — `build_runtime_boot_pipeline`
- `aletheus/runtime/core.py:282` — `build_runtime_boot_pipeline`

## Legacy Runtime References

- None discovered.

## Dependency Cycles

- No dependency cycles discovered.

## Orphan Modules

- `aletheus.runtime.adapter`
- `aletheus.runtime.adapters`
- `aletheus.runtime.adapters.topology_registry_adapter`
- `aletheus.runtime.audit.registry_snapshot`
- `aletheus.runtime.boot`
- `aletheus.runtime.boot_pipeline.dependencies`
- `aletheus.runtime.boot_pipeline.executor`
- `aletheus.runtime.boot_pipeline.manifest`
- `aletheus.runtime.boot_pipeline.models`
- `aletheus.runtime.boot_pipeline.reporter`
- `aletheus.runtime.certification.certifier`
- `aletheus.runtime.certification.federation_certifier`
- `aletheus.runtime.command_handlers`
- `aletheus.runtime.composition.models`
- `aletheus.runtime.composition.reporter`
- `aletheus.runtime.contracts`
- `aletheus.runtime.contracts.components`
- `aletheus.runtime.contracts.managers`
- `aletheus.runtime.council.council`
- `aletheus.runtime.domains.application`
- `aletheus.runtime.domains.executive`
- `aletheus.runtime.domains.semantic`
- `aletheus.runtime.domains.state`
- `aletheus.runtime.lifecycle.models`
- `aletheus.runtime.lifecycle.reporter`
- `aletheus.runtime.managers.lifecycle_manager`
- `aletheus.runtime.managers.observability_manager`
- `aletheus.runtime.managers.runtime_inspector`
- `aletheus.runtime.manifest`
- `aletheus.runtime.patches.core.goal_list_fix`
- `aletheus.runtime.readiness.federation_readiness_check`
- `aletheus.runtime.release.manifest`

## Findings

- **WARNING** `boot_pipeline`: Multiple runtime boot-pipeline paths remain active (2).
- **WARNING** `empty_module`: Python module is empty. — `aletheus/runtime/boot/__init__.py`
- **WARNING** `empty_module`: Python module is empty. — `aletheus/runtime/command_handlers/__init__.py`
- **WARNING** `empty_module`: Python module is empty. — `aletheus/runtime/contracts/__init__.py`
- **WARNING** `empty_module`: Python module is empty. — `aletheus/runtime/contracts/components/__init__.py`
- **WARNING** `empty_module`: Python module is empty. — `aletheus/runtime/contracts/managers/__init__.py`
- **WARNING** `empty_module`: Python module is empty. — `aletheus/runtime/manifest/__init__.py`
- **WARNING** `module_size`: Module contains 1027 lines and exceeds the recommended threshold of 750. — `aletheus/runtime/core.py`
- **INFO** `orphan_modules`: 32 runtime modules have no internal inbound or outbound imports.
