# Genesis 8 Stale Command Capability Audit

- Runtime type: `aletheus.runtime.core.AletheusRuntime`
- Candidate components: **101**

## Stale Registration Modules

### `workspace_commands`

- `workspace.overview` → `runtime._cmd_workspace_overview` (line 12)
- `workspace.stats` → `runtime._cmd_workspace_stats` (line 17)
- `founder.journal.create` → `runtime._cmd_founder_journal_create` (line 22)
- `founder.journal.list` → `runtime._cmd_founder_journal_list` (line 27)
- `objective.create` → `runtime._cmd_objective_create` (line 32)
- `objective.list` → `runtime._cmd_objective_list` (line 37)
- `notification.create` → `runtime._cmd_notification_create` (line 42)
- `notification.list` → `runtime._cmd_notification_list` (line 47)

### `application_commands`

- `application.register` → `runtime._cmd_application_register` (line 12)
- `application.list` → `runtime._cmd_application_list` (line 17)
- `application.start` → `runtime._cmd_application_start` (line 22)
- `application.stop` → `runtime._cmd_application_stop` (line 27)
- `application.restart` → `runtime._cmd_application_restart` (line 32)
- `application.health` → `runtime._cmd_application_health` (line 37)
- `application.stats` → `runtime._cmd_application_stats` (line 42)
- `application.install` → `runtime._cmd_application_install` (line 47)
- `application.uninstall` → `runtime._cmd_application_uninstall` (line 52)
- `application.manifest` → `runtime._cmd_application_manifest` (line 57)
- `application.events` → `runtime._cmd_application_events` (line 62)
- `application.bootstrap.defaults` → `runtime._cmd_application_bootstrap_defaults` (line 67)

### `semantic_commands`

- `semantic.concept.create` → `runtime._cmd_semantic_concept_create` (line 12)
- `semantic.concept.search` → `runtime._cmd_semantic_concept_search` (line 17)
- `semantic.assert` → `runtime._cmd_semantic_assert` (line 22)
- `semantic.query` → `runtime._cmd_semantic_query` (line 27)
- `semantic.explain` → `runtime._cmd_semantic_explain` (line 32)
- `semantic.bootstrap.cardhawk` → `runtime._cmd_semantic_bootstrap_cardhawk` (line 37)
- `semantic.stats` → `runtime._cmd_semantic_stats` (line 42)

### `executive_commands`

- `executive.status` → `runtime._cmd_executive_status` (line 12)
- `executive.snapshot` → `runtime._cmd_executive_snapshot` (line 17)
- `executive.summary` → `runtime._cmd_executive_summary` (line 22)
- `executive.recommendations` → `runtime._cmd_executive_recommendations` (line 27)
- `executive.risks` → `runtime._cmd_executive_risks` (line 32)
- `executive.daily_brief` → `runtime._cmd_executive_daily_brief` (line 37)
- `executive.system_report` → `runtime._cmd_executive_system_report` (line 42)

### `planning_commands`

- `plan.generate` → `domain.generate` (line 14)
- `plan.list` → `domain.list` (line 19)

### `uil_commands`

- `uil.context` → `runtime._cmd_uil_context` (line 12)
- `uil.reason` → `runtime._cmd_uil_reason` (line 17)
- `uil.synthesize` → `runtime._cmd_uil_synthesize` (line 22)
- `uil.decide` → `runtime._cmd_uil_decide` (line 27)
- `uil.brief` → `runtime._cmd_uil_brief` (line 32)
- `uil.snapshot` → `runtime._cmd_uil_snapshot` (line 37)
- `uil.timeline` → `runtime._cmd_uil_timeline` (line 42)
- `uil.stats` → `runtime._cmd_uil_stats` (line 47)

## Candidate Runtime Components

### `agents`

- Type: `aletheus.agents_v2.agent_core.AletheusAutonomousAgentRuntime`
- `assign(agent_id: 'str', mission: 'str')`
- `bootstrap()`
- `heartbeat()`
- `list_agents()`
- `message(sender: 'str', recipient: 'str', message: 'str')`
- `pause(agent_id: 'str')`
- `register_default_agents()`
- `resume(agent_id: 'str')`
- `spawn(name: 'str', role: 'str')`
- `statistics()`
- `stats()`
- `status()`
- `stop(agent_id: 'str')`

### `agents_v2`

- Type: `aletheus.agents_v2.agent_core.AletheusAutonomousAgentRuntime`
- `assign(agent_id: 'str', mission: 'str')`
- `bootstrap()`
- `heartbeat()`
- `list_agents()`
- `message(sender: 'str', recipient: 'str', message: 'str')`
- `pause(agent_id: 'str')`
- `register_default_agents()`
- `resume(agent_id: 'str')`
- `spawn(name: 'str', role: 'str')`
- `statistics()`
- `stats()`
- `status()`
- `stop(agent_id: 'str')`

### `anchor_dependencies`

- Type: `aletheus.runtime.anchors.dependency.AnchorDependencyGraph`
- `can_detach(anchor)`
- `dependencies_for(anchor)`
- `register_dependency(anchor, requires)`
- `snapshot()`
- `startup_order()`
- `validate()`

### `anchor_governance_analyzer`

- Type: `aletheus.runtime.anchors.governance.AnchorGovernanceCouncil`
- `evaluate(anchor, proposal)`
- `history()`
- `snapshot()`

### `anchor_lifecycle`

- Type: `aletheus.runtime.anchors.lifecycle.AnchorLifecycleController`
- `attach(name)`
- `detach(name)`
- `health(name=None)`
- `history_snapshot()`
- `record(action, anchor)`
- `restart(name)`

### `anchor_registry`

- Type: `aletheus.runtime.anchors.registry.AnchorRegistry`
- `attach_all()`
- `get(name)`
- `list()`
- `register(name, anchor)`
- `status()`
- `validate_contracts()`

### `application_anchor`

- Type: `aletheus.runtime.anchors.application.ApplicationAnchorCircuit`
- `attach()`
- `capabilities()`
- `contract()`
- `detach()`
- `health()`
- `status()`
- `validate_contract()`

### `application_runtime`

- Type: `aletheus.platform.application_runtime.ApplicationRuntime`
- `health()`
- `install(name)`
- `manifest(name)`
- `register(name, version='1.0.0', description='', services=None)`
- `restart(name)`
- `start(name)`
- `stop(name)`

### `applications`

- Type: `aletheus.applications.application_core.AletheusApplicationManager`
- `events(app_id: 'str' = '', application_id: 'str' = '', name: 'str' = '') -> 'List[Dict[str, Any]]'`
- `get_application(app_id: 'str' = '', application_id: 'str' = '', name: 'str' = '') -> 'NativeApplication | None'`
- `health(app_id: 'str' = '', application_id: 'str' = '', name: 'str' = '') -> 'Dict[str, Any]'`
- `install_application(app_id: 'str', name: 'str', version: 'str' = '1.0.0', author: 'str' = '6th Dimension Multimedia', description: 'str' = '', autostart: 'bool' = False, permissions: 'List[str] | None' = None, dependencies: 'List[str] | None' = None, commands: 'List[str] | None' = None, services: 'List[str] | None' = None) -> 'NativeApplication'`
- `install_default_applications() -> 'List[Dict[str, Any]]'`
- `list_applications() -> 'List[Dict[str, Any]]'`
- `manifest(app_id: 'str' = '', application_id: 'str' = '', name: 'str' = '') -> 'Dict[str, Any]'`
- `register_application(name: 'str', version: 'str', description: 'str' = '', services: 'List[Dict[str, Any]] | None' = None, dependencies: 'List[str] | None' = None, commands: 'List[str] | None' = None) -> 'NativeApplication'`
- `register_card_hawk_foundation() -> 'NativeApplication'`
- `restart_application(app_id: 'str' = '', application_id: 'str' = '', name: 'str' = '') -> 'Dict[str, Any]'`
- `start_application(app_id: 'str' = '', application_id: 'str' = '', name: 'str' = '') -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`
- `stop_application(app_id: 'str' = '', application_id: 'str' = '', name: 'str' = '') -> 'Dict[str, Any]'`
- `uninstall_application(app_id: 'str' = '', name: 'str' = '') -> 'Dict[str, Any]'`

### `architecture_governance`

- Type: `aletheus.runtime.governance.architecture_rules.ArchitectureGovernanceRules`
- `commands_have_handlers()`
- `domains_registered()`
- `evaluate() -> 'Dict[str, Any]'`
- `registry_healthy()`
- `validator_healthy()`

### `architecture_validator`

- Type: `aletheus.runtime.architecture.validator.ArchitectureValidator`
- `validate() -> 'Dict[str, Any]'`

### `boot_certification`

- Type: `aletheus.runtime.certification.boot_certification.BootCertification`
- `certify(runtime)`

### `boot_context`

- Type: `aletheus.runtime.boot_pipeline.context.RuntimeBootContext`

### `boot_report`

- Type: `aletheus.runtime.boot_pipeline.report.BootReport`
- `finish()`
- `record(phase_name: str)`

### `boot_validator`

- Type: `aletheus.runtime.integrity.boot_validator.RuntimeBootValidator`
- `validate() -> 'Dict[str, Any]'`

### `certification_manager`

- Type: `aletheus.runtime.managers.certification_manager.CertificationManager`
- `certify()`
- `freeze_review()`

### `cognition`

- Type: `aletheus.cognition.cognition_core.AletheusCognitionCore`
- `complete_goal(goal_id: 'str') -> 'Dict[str, Any]'`
- `create_goal(title: 'str', description: 'str' = '', priority: 'str' = 'medium', owner: 'str' = 'Founder', application: 'str' = 'system') -> 'Goal'`
- `decision_history() -> 'List[Dict[str, Any]]'`
- `generate_plan(goal_id: 'str', goal_title: 'str' = '') -> 'Plan'`
- `list_goals(status: 'str | None' = None) -> 'List[Dict[str, Any]]'`
- `list_plans() -> 'List[Dict[str, Any]]'`
- `list_reasoning_sessions() -> 'List[Dict[str, Any]]'`
- `reason(prompt: 'str', evidence: 'List[str] | None' = None, assumptions: 'List[str] | None' = None) -> 'ReasoningSession'`
- `record_decision(title: 'str', decision: 'str', rationale: 'str', confidence: 'float' = 0.75, evidence: 'List[str] | None' = None) -> 'Decision'`
- `stats() -> 'Dict[str, Any]'`

### `command_auditor`

- Type: `aletheus.runtime.audit.command_surface.CommandSurfaceAuditor`
- `audit()`

### `command_bootstrapper`

- Type: `aletheus.runtime.command_bootstrap.bootstrapper.RuntimeCommandBootstrapper`
- `bootstrap(runtime)`

### `command_manager`

- Type: `aletheus.runtime.managers.command_manager.CommandManager`
- `bootstrap()`
- `count()`
- `list()`
- `status()`

### `commands`

- Type: `aletheus.runtime.commands.command_bus.CommandBus`
- `categories() -> 'list[str]'`
- `count() -> 'int'`
- `dispatch(command: 'str', payload: 'dict[str, Any] | None' = None, application: 'str' = 'system') -> 'RuntimeContext'`
- `execute(command: 'str', payload: 'dict[str, Any] | None' = None, application: 'str' = 'system') -> 'RuntimeContext'`
- `has(command: 'str') -> 'bool'`
- `health() -> 'dict[str, Any]'`
- `list() -> 'list[str]'`
- `register(name: 'str', handler: 'Callable[..., Any]', category: 'str' = 'general', description: 'str' = '', metadata: 'dict[str, Any] | None' = None, *, replace: 'bool' = False)`
- `register_context_handler(name: 'str', handler: 'Callable[[RuntimeContext], RuntimeContext]', *, replace: 'bool' = False) -> 'Callable[[RuntimeContext], RuntimeContext]'`
- `unregister(name: 'str') -> 'bool'`

### `compat`

- Type: `aletheus.runtime.compat.registry.CompatibilityRegistry`
- `list()`
- `register(alias: 'str', implementation: 'Any', capabilities=None)`
- `resolve(alias)`
- `statistics()`

### `compatibility_adapter`

- Type: `aletheus.runtime.adapters.compatibility_adapter.CompatibilityCommandAdapter`
- `contract(context)`
- `list(context)`
- `resolve(context)`
- `statistics(context)`

### `copilot`

- Type: `aletheus.copilot.copilot_core.AletheusFounderCopilot`
- `ask(prompt: 'str', runtime: 'Any') -> 'CopilotExchange'`
- `brief(runtime: 'Any') -> 'Dict[str, Any]'`
- `classify_intent(prompt: 'str') -> 'str'`
- `history() -> 'List[Dict[str, Any]]'`
- `recommend(runtime: 'Any') -> 'List[Dict[str, Any]]'`
- `stats() -> 'Dict[str, Any]'`
- `timeline(runtime: 'Any') -> 'Dict[str, Any]'`

### `decision`

- Type: `aletheus.decision_v2.decision_core.AletheusAutonomousDecisionEngine`
- `add_policy(name: 'str', description: 'str', policy_type: 'str' = 'general', weight: 'float' = 1.0) -> 'Dict[str, Any]'`
- `bootstrap() -> 'Dict[str, Any]'`
- `evaluate(title: 'str', objective: 'str', options: 'List[Dict[str, Any]]', policy: 'str', runtime: 'Any') -> 'Dict[str, Any]'`
- `execute(decision_id: 'str') -> 'Dict[str, Any]'`
- `explain(decision_id: 'str') -> 'Dict[str, Any]'`
- `history() -> 'Dict[str, Any]'`
- `rollback(decision_id: 'str') -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`

### `diagnostics`

- Type: `aletheus.runtime.diagnostics.RuntimeDiagnostics`
- `report() -> 'Dict[str, Any]'`

### `distributed`

- Type: `aletheus.distributed_v3.distributed_core.AletheusDistributedRuntimeFabric`
- `assign_task(*args, **kwargs)`
- `bootstrap()`
- `bootstrap_primary_cluster()`
- `broadcast(*args, **kwargs)`
- `cluster_status(cluster_id='')`
- `create_cluster(name='Aletheus Cluster')`
- `elect_leader()`
- `heartbeat()`
- `history()`
- `join(node_name: 'str', capabilities=None, services=None)`
- `leave(node_id: 'str')`
- `list_clusters()`
- `nodes()`
- `register_node(**kwargs)`
- `remove_node(node_id)`
- `services()`
- `statistics()`
- `stats()`
- `status()`

### `engines`

- Type: `aletheus.runtime.registries.EngineRegistry`
- `count() -> 'int'`
- `list() -> 'List[str]'`
- `register(name: 'str', handler: 'Callable[[RuntimeContext], RuntimeContext]') -> 'None'`
- `run(name: 'str', context: 'RuntimeContext') -> 'RuntimeContext'`

### `enterprise`

- Type: `aletheus.enterprise.enterprise_core.AletheusEnterpriseCore`
- `audit(actor: 'str', action: 'str', target: 'str', outcome: 'str' = 'recorded', metadata: 'Dict[str, Any] | None' = None) -> 'AuditRecord'`
- `audit_history() -> 'List[Dict[str, Any]]'`
- `bootstrap_cardhawk_enterprise() -> 'EnterpriseOrganization'`
- `create_department(organization_id: 'str', name: 'str', description: 'str' = '') -> 'Dict[str, Any]'`
- `create_organization(name: 'str', description: 'str' = '', applications: 'List[str] | None' = None) -> 'EnterpriseOrganization'`
- `create_policy(organization_id: 'str', name: 'str', description: 'str' = '', scope: 'str' = 'enterprise', rules: 'List[str] | None' = None) -> 'Dict[str, Any]'`
- `create_team(organization_id: 'str', department_id: 'str', name: 'str', description: 'str' = '', members: 'List[str] | None' = None) -> 'Dict[str, Any]'`
- `get_organization(organization_id: 'str' = '', name: 'str' = '') -> 'EnterpriseOrganization | None'`
- `governed_action(actor: 'str', action: 'str', target: 'str', organization_id: 'str' = '', metadata: 'Dict[str, Any] | None' = None) -> 'Dict[str, Any]'`
- `list_organizations() -> 'List[Dict[str, Any]]'`
- `stats() -> 'Dict[str, Any]'`

### `event_adapter`

- Type: `aletheus.runtime.adapters.event_adapter.EventCommandAdapter`
- `bootstrap(context)`
- `history(context)`
- `publish(context)`
- `replay(context)`
- `statistics(context)`
- `subscribe(context)`
- `unsubscribe(context)`

### `event_bus`

- Type: `aletheus.event_bus_v3.event_bus_core.AletheusEventBus`
- `bootstrap()`
- `history(topic=None)`
- `publish(topic, payload, publisher='runtime', priority='normal', source=None, **kwargs)`
- `replay(topic)`
- `statistics()`
- `subscribe(topic, subscriber)`
- `unsubscribe(topic, subscriber)`

### `event_bus_v3`

- Type: `aletheus.event_bus_v3.event_bus_core.AletheusEventBus`
- `bootstrap()`
- `history(topic=None)`
- `publish(topic, payload, publisher='runtime', priority='normal', source=None, **kwargs)`
- `replay(topic)`
- `statistics()`
- `subscribe(topic, subscriber)`
- `unsubscribe(topic, subscriber)`

### `events`

- Type: `aletheus.runtime.events.EventBus`
- `count() -> 'int'`
- `publish(event_type: 'str', payload: 'Dict[str, Any]', source: 'str' = 'system') -> 'RuntimeEvent'`
- `recent(limit: 'int' = 100) -> 'List[Dict[str, Any]]'`
- `subscribe(event_type: 'str', handler: 'Callable[[RuntimeEvent], None]') -> 'None'`

### `executive`

- Type: `aletheus.executive.executive_core.AletheusExecutiveCore`
- `analyze_risks(runtime: 'Any') -> 'List[Dict[str, Any]]'`
- `daily_brief(runtime: 'Any') -> 'Dict[str, Any]'`
- `generate_recommendations(runtime: 'Any') -> 'List[Dict[str, Any]]'`
- `snapshot(runtime: 'Any') -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`
- `summarize(runtime: 'Any') -> 'Dict[str, Any]'`
- `system_report(runtime: 'Any') -> 'Dict[str, Any]'`

### `federation_v3`

- Type: `aletheus.federation_v3.federation_core.AletheusFederationEngine`
- `bootstrap()`
- `broadcast(message)`
- `discover()`
- `join(name, address, capabilities=None, services=None)`
- `leave(node_id)`
- `query()`
- `statistics()`

### `genesis6_report`

- Type: `aletheus.runtime.release.genesis6_report.Genesis6CertificationReport`
- `generate(runtime)`

### `genesis6_review`

- Type: `aletheus.runtime.release.genesis6_review.Genesis6FreezeReview`
- `review(runtime)`

### `genesis6_validator`

- Type: `aletheus.runtime.release.genesis6_validator.Genesis6Validator`
- `validate(runtime)`

### `governance`

- Type: `aletheus.runtime.governance.governance_core.GovernanceEngine`
- `overall_status()`
- `validate_constitution()`
- `validate_principle_x()`
- `validate_repository()`
- `validate_runtime()`

### `governance_history`

- Type: `aletheus.runtime.governance.history.GovernanceHistory`
- `history()`
- `record(event_type: 'str', payload: 'dict')`

### `governance_manager`

- Type: `aletheus.runtime.managers.governance_manager.GovernanceManager`
- `status()`

### `graph_adapter`

- Type: `aletheus.runtime.adapters.graph_adapter.GraphCommandAdapter`
- `entity_create(context)`
- `entity_search(context)`
- `graph_export(context)`
- `graph_query(context)`
- `graph_stats(context)`
- `relationship_create(context)`
- `relationship_search(context)`

### `hardening`

- Type: `aletheus.runtime.hardening.RuntimeHardening`
- `audit() -> 'Dict[str, Any]'`
- `dashboard() -> 'Dict[str, Any]'`
- `documentation() -> 'str'`
- `selftest() -> 'Dict[str, Any]'`
- `snapshot() -> 'Dict[str, Any]'`
- `write_documentation(path: 'str' = 'RUNTIME_DOCUMENTATION.md') -> 'Dict[str, Any]'`

### `health_manager`

- Type: `aletheus.runtime.managers.health_manager.HealthManager`
- `health()`

### `high_availability`

- Type: `aletheus.high_availability_v3.high_availability_core.AletheusHighAvailabilityEngine`
- `bootstrap()`
- `demote(node_id: 'str')`
- `failover()`
- `join(name: 'str', metadata=None)`
- `leave(node_id: 'str')`
- `promote(node_id: 'str')`
- `recover(node_id: 'str')`
- `replicate(payload=None)`
- `statistics()`
- `status()`

### `high_availability_v3`

- Type: `aletheus.high_availability_v3.high_availability_core.AletheusHighAvailabilityEngine`
- `bootstrap()`
- `demote(node_id: 'str')`
- `failover()`
- `join(name: 'str', metadata=None)`
- `leave(node_id: 'str')`
- `promote(node_id: 'str')`
- `recover(node_id: 'str')`
- `replicate(payload=None)`
- `statistics()`
- `status()`

### `intelligence`

- Type: `aletheus.intelligence.intelligence_core.AletheusUniversalIntelligence`
- `brief(runtime: 'Any') -> 'Dict[str, Any]'`
- `build_context(question: 'str', runtime: 'Any') -> 'IntelligenceContext'`
- `confidence_score(context: 'Dict[str, Any]') -> 'float'`
- `decide(question: 'str', runtime: 'Any') -> 'IntelligenceDecision'`
- `reason(question: 'str', runtime: 'Any') -> 'Dict[str, Any]'`
- `snapshot(runtime: 'Any') -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`
- `synthesize(question: 'str', runtime: 'Any') -> 'Dict[str, Any]'`
- `timeline() -> 'Dict[str, Any]'`

### `intelligence_dispatcher`

- Type: `aletheus.runtime.kernel.dispatcher.IntelligenceDispatcher`
- `dispatch(runtime: 'Any', command: 'str', payload: 'Dict | None' = None)`
- `statistics()`

### `intelligence_orchestrator`

- Type: `aletheus.runtime.kernel.orchestrator.IntelligenceOrchestrator`
- `create_task(command: 'str', payload: 'Dict[str, Any] | None' = None, priority: 'int' = 5, metadata: 'Dict[str, Any] | None' = None) -> 'Dict[str, Any]'`
- `execute(command: 'str', payload: 'Dict[str, Any] | None', runtime: 'Any', priority: 'int' = 5) -> 'Dict[str, Any]'`
- `execute_task(task_id: 'str', runtime: 'Any') -> 'Dict[str, Any]'`
- `list_tasks() -> 'Dict[str, Any]'`
- `statistics() -> 'Dict[str, Any]'`

### `intelligence_scheduler`

- Type: `aletheus.runtime.kernel.scheduler.IntelligenceScheduler`
- `next() -> 'Dict[str, Any]'`
- `schedule(task_id: 'str', priority: 'int' = 5) -> 'Dict[str, Any]'`
- `statistics() -> 'Dict[str, Any]'`

### `intelligence_supervisor`

- Type: `aletheus.runtime.kernel.supervisor.IntelligenceSupervisor`
- `check(runtime: 'Any') -> 'Dict[str, Any]'`
- `statistics() -> 'Dict[str, Any]'`

### `invariant_manager`

- Type: `aletheus.runtime.managers.invariant_manager.InvariantManager`
- `check()`

### `kernel`

- Type: `aletheus.runtime.kernel.executor.KernelExecutor`
- `execute(command: 'str', payload: 'Dict[str, Any] | None' = None, priority: 'int' = 5)`
- `statistics()`

### `kernel_v2`

- Type: `aletheus.kernel_v2.kernel_core.AletheusAutonomousKernel`
- `boot(runtime: 'Any') -> 'Dict[str, Any]'`
- `publish(event_type: 'str', source: 'str', payload: 'Dict[str, Any] | None' = None) -> 'KernelEvent'`
- `register(name: 'str', item_type: 'str', status: 'str' = 'registered', metadata: 'Dict[str, Any] | None' = None) -> 'KernelRegistryItem'`
- `route_event(event_type: 'str', source: 'str', payload: 'Dict[str, Any] | None' = None) -> 'Dict[str, Any]'`
- `snapshot() -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`
- `status() -> 'Dict[str, Any]'`
- `sync_runtime(runtime: 'Any') -> 'Dict[str, Any]'`

### `knowledge`

- Type: `aletheus.knowledge.knowledge_core.AletheusKnowledgeCore`
- `create_entity(label: 'str', entity_type: 'str' = 'generic', properties: 'Dict[str, Any] | None' = None) -> 'Entity'`
- `create_relationship(source_id: 'str', target_id: 'str', relationship_type: 'str', properties: 'Dict[str, Any] | None' = None) -> 'Relationship'`
- `graph_export() -> 'Dict[str, Any]'`
- `graph_query(entity_id: 'str') -> 'Dict[str, Any]'`
- `search_entities(label: 'str | None' = None, entity_type: 'str | None' = None) -> 'List[Dict[str, Any]]'`
- `search_relationships(source_id: 'str | None' = None, target_id: 'str | None' = None, relationship_type: 'str | None' = None) -> 'List[Dict[str, Any]]'`
- `stats() -> 'Dict[str, Any]'`

### `knowledge_anchor`

- Type: `aletheus.runtime.anchors.knowledge.KnowledgeAnchorCircuit`
- `attach()`
- `capabilities()`
- `contract()`
- `detach()`
- `health()`
- `status()`
- `validate_contract()`

### `knowledge_graph`

- Type: `aletheus.knowledge_graph.knowledge_graph_core.KnowledgeGraphCore`
- `analyze()`
- `connect(source, target)`
- `register_node(node)`

### `learning`

- Type: `aletheus.learning.learning_core.AletheusAdaptiveLearning`
- `create_lesson(title: 'str', lesson: 'str', source_experience_id: 'str' = '', confidence: 'float' = 0.75, tags: 'List[str] | None' = None) -> 'LearnedLesson'`
- `discover_patterns() -> 'List[Dict[str, Any]]'`
- `feedback(experience_id: 'str', outcome: 'str', lesson: 'str' = '', confidence: 'float' = 0.8) -> 'Dict[str, Any]'`
- `improve(runtime: 'Any') -> 'List[Dict[str, Any]]'`
- `record_experience(event_type: 'str', description: 'str', source: 'str' = 'aletheus', outcome: 'str' = 'unknown', confidence: 'float' = 0.75, metadata: 'Dict[str, Any] | None' = None) -> 'LearningExperience'`
- `snapshot() -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`

### `memory`

- Type: `aletheus.memory.core.AletheusMemoryCore`
- `clear_working_memory() -> 'int'`
- `recall(key: 'Optional[str]' = None, namespace: 'Optional[str]' = None, memory_type: 'Optional[str]' = None, tag: 'Optional[str]' = None, limit: 'int' = 100) -> 'List[Dict[str, Any]]'`
- `remember(key: 'str', value: 'Any', namespace: 'str' = 'system', memory_type: 'str' = 'working', tags: 'Optional[List[str]]' = None) -> 'MemoryRecord'`
- `stats() -> 'Dict[str, Any]'`

### `memory_anchor`

- Type: `aletheus.runtime.anchors.memory.MemoryAnchorCircuit`
- `attach()`
- `capabilities()`
- `contract()`
- `detach()`
- `health()`
- `status()`
- `validate_contract()`

### `memory_mesh`

- Type: `aletheus.memory_mesh.mesh_core.AletheusMemoryMesh`
- `cache(object_id: 'str' = '') -> 'Dict[str, Any]'`
- `history(object_id: 'str' = '') -> 'Dict[str, Any]'`
- `replicate(object_id: 'str' = '', target_node: 'str' = 'primary') -> 'Dict[str, Any]'`
- `restore(snapshot_id: 'str') -> 'Dict[str, Any]'`
- `retrieve(object_id: 'str' = '', key: 'str' = '', namespace: 'str' = 'global') -> 'Dict[str, Any]'`
- `search(query: 'str' = '', tags: 'List[str] | None' = None, namespace: 'str' = '') -> 'List[Dict[str, Any]]'`
- `snapshot(name: 'str' = 'Memory Mesh Snapshot') -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`
- `store(key: 'str', value: 'Any', namespace: 'str' = 'global', object_type: 'str' = 'generic', tags: 'List[str] | None' = None, owner: 'str' = 'aletheus', metadata: 'Dict[str, Any] | None' = None) -> 'Dict[str, Any]'`
- `sync(node: 'str' = 'distributed_fabric') -> 'Dict[str, Any]'`

### `metrics`

- Type: `aletheus.runtime.metrics.RuntimeMetrics`
- `count() -> 'int'`
- `recent(limit: 'int' = 100) -> 'List[Dict[str, Any]]'`
- `record(name: 'str', value: 'Any') -> 'None'`

### `mission`

- Type: `aletheus.mission.mission_core.AletheusMissionCore`
- `complete_mission(mission_id: 'str') -> 'Dict[str, Any]'`
- `complete_task(mission_id: 'str', task_id: 'str') -> 'Dict[str, Any]'`
- `create_mission(title: 'str', objective: 'str', application: 'str' = 'system', priority: 'str' = 'medium', tasks: 'List[Dict[str, Any]] | None' = None) -> 'Mission'`
- `generate_mission_from_goal(goal_title: 'str', goal_description: 'str' = '', application: 'str' = 'system', priority: 'str' = 'high') -> 'Mission'`
- `get_mission(mission_id: 'str') -> 'Mission | None'`
- `history() -> 'List[Dict[str, Any]]'`
- `list_missions(status: 'str | None' = None) -> 'List[Dict[str, Any]]'`
- `run_mission(mission_id: 'str') -> 'MissionRun'`
- `stats() -> 'Dict[str, Any]'`

### `mission_adapter`

- Type: `aletheus.runtime.adapters.mission_adapter.MissionCommandAdapter`
- `complete(context)`
- `create(context)`
- `from_goal(context)`
- `history(context)`
- `list(context)`
- `run(context)`
- `stats(context)`
- `task_complete(context)`

### `mission_v2`

- Type: `aletheus.missions_v2.mission_core.AletheusAutonomousMissionEngine`
- `cancel_mission(mission_id: 'str') -> 'Dict[str, Any]'`
- `create_mission(title: 'str', objective: 'str', application: 'str' = 'AletheusOS', priority: 'str' = 'high', tasks: 'List[Dict[str, Any]] | None' = None) -> 'AutonomousMissionV2'`
- `default_tasks(objective: 'str', application: 'str') -> 'List[Dict[str, Any]]'`
- `emit(mission_id: 'str', event_type: 'str', message: 'str', payload: 'Dict[str, Any] | None' = None) -> 'MissionTelemetryV2'`
- `execute_mission(mission_id: 'str', runtime: 'Any') -> 'Dict[str, Any]'`
- `execute_next(mission_id: 'str', runtime: 'Any') -> 'Dict[str, Any]'`
- `get_mission(mission_id: 'str') -> 'AutonomousMissionV2 | None'`
- `list_missions(status: 'str | None' = None) -> 'List[Dict[str, Any]]'`
- `mission_telemetry(mission_id: 'str' = '') -> 'List[Dict[str, Any]]'`
- `pause_mission(mission_id: 'str') -> 'Dict[str, Any]'`
- `plan_mission(mission_id: 'str', runtime: 'Any') -> 'Dict[str, Any]'`
- `resume_mission(mission_id: 'str') -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`

### `persistence_v3`

- Type: `aletheus.persistence_v3.persistence_core.AletheusPersistenceEngine`
- `bootstrap()`
- `export()`
- `import_state(state: 'Dict[str, Any]')`
- `load()`
- `restore(snapshot_id: 'str')`
- `save(runtime=None)`
- `snapshot(name: 'str' = 'Runtime Snapshot', runtime=None)`
- `statistics()`

### `pipelines`

- Type: `aletheus.runtime.pipeline.PipelineExecutor`
- `execute(pipeline_name: 'str', context: 'RuntimeContext') -> 'RuntimeContext'`
- `list() -> 'Dict[str, Any]'`
- `register(pipeline: 'Pipeline') -> 'None'`

### `planning`

- Type: `aletheus.planning_v2.planning_core.AletheusPlanningEngine`
- `bootstrap()`
- `complete(plan_id)`
- `create(goal: 'str')`
- `execute(plan_id)`
- `list_plans()`
- `progress(plan_id)`
- `register_default_plans()`
- `replan(plan_id)`
- `statistics()`
- `status()`
- `version()`

### `planning_v2`

- Type: `aletheus.planning_v2.planning_core.AletheusPlanningEngine`
- `bootstrap()`
- `complete(plan_id)`
- `create(goal: 'str')`
- `execute(plan_id)`
- `list_plans()`
- `progress(plan_id)`
- `register_default_plans()`
- `replan(plan_id)`
- `statistics()`
- `status()`
- `version()`

### `plugins`

- Type: `aletheus.plugins.runtime_plugin_manager.RuntimePluginManager`
- `list() -> 'Dict[str, Dict[str, str]]'`
- `register(plugin: 'RuntimePlugin') -> 'None'`

### `plugins_v3`

- Type: `aletheus.plugins_v3.plugin_core.AletheusPluginManager`
- `bootstrap()`
- `disable(plugin_id)`
- `enable(plugin_id)`
- `install(**payload)`
- `list()`
- `remove(plugin_id)`
- `statistics()`
- `status()`
- `update(plugin_id, version)`

### `principle_x`

- Type: `aletheus.runtime.governance.principle_x.PrincipleXValidator`
- `validate()`

### `queue`

- Type: `aletheus.runtime.job_queue.JobQueue`
- `enqueue(command: 'str', payload: 'Dict[str, Any] | None' = None, application: 'str' = 'system') -> 'RuntimeJob'`
- `list() -> 'List[Dict[str, Any]]'`
- `run_next() -> 'RuntimeJob | None'`

### `readiness_snapshot`

- Type: `aletheus.runtime.readiness.snapshot.RuntimeReadinessSnapshot`
- `generate(runtime)`

### `reasoning`

- Type: `aletheus.reasoning.reasoning_core.AletheusCognitiveReasoningEngine`
- `add_rule(name: 'str', description: 'str', rule_type: 'str' = 'general', weight: 'float' = 0.75) -> 'Dict[str, Any]'`
- `bootstrap_rules() -> 'Dict[str, Any]'`
- `confidence() -> 'Dict[str, Any]'`
- `decision(question: 'str', runtime: 'Any', context: 'Dict[str, Any] | None' = None) -> 'Dict[str, Any]'`
- `evaluate(question: 'str', runtime: 'Any', context: 'Dict[str, Any] | None' = None) -> 'Dict[str, Any]'`
- `explain(trace_id: 'str' = '') -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`
- `trace(trace_id: 'str' = '') -> 'Dict[str, Any]'`

### `registry`

- Type: `aletheus.runtime.registry.runtime_registry.RuntimeRegistry`
- `register_component(name: 'str', metadata: 'Dict[str, Any]')`
- `register_domain(name: 'str', instance: 'Any')`
- `register_service(name: 'str', instance: 'Any')`
- `snapshot()`

### `registry_compatibility`

- Type: `aletheus.runtime.registry.compatibility.RegistryCompatibility`
- `migrate(registry)`
- `validate(registry)`

### `registry_governance`

- Type: `aletheus.runtime.governance.registry_rules.RegistryGovernanceRules`
- `validate(runtime)`

### `registry_manager`

- Type: `aletheus.runtime.managers.registry_manager.RegistryManager`
- `healthy()`
- `snapshot()`

### `release`

- Type: `aletheus.release.core.AletheusReleaseCore`
- `status() -> 'Dict[str, Any]'`
- `validate_runtime(runtime: 'Any') -> 'Dict[str, Any]'`

### `runtime_adapter`

- Type: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter`
- `audit(context)`
- `boot_validate(context)`
- `dashboard(context)`
- `docs(context)`
- `doctor(context)`
- `health_report(context)`
- `invariants(context)`
- `selftest(context)`
- `snapshot(context)`

### `runtime_doctor`

- Type: `aletheus.runtime.integrity.doctor.RuntimeDoctor`
- `run() -> 'Dict[str, Any]'`
- `write_reports() -> 'Dict[str, Any]'`

### `runtime_facade`

- Type: `aletheus.runtime.managers.runtime_facade.RuntimeFacade`
- `applications_snapshot()`
- `architecture_snapshot()`
- `boot_certification_validate()`
- `diagnostics()`
- `health()`
- `invariants()`
- `platform_services()`
- `runtime_readiness()`

### `runtime_invariants`

- Type: `aletheus.runtime.integrity.invariants.RuntimeInvariantEngine`
- `validate() -> 'Dict[str, Any]'`

### `scheduler`

- Type: `aletheus.runtime.scheduler.Scheduler`
- `list() -> 'Dict[str, Any]'`
- `register(name: 'str', description: 'str', handler: 'Callable[[], Any]') -> 'None'`
- `run(name: 'str') -> 'Any'`

### `security`

- Type: `aletheus.security_v3.security_core.AletheusSecurityEngine`
- `assign_role(identity: 'str', role: 'str')`
- `audit(action: 'str', actor: 'str', status='success', metadata=None)`
- `authenticate(identity: 'str')`
- `authorize(identity: 'str', permission: 'str')`
- `bootstrap()`
- `create_role(name: 'str', permissions=None)`
- `policy(name: 'str', definition=None)`
- `statistics()`

### `security_v3`

- Type: `aletheus.security_v3.security_core.AletheusSecurityEngine`
- `assign_role(identity: 'str', role: 'str')`
- `audit(action: 'str', actor: 'str', status='success', metadata=None)`
- `authenticate(identity: 'str')`
- `authorize(identity: 'str', permission: 'str')`
- `bootstrap()`
- `create_role(name: 'str', permissions=None)`
- `policy(name: 'str', definition=None)`
- `statistics()`

### `semantic`

- Type: `aletheus.semantic.semantic_core.AletheusSemanticCore`
- `assert_fact(subject: 'str', predicate: 'str', object_value: 'str', confidence: 'float' = 0.75, source: 'str' = 'aletheus', metadata: 'Dict[str, Any] | None' = None) -> 'SemanticAssertion'`
- `bootstrap_cardhawk_semantics() -> 'Dict[str, Any]'`
- `create_concept(name: 'str', concept_type: 'str' = 'concept', description: 'str' = '', aliases: 'List[str] | None' = None, metadata: 'Dict[str, Any] | None' = None) -> 'SemanticConcept'`
- `explain_concept(name: 'str') -> 'Dict[str, Any]'`
- `find_concept_exact(name: 'str') -> 'SemanticConcept | None'`
- `query_assertions(subject: 'str' = '', predicate: 'str' = '', object_value: 'str' = '') -> 'List[Dict[str, Any]]'`
- `search_concepts(query: 'str' = '', concept_type: 'str' = '') -> 'List[Dict[str, Any]]'`
- `stats() -> 'Dict[str, Any]'`

### `service_registry`

- Type: `aletheus.platform.service_registry.ServiceRegistry`
- `get(name)`
- `health()`
- `list()`
- `register(name, version='1.0.0', domain='core', status='active', metadata=None)`

### `services`

- Type: `aletheus.runtime.services.service_registry.ServiceRegistry`
- `get(name)`
- `has(name)`
- `list()`
- `register(name, service)`
- `statistics()`
- `unregister(name)`

### `snapshot_manager`

- Type: `aletheus.runtime.managers.snapshot_manager.SnapshotManager`
- `snapshot()`

### `spa`

- Type: `aletheus.runtime.intelligence.spa_bridge.RuntimeSPABridge`
- `assess()`
- `drift_report()`
- `registry_governance_check()`

### `telemetry_v3`

- Type: `aletheus.telemetry_v3.telemetry_core.AletheusTelemetryEngine`
- `bootstrap()`
- `health(component: 'str' = 'runtime', status: 'str' = 'healthy')`
- `log(level: 'str', message: 'str', source: 'str' = 'runtime', metadata=None)`
- `metric(name: 'str', value: 'Any', category: 'str' = 'runtime', metadata=None)`
- `record(name: 'str', value: 'Any' = None, category: 'str' = 'runtime', metadata=None)`
- `statistics()`
- `timeline(message: 'str', source: 'str' = 'runtime', metadata=None)`
- `trace(name: 'str', status: 'str' = 'completed', parent_span=None, correlation_id=None, metadata=None)`

### `tenancy`

- Type: `aletheus.tenancy_v3.tenancy_core.AletheusTenancyEngine`
- `bootstrap()`
- `create_organization(name: 'str', metadata=None)`
- `create_tenant(organization_id: 'str', name: 'str', environment: 'str' = 'production', quotas=None, metadata=None)`
- `create_workspace(tenant_id: 'str', name: 'str', metadata=None)`
- `delete_tenant(tenant_id: 'str')`
- `delete_workspace(workspace_id: 'str')`
- `health()`
- `list_tenants()`
- `list_workspaces(tenant_id=None)`
- `select_tenant(tenant_id: 'str')`
- `statistics()`
- `update_organization(organization_id: 'str', name=None, metadata=None, status=None)`

### `tenancy_v3`

- Type: `aletheus.tenancy_v3.tenancy_core.AletheusTenancyEngine`
- `bootstrap()`
- `create_organization(name: 'str', metadata=None)`
- `create_tenant(organization_id: 'str', name: 'str', environment: 'str' = 'production', quotas=None, metadata=None)`
- `create_workspace(tenant_id: 'str', name: 'str', metadata=None)`
- `delete_tenant(tenant_id: 'str')`
- `delete_workspace(workspace_id: 'str')`
- `health()`
- `list_tenants()`
- `list_workspaces(tenant_id=None)`
- `select_tenant(tenant_id: 'str')`
- `statistics()`
- `update_organization(organization_id: 'str', name=None, metadata=None, status=None)`

### `validation_manager`

- Type: `aletheus.runtime.managers.validation_manager.ValidationManager`
- `boot_certification()`
- `genesis6_validate()`

### `workflow`

- Type: `aletheus.workflow_v3.workflow_core.AletheusWorkflowEngine`
- `bootstrap()`
- `cancel(workflow_id)`
- `create(title, description)`
- `pause(workflow_id)`
- `resume(workflow_id)`
- `start(workflow_id)`
- `statistics()`
- `status()`

### `workflow_v2`

- Type: `aletheus.workflows_v2.workflow_core.AletheusWorkflowFabric`
- `cancel(workflow_id: 'str') -> 'Dict[str, Any]'`
- `create_workflow(title: 'str', objective: 'str', application: 'str' = 'AletheusOS', nodes: 'List[Dict[str, Any]] | None' = None) -> 'WorkflowExecution'`
- `default_nodes(objective: 'str', application: 'str') -> 'List[Dict[str, Any]]'`
- `emit(workflow_id: 'str', event_type: 'str', message: 'str', payload: 'Dict[str, Any] | None' = None) -> 'WorkflowEvent'`
- `execute_next(workflow_id: 'str', runtime: 'Any') -> 'Dict[str, Any]'`
- `execute_node(workflow: 'WorkflowExecution', node: 'WorkflowNode', runtime: 'Any') -> 'Dict[str, Any]'`
- `execute_workflow(workflow_id: 'str', runtime: 'Any') -> 'Dict[str, Any]'`
- `get_workflow(workflow_id: 'str') -> 'WorkflowExecution | None'`
- `history(workflow_id: 'str' = '') -> 'List[Dict[str, Any]]'`
- `list_workflows(status: 'str | None' = None) -> 'List[Dict[str, Any]]'`
- `pause(workflow_id: 'str') -> 'Dict[str, Any]'`
- `resume(workflow_id: 'str') -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`

### `workflow_v3`

- Type: `aletheus.workflow_v3.workflow_core.AletheusWorkflowEngine`
- `bootstrap()`
- `cancel(workflow_id)`
- `create(title, description)`
- `pause(workflow_id)`
- `resume(workflow_id)`
- `start(workflow_id)`
- `statistics()`
- `status()`

### `workflows`

- Type: `aletheus.runtime.workflow.WorkflowExecutor`
- `execute(workflow_name: 'str', application: 'str' = 'system') -> 'RuntimeContext'`
- `list() -> 'Dict[str, Any]'`
- `register(workflow: 'WorkflowGraph') -> 'None'`

### `workspace`

- Type: `aletheus.workspace.workspace_core.AletheusFounderWorkspace`
- `create_journal_entry(title: 'str', body: 'str', category: 'str' = 'general', tags: 'List[str] | None' = None) -> 'FounderJournalEntry'`
- `create_notification(title: 'str', message: 'str', severity: 'str' = 'info', source: 'str' = 'aletheus') -> 'FounderNotification'`
- `create_objective(title: 'str', description: 'str' = '', priority: 'str' = 'medium', application: 'str' = 'system') -> 'StrategicObjective'`
- `list_journal() -> 'List[Dict[str, Any]]'`
- `list_notifications(unread_only: 'bool' = False) -> 'List[Dict[str, Any]]'`
- `list_objectives(status: 'str | None' = None) -> 'List[Dict[str, Any]]'`
- `overview(runtime: 'Any') -> 'Dict[str, Any]'`
- `stats() -> 'Dict[str, Any]'`
