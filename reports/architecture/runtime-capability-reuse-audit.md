# AletheusOS Runtime Capability Reuse Audit

Purpose: identify existing implementations before approving new builds.

## startup_boot

- All candidates: **2104**
- High-signal candidates: **40**

| Score | Path | Matched terms |
|---:|---|---|
| 19 | `aletheus/span/bootstrap.py` | boot, bootstrap, initialization, initialize, lifecycle, start, startup |
| 19 | `reports/span/backups/bootstrap_v2_20260719T115601Z/bootstrap.py` | boot, bootstrap, initialization, initialize, lifecycle, start, startup |
| 19 | `reports/span/backups/bootstrap_v2_20260719T120944Z/bootstrap.py` | boot, bootstrap, initialization, initialize, lifecycle, start, startup |
| 17 | `aletheus/runtime/services/registry_federation_bootstrap.py` | boot, bootstrap, initialize, start, startup |
| 16 | `aletheus/runtime_platform/bootstrap/lifecycle.py` | boot, bootstrap, lifecycle |
| 15 | `aletheus/genesis_engine/bootstrap/engine.py` | boot, bootstrap, initialize |
| 14 | `Genesis-012B-SPAN-Runtime-Integration/files/tests/strategic/runtime/test_runtime_bootstrap.py` | boot, bootstrap, initialize, start |
| 14 | `aletheus/runtime/bootstrap/runtime_bootstrap.py` | boot, bootstrap, start, startup |
| 14 | `core/startup.py` | boot, bootstrap, start, startup |
| 14 | `tests/strategic/runtime/test_runtime_bootstrap.py` | boot, bootstrap, initialize, start |
| 13 | `aletheus/institutional_civilization/bootstrap.py` | boot, bootstrap, readiness |
| 13 | `aletheus/runtime_platform/bootstrap/boot_manager.py` | boot, bootstrap, lifecycle |
| 13 | `core/bootstrap.py` | boot, bootstrap, initialize |
| 12 | `Genesis10_Work_Organization/04_reports/genesis_8_command_dispatch/guarded_registration_backup_20260710_044725/bootstrapper.py` | boot, bootstrap |
| 12 | `Genesis10_Work_Organization/04_reports/genesis_8_command_dispatch/prediction_adapter_backup_20260710_050230/core.py` | boot, bootstrap, initialization, initialize, lifecycle, readiness |
| 12 | `Genesis10_Work_Organization/04_reports/genesis_8_command_dispatch/registration_catalog_backup_20260710_044531/bootstrapper.py` | boot, bootstrap |
| 12 | `Genesis10_Work_Organization/04_reports/genesis_8_command_dispatch/safe_alias_backup_20260710_045355/bootstrapper.py` | boot, bootstrap |
| 12 | `aletheus/atlas/bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/capability_graph/bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/concept_collision_engine/bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/executive_kernel/bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/genesis/bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/intent_registry/bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/neural/envelope/bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/oracle/bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/platform_lifecycle/core.py` | boot, lifecycle, start |
| 12 | `aletheus/platform_verification/bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/repository_dna/audit_bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/runtime/boot_phases/command_bootstrap.py` | boot, bootstrap |
| 12 | `aletheus/runtime/bootstrap/bootstrap_engine.py` | boot, bootstrap |
| 12 | `aletheus/runtime/command_bootstrap/bootstrapper.py` | boot, bootstrap |
| 12 | `aletheus/runtime/core.py` | boot, bootstrap, initialization, initialize, lifecycle, readiness |
| 12 | `aletheus/runtime/lifecycle/manager.py` | boot, initialize, lifecycle |
| 12 | `aletheus/runtime/managers/lifecycle_manager.py` | boot, initialize, lifecycle |
| 12 | `aletheus/watch_tower/bootstrap.py` | boot, bootstrap |
| 12 | `components/chds/core/bootstrap.py` | boot, bootstrap |
| 12 | `reports/genesis_8_command_dispatch/guarded_registration_backup_20260710_044725/bootstrapper.py` | boot, bootstrap |
| 12 | `reports/genesis_8_command_dispatch/prediction_adapter_backup_20260710_050230/core.py` | boot, bootstrap, initialization, initialize, lifecycle, readiness |
| 12 | `reports/genesis_8_command_dispatch/registration_catalog_backup_20260710_044531/bootstrapper.py` | boot, bootstrap |
| 12 | `reports/genesis_8_command_dispatch/safe_alias_backup_20260710_045355/bootstrapper.py` | boot, bootstrap |

## runtime_health

- All candidates: **832**
- High-signal candidates: **40**

| Score | Path | Matched terms |
|---:|---|---|
| 12 | `tests/platform_intelligence/constitutional_runtime_supervisor/test_crs.py` | degraded, health, supervisor |
| 10 | `aletheus/institutional_civilization/readiness.py` | degraded, health, readiness |
| 10 | `aletheus/platform_intelligence/constitutional_runtime_supervisor/models.py` | degraded, health, supervisor |
| 10 | `aletheus/platform_intelligence/constitutional_runtime_supervisor/supervisor.py` | degraded, health, supervisor |
| 10 | `aletheus/runtime_supervisor/core.py` | degraded, health, supervisor |
| 10 | `aletheus/runtime_supervisor/health.py` | health, supervisor |
| 9 | `aletheus/runtime/managers/runtime_facade.py` | diagnostic, health, readiness |
| 9 | `backups/runtime/core_v4.6.2_stable.py` | diagnostic, health, supervisor |
| 9 | `migrations/genesis6/core_v481_registration_cutover.py` | diagnostic, health, supervisor |
| 8 | `archive/quarantine/empty_python_modules/20260710T120028Z/aletheus/autonomic/health.py` | autonomic, health |
| 7 | `aletheus/atlas/health.py` | degraded, health |
| 7 | `aletheus/cognitive_kernel/health.py` | diagnostic, health |
| 7 | `aletheus/foundation/capability/health.py` | diagnostic, health |
| 7 | `aletheus/foundation_readiness/core.py` | health, readiness |
| 7 | `aletheus/platform_intelligence/intelligence_engine/health.py` | degraded, health |
| 7 | `aletheus/runtime/contracts/health.py` | degraded, health |
| 7 | `aletheus/runtime/diagnostics.py` | diagnostic, health |
| 7 | `aletheus/runtime/kernel/supervisor.py` | health, supervisor |
| 7 | `aletheus/runtime_registry_v2/health.py` | degraded, health |
| 7 | `aletheus/runtime_supervisor/policies.py` | degraded, supervisor |
| 7 | `aletheus/span/bootstrap.py` | degraded, diagnostic, health |
| 7 | `aletheusos_kernel_sprint1/src/aletheus/core/health.py` | degraded, health |
| 7 | `reports/span/backups/bootstrap_v2_20260719T115601Z/bootstrap.py` | degraded, diagnostic, health |
| 7 | `reports/span/backups/bootstrap_v2_20260719T120944Z/bootstrap.py` | degraded, diagnostic, health |
| 7 | `tests/platform_intelligence/constitutional_policy_engine/test_cpe.py` | degraded, health, supervisor |
| 7 | `tests/platform_intelligence/constitutional_runtime_executive/test_crx.py` | degraded, health, supervisor |
| 7 | `tools/repository/audit_runtime_capabilities.py` | autonomic, degraded, diagnostic, health, liveness, readiness, supervisor |
| 6 | `Genesis10_Work_Organization/04_reports/genesis_8_command_dispatch/prediction_adapter_backup_20260710_050230/core.py` | diagnostic, health, readiness, supervisor |
| 6 | `aletheus/aos_search/health.py` | health |
| 6 | `aletheus/autonomy/health/engine.py` | health |
| 6 | `aletheus/canonical_identity/health.py` | health |
| 6 | `aletheus/capability_engine/health.py` | health |
| 6 | `aletheus/collectible_portfolio/health.py` | health |
| 6 | `aletheus/consensus_engine/health.py` | health |
| 6 | `aletheus/constitutional_graph/health.py` | health |
| 6 | `aletheus/constitutional_ledger/health.py` | health |
| 6 | `aletheus/constitutional_library/health.py` | health |
| 6 | `aletheus/constitutional_memory/health.py` | health |
| 6 | `aletheus/constitutional_policy/health.py` | health |
| 6 | `aletheus/contracts/platform_contract.py` | diagnostic, health |

## dependency_topology

- All candidates: **652**
- High-signal candidates: **40**

| Score | Path | Matched terms |
|---:|---|---|
| 22 | `aletheus/runtime_platform/topology/dependency_graph.py` | cycle, dependencies, dependency, graph, topology |
| 16 | `aletheus/self_assembly/dependency_graph.py` | cycle, dependencies, dependency, graph |
| 16 | `tests/platform_intelligence/constitutional_graph/test_constitutional_graph.py` | cycle, dependencies, dependency, graph, topology |
| 14 | `aletheus/constitutional_time/graph.py` | cycle, dag, dependencies, dependency, graph |
| 13 | `aletheus/atlas/architecture_graph.py` | atlas, dependencies, dependency, graph, topology |
| 13 | `aletheus/platform_intelligence/constitutional_dependency_manager/manager.py` | cycle, dependencies, dependency, graph |
| 13 | `aletheus/platform_intelligence/constitutional_graph/graph.py` | cycle, dependencies, graph, topology |
| 13 | `aletheus/runtime/anchors/cognitive_dependency_graph.py` | dependencies, dependency, graph |
| 13 | `aletheus/spectrum_platform_analyzer/circular_dependencies.py` | cycle, dependencies, dependency, graph |
| 12 | `aletheus/atlas/models.py` | atlas, graph, topology |
| 12 | `aletheus/module_registry/dependency_graph.py` | dependency, graph |
| 12 | `aletheus/runtime/anchors/dependency.py` | dependencies, dependency, graph |
| 12 | `aletheus/span/graph.py` | cycle, dependency, graph |
| 12 | `architecture/dependency_graph.py` | dependency, graph |
| 11 | `aletheus/atlas/dependency_engine.py` | atlas, dependency, graph |
| 11 | `aletheus/atlas/topology.py` | atlas, graph, topology |
| 11 | `tests/platform_intelligence/constitutional_dependency_manager/test_cdm.py` | cycle, dependencies, dependency, graph |
| 10 | `Genesis10_Work_Organization/04_reports/genesis_8_command_dispatch/prediction_adapter_backup_20260710_050230/core.py` | cycle, dependencies, dependency, graph |
| 10 | `aletheus/orchestrator/component_graph.py` | dependencies, dependency, graph |
| 10 | `aletheus/platform_intelligence/constitutional_dependency_manager/exceptions.py` | cycle, dependency, graph |
| 10 | `aletheus/runtime/core.py` | cycle, dependencies, dependency, graph |
| 10 | `reports/genesis_8_command_dispatch/prediction_adapter_backup_20260710_050230/core.py` | cycle, dependencies, dependency, graph |
| 10 | `tests/constitutional_time/test_time_engine.py` | cycle, dependencies, dependency, graph |
| 9 | `aletheus/atlas/repository_dna_adapter.py` | atlas, graph |
| 9 | `aletheus/atlas/repository_dna_service.py` | atlas, graph |
| 9 | `aletheus/atlas/service.py` | atlas, graph |
| 9 | `aletheus/capability_graph/graph.py` | dependencies, graph |
| 9 | `aletheus/mastery/graph/engine.py` | dependency, graph |
| 9 | `aletheus/platform_intelligence/constitutional_graph/exceptions.py` | cycle, graph |
| 9 | `aletheus/platform_intelligence/runtime_explorer/explorer.py` | cycle, dependencies, graph |
| 9 | `aletheus/runtime_platform/topology/topology_registry.py` | dependencies, dependency, graph, topology |
| 9 | `aletheus/span/analyzers/dependency.py` | cycle, dependencies, dependency, graph |
| 9 | `aletheus/spectrum_platform_analyzer/dependency.py` | dependency, graph |
| 8 | `aletheus/atlas/analyzer.py` | atlas, graph, topology |
| 8 | `aletheus/platform_intelligence/constitutional_dependency_manager/models.py` | cycle, dependencies, dependency |
| 8 | `aletheus/platform_intelligence/constitutional_graph/statistics.py` | cycle, graph, topology |
| 8 | `aletheus/platform_intelligence/constitutional_runtime_kernel/kernel.py` | cycle, dependency, graph, topology |
| 8 | `aletheus/self_assembly/dependency_resolver.py` | cycle, dependency, graph |
| 8 | `archive/quarantine/empty_python_modules/20260710T120028Z/aletheus/service_fabric/dependency_graph.py` | dependency, graph |
| 8 | `tests/platform_intelligence/constitutional_runtime_kernel/test_dependency_plan_integration.py` | cycle, dependencies, dependency |

## capability_registration

- All candidates: **1345**
- High-signal candidates: **40**

| Score | Path | Matched terms |
|---:|---|---|
| 18 | `aletheus/runtime_platform/topology/topology_registry.py` | capability, provider, register, registration, registry |
| 15 | `aletheus/capability_engine/registry.py` | capability, register, registry |
| 15 | `aletheus/capability_manifest/registry.py` | capability, register, registry |
| 15 | `aletheus/intelligence_fabric/capability_registry.py` | capability, register, registry |
| 15 | `aletheus/runtime/universal/capability_registry.py` | capability, register, registry |
| 15 | `aletheus/runtime_platform/providers/provider_registry.py` | provider, register, registry |
| 15 | `aletheus/span/provider_registry.py` | provider, register, registry |
| 15 | `capability_engine/registry.py` | capability, register, registry |
| 15 | `card_hawk/runtime/capability_registry.py` | capability, register, registry |
| 15 | `core/provider_registry.py` | provider, register, registry |
| 15 | `registry/provider_registry.py` | provider, register, registry |
| 15 | `tests/nimble/test_deployment_provider_registry.py` | provider, register, registry |
| 15 | `tests/test_runtime_service_registry.py` | register, registry, service registry |
| 14 | `aletheus/platform_intelligence/service_registry/registry.py` | register, registration, registry, service registry |
| 14 | `aletheus/runtime/services/registry_federation_registration.py` | capability, register, registration, registry |
| 14 | `aletheus/span/providers/registry.py` | capability, provider, register, registry |
| 14 | `tests/platform_intelligence/service_registry/test_service_registry.py` | register, registration, registry, service registry |
| 13 | `aletheus/engine_registry/registry.py` | engine registry, register, registry |
| 13 | `aletheus/experience_gateway/providers/default_registry.py` | provider, register, registry |
| 13 | `aletheus/platform/service_registry.py` | register, registry, service registry |
| 13 | `aletheus/platform_intelligence/service_registry/exceptions.py` | register, registry, service registry |
| 13 | `aletheus/runtime/registrations/registry_commands.py` | register, registration, registry |
| 13 | `aletheus/runtime/services/service_registry.py` | register, registry, service registry |
| 13 | `card_hawk/intelligence/core/capability_registry.py` | capability, register, registry |
| 13 | `card_hawk/runtime/registration.py` | capability, register, registration, registry |
| 13 | `cardhawkos/runtime/service_registry.py` | register, registry, service registry |
| 13 | `core/engine_registry.py` | engine registry, register, registry |
| 13 | `core/service_registry.py` | register, registry, service registry |
| 13 | `registry/engine_registry.py` | engine registry, register, registry |
| 13 | `tests/nimble/test_provider_capability_governance.py` | capability, provider, registry |
| 12 | `aletheus/aos_search/providers.py` | provider, register, registry |
| 12 | `aletheus/experience_gateway/providers/contracts.py` | provider, register, registry |
| 12 | `aletheus/intelligence_gateway/registry.py` | capability, register, registry |
| 12 | `aletheus/runtime/anchors/cognitive_registry.py` | capability, register, registry |
| 12 | `aletheus/runtime/capabilities/registry.py` | capability, register, registry |
| 12 | `aletheus/runtime/commands/tests/test_compiled_registry_dispatcher.py` | register, registration, registry |
| 12 | `core/registry.py` | provider, register, registry |
| 11 | `aletheus/foundation_service_bus/registry.py` | capability, register, registry, service registry |
| 11 | `aletheus/platform_intelligence/service_registry/models.py` | register, registry, service registry |
| 11 | `aletheus/runtime_registry_v2/core.py` | capability, register, registration, registry |

## configuration_validation

- All candidates: **222**
- High-signal candidates: **23**

| Score | Path | Matched terms |
|---:|---|---|
| 12 | `aletheus/neural/envelope/configuration.py` | config, configuration |
| 12 | `aletheus/span/providers/configuration.py` | config, configuration |
| 12 | `config/settings.py` | config, environment, schema, settings |
| 11 | `cardhawkos/config/settings.py` | config, configuration, settings |
| 9 | `aletheus/experience_gateway/security/auth_config.py` | config, environment |
| 9 | `tests/experience_gateway/test_auth_config.py` | config, configuration |
| 7 | `aletheus/strategic/span/config.py` | config, configuration |
| 7 | `core/config.py` | config, configuration |
| 7 | `security/config_validator.py` | config, configuration |
| 7 | `tests/test_experience_gateway_probes.py` | config, configuration, environment |
| 6 | `aletheus/adaptive_intelligence/capabilities/engine.py` | config, configuration |
| 6 | `aletheus/adaptive_intelligence/environment/engine.py` | environment |
| 6 | `aletheus/platform/deployment/environments.py` | environment |
| 6 | `config/development.py` | config, environment, settings |
| 6 | `config/production.py` | config, environment, settings |
| 6 | `config/staging.py` | config, environment, settings |
| 6 | `core/exceptions.py` | config, configuration |
| 6 | `tests/nimble/test_environment_promotion.py` | environment |
| 6 | `tests/strategic/test_span_config.py` | config |
| 6 | `tools/repository/audit_runtime_capabilities.py` | config, configuration, environment, schema, settings, validate config |
| 5 | `config/__init__.py` | config, settings |
| 5 | `config/constants.py` | config, schema |
| 5 | `tools/validation/nimble/validate_nimble_environment_automation.py` | environment, schema |

## constitutional_validation

- All candidates: **944**
- High-signal candidates: **40**

| Score | Path | Matched terms |
|---:|---|---|
| 18 | `aletheus/constitutional_library/governance.py` | constitution, constitutional, governance |
| 18 | `aletheus/constitutional_policy/core.py` | constitution, constitutional, policy |
| 18 | `aletheus/constitutional_policy/evaluator.py` | constitution, constitutional, policy |
| 18 | `aletheus/constitutional_policy/models.py` | constitution, constitutional, policy |
| 18 | `aletheus/constitutional_policy/registry.py` | constitution, constitutional, policy |
| 18 | `aletheus/platform_intelligence/constitutional_policy_engine/engine.py` | constitution, constitutional, policy |
| 18 | `aletheus/platform_intelligence/constitutional_policy_engine/exceptions.py` | constitution, constitutional, policy |
| 18 | `aletheus/platform_intelligence/constitutional_policy_engine/models.py` | constitution, constitutional, policy |
| 17 | `aletheus/constitutional_intelligence/audit.py` | audit, constitution, constitutional, governance |
| 17 | `tests/platform_intelligence/constitutional_policy_engine/test_cpe.py` | audit, constitution, constitutional, policy |
| 15 | `aletheus/constitutional_intelligence/enforcement.py` | constitution, constitutional, enforcement, governance |
| 15 | `aletheus/constitutional_intelligence/engine.py` | audit, constitution, constitutional, governance, policy |
| 15 | `aletheus/platform_intelligence/constitutional/transitions.py` | constitution, constitutional, policy |
| 15 | `aletheus/platform_intelligence/constitutional_runtime_executive/exceptions.py` | constitution, constitutional, policy |
| 15 | `aletheus/platform_intelligence/constitutional_runtime_executive/executive.py` | constitution, constitutional, policy |
| 15 | `aletheus/platform_intelligence/constitutional_runtime_governor/governor.py` | constitution, constitutional, enforcement, governance, policy |
| 15 | `aletheus/platform_intelligence/constitutional_runtime_supervisor/models.py` | constitution, constitutional, policy |
| 14 | `aletheus/platform_intelligence/constitutional_runtime_council/council.py` | constitution, constitutional, governance, policy |
| 14 | `aletheus/platform_intelligence/constitutional_runtime_council/models.py` | constitution, constitutional, governance, policy |
| 14 | `aletheus/platform_intelligence/constitutional_runtime_observatory/models.py` | constitution, constitutional, governance, policy |
| 14 | `aletheus/platform_intelligence/constitutional_runtime_observatory/observatory.py` | constitution, constitutional, governance, policy |
| 14 | `tests/platform_intelligence/constitutional_policy_engine/test_crx_integration.py` | constitution, constitutional, policy |
| 13 | `aletheus/constitutional_cases/models.py` | constitution, constitutional, governance |
| 13 | `aletheus/constitutional_events/registry.py` | constitution, constitutional, governance |
| 13 | `aletheus/constitutional_ledger/recorder.py` | constitution, constitutional, enforcement |
| 13 | `aletheus/constitutional_library/core.py` | constitution, constitutional, governance |
| 13 | `aletheus/constitutional_missions/models.py` | constitution, constitutional, governance |
| 13 | `aletheus/platform_intelligence/constitutional/enums.py` | constitution, constitutional, policy |
| 13 | `aletheus/platform_intelligence/constitutional/exceptions.py` | constitution, constitutional, policy |
| 13 | `aletheus/platform_intelligence/constitutional/object.py` | constitution, constitutional, policy |
| 13 | `aletheus/platform_intelligence/constitutional_graph/exceptions.py` | constitution, constitutional, policy |
| 13 | `aletheus/platform_intelligence/constitutional_runtime_supervisor/supervisor.py` | constitution, constitutional, policy |
| 12 | `Genesis14_SPAN_Constitutional_Intelligence/package/aletheus/span/rules/governance.py` | constitution, constitutional, governance |
| 12 | `aletheus/constitutional_audit/__init__.py` | audit, constitution, constitutional |
| 12 | `aletheus/constitutional_cases/engine.py` | constitution, constitutional |
| 12 | `aletheus/constitutional_cases/registry.py` | constitution, constitutional |
| 12 | `aletheus/constitutional_cognition/convergence.py` | constitution, constitutional |
| 12 | `aletheus/constitutional_cognition/models.py` | constitution, constitutional |
| 12 | `aletheus/constitutional_cognition/virtues.py` | constitution, constitutional |
| 12 | `aletheus/constitutional_enforcement/__init__.py` | constitution, constitutional, enforcement |

## observability

- All candidates: **268**
- High-signal candidates: **31**

| Score | Path | Matched terms |
|---:|---|---|
| 11 | `observability/telemetry.py` | metrics, observability, telemetry |
| 10 | `aletheus/production/observability/metrics.py` | metrics, observability |
| 8 | `metrics/system_metrics.py` | metrics, observability, telemetry |
| 7 | `aletheus/telemetry_v3/telemetry_core.py` | metrics, telemetry |
| 7 | `backups/runtime/core_v4.6.2_stable.py` | metrics, observability, telemetry |
| 7 | `migrations/genesis6/core_v481_registration_cutover.py` | metrics, observability, telemetry |
| 7 | `tests/test_aletheus_v35_telemetry.py` | observability, telemetry |
| 6 | `aletheus/atlas/metrics.py` | metrics |
| 6 | `aletheus/constitutional_instrumentation/bootstrap.py` | instrumentation |
| 6 | `aletheus/infrastructure/observability/engine.py` | observability |
| 6 | `aletheus/operations/observability_fabric/engine.py` | observability |
| 6 | `aletheus/platform_fabric/observability/engine.py` | observability |
| 6 | `aletheus/platform_surface/instrumentation.py` | instrumentation |
| 6 | `aletheus/runtime/anchors/cognitive_metrics.py` | metrics |
| 6 | `aletheus/runtime/domains/telemetry.py` | telemetry |
| 6 | `aletheus/runtime/managers/observability_manager.py` | observability |
| 6 | `aletheus/runtime/metrics.py` | metrics |
| 6 | `aletheus/runtime/registrations/telemetry_commands.py` | telemetry |
| 6 | `aletheus/services_economy/metrics/engine.py` | metrics |
| 6 | `aletheus/strategic/span/telemetry.py` | telemetry |
| 6 | `analytics/runtime/event_metrics.py` | metrics |
| 6 | `card_hawk/analytics/metrics.py` | metrics |
| 6 | `card_hawk/launch/operations/telemetry.py` | telemetry |
| 6 | `core/metrics.py` | metrics |
| 6 | `services/runtime_metrics.py` | metrics |
| 6 | `tests/nimble/test_baseline_governance.py` | metrics, telemetry |
| 6 | `tests/nimble/test_instrumentation_preview.py` | instrumentation |
| 6 | `tools/repository/audit_runtime_capabilities.py` | instrumentation, metrics, observability, runtime explorer, runtime intelligence, telemetry |
| 6 | `tools/repository/metrics.py` | metrics |
| 5 | `aletheus/constitutional_instrumentation/bus.py` | instrumentation, telemetry |
| 5 | `tools/build/build_nimble_intelligence_instrumentation_preview.py` | instrumentation, telemetry |

## resilience_recovery

- All candidates: **126**
- High-signal candidates: **28**

| Score | Path | Matched terms |
|---:|---|---|
| 7 | `bin/create_nimble_audit_recovery_source.py` | checkpoint, recovery |
| 7 | `bin/plan_nimble_audit_recovery.py` | checkpoint, recovery |
| 7 | `bin/validate_nimble_audit_recovery_source.py` | checkpoint, recovery |
| 7 | `plan_nimble_audit_recovery.py` | checkpoint, recovery |
| 7 | `tools/create/create_nimble_audit_recovery_source.py` | checkpoint, recovery |
| 7 | `tools/planning/plan_nimble_audit_recovery.py` | checkpoint, recovery |
| 7 | `tools/repository/audit_runtime_capabilities.py` | checkpoint, circuit breaker, fault tolerance, graceful degradation, recovery, restart, retry |
| 7 | `tools/validation/nimble/validate_nimble_audit_recovery_source.py` | checkpoint, recovery |
| 6 | `aletheus/immortality/recovery/engine.py` | recovery |
| 6 | `aletheus/infrastructure/recovery/engine.py` | recovery |
| 6 | `aletheus/production/runtime/recovery.py` | recovery |
| 6 | `aletheus/reliability/recovery/engine.py` | recovery |
| 6 | `aletheus/runtime/recovery/manager.py` | recovery |
| 6 | `aletheus/runtime_supervisor/recovery.py` | recovery |
| 6 | `aletheus/security/recovery/engine.py` | recovery |
| 6 | `aletheus/services_economy/recovery/engine.py` | recovery |
| 6 | `bin/create_nimble_audit_checkpoint.py` | checkpoint |
| 6 | `tests/nimble/test_audit_checkpoints.py` | checkpoint |
| 6 | `tests/nimble/test_audit_recovery.py` | recovery |
| 6 | `tests/platform_intelligence/constitutional_runtime_supervisor/test_crs.py` | recovery, restart |
| 6 | `tools/create/create_nimble_audit_checkpoint.py` | checkpoint |
| 5 | `bin/apply_nimble_audit_recovery.py` | checkpoint, recovery |
| 5 | `tests/nimble/audit/test_nimble_audit_recovery_apply_simulation.py` | checkpoint, recovery |
| 5 | `tests/nimble/audit/test_nimble_audit_recovery_simulation.py` | checkpoint, recovery |
| 5 | `tests/platform_intelligence/constitutional_runtime_governor/test_crg.py` | recovery, restart, retry |
| 5 | `tools/apply/apply_nimble_audit_recovery.py` | checkpoint, recovery |
| 5 | `tools/runtime_orchestration_checkpoint.py` | checkpoint, recovery |
| 5 | `tools/validation/nimble/validate_nimble_audit_recovery_contract.py` | checkpoint, recovery |

