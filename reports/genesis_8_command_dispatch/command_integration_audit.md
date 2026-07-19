# Genesis 8 Command Integration Audit

## Objective

Map the existing command façade, registry, manager, and runtime call sites
before wiring the Genesis 8 dispatcher behind the stable `CommandBus` API.

## command_bus

- Path: `aletheus/runtime/commands/command_bus.py`
- Exists: **True**
- Lines: **326**

### Imports

- `from __future__ import annotations`
- `from typing import Any, Callable`
- `from aletheus.runtime.commands_v2.registry import RuntimeCommandRegistry`
- `from aletheus.runtime.context import RuntimeContext`
- `from runtime_commands import RuntimeCommands`

### Classes

#### `CommandBus(object)`

Methods:

- `def __init__(self, runtime: Any, registry: BinOp(left=Name(id='RuntimeCommandRegistry', ctx=Load()), op=BitOr(), right=Constant(value=None)) = None) -> Constant(value=None)`
- `def _register_builtin_runtime_commands(self) -> Constant(value=None)`
- `def register_context_handler(self, name: str, handler: Callable, *, replace: bool = False) -> Callable`
- `def register(self, name: str, handler: Callable, category: str = 'general', description: str = '', metadata: BinOp(left=Subscript(value=Name(id='dict', ctx=Load()), slice=Tuple(elts=[Name(id='str', ctx=Load()), Name(id='Any', ctx=Load())], ctx=Load()), ctx=Load()), op=BitOr(), right=Constant(value=None)) = None, *, replace: bool = False)`
- `def unregister(self, name: str) -> bool`
- `def dispatch(self, command: str, payload: BinOp(left=Subscript(value=Name(id='dict', ctx=Load()), slice=Tuple(elts=[Name(id='str', ctx=Load()), Name(id='Any', ctx=Load())], ctx=Load()), ctx=Load()), op=BitOr(), right=Constant(value=None)) = None, application: str = 'system') -> RuntimeContext`
- `def execute(self, command: str, payload: BinOp(left=Subscript(value=Name(id='dict', ctx=Load()), slice=Tuple(elts=[Name(id='str', ctx=Load()), Name(id='Any', ctx=Load())], ctx=Load()), ctx=Load()), op=BitOr(), right=Constant(value=None)) = None, application: str = 'system') -> RuntimeContext`
- `def _extract_error(response: Any, *, fallback: str) -> str`
- `def has(self, command: str) -> bool`
- `def count(self) -> int`
- `def list(self) -> list`
- `def categories(self) -> list`
- `def health(self) -> dict`

### Top-level functions

- None

## command_package

- Path: `aletheus/runtime/commands/__init__.py`
- Exists: **True**
- Lines: **39**

### Imports

- `from command_bus import CommandBus`
- `from contracts import CommandContext, CommandHandler, CommandMiddleware, CommandRequest, CommandResult`
- `from errors import CommandDispatchError, CommandExecutionError, CommandNotFoundError, CommandResultTypeError, CommandValidationError, DuplicateCommandError, RegistryFrozenError`
- `from models import CompiledCommand`
- `from registry import CompiledCommandRegistry`
- `from dispatcher import CommandDispatcher`

### Classes

- None

### Top-level functions

- None

## registry

- Path: `aletheus/runtime/commands_v2/registry.py`
- Exists: **True**
- Lines: **140**

### Imports

- `from __future__ import annotations`
- `from typing import Any, Callable`
- `from models import CommandRecord, CommandResult`

### Classes

#### `RuntimeCommandRegistry(object)`

Methods:

- `def __init__(self) -> Constant(value=None)`
- `def register(self, name: str, handler: Callable, category: str = 'general', description: str = '', metadata: BinOp(left=Subscript(value=Name(id='dict', ctx=Load()), slice=Tuple(elts=[Name(id='str', ctx=Load()), Name(id='Any', ctx=Load())], ctx=Load()), ctx=Load()), op=BitOr(), right=Constant(value=None)) = None, *, replace: bool = False) -> CommandRecord`
- `def unregister(self, name: str) -> bool`
- `def has(self, name: str) -> bool`
- `def get(self, name: str)`
- `def dispatch(self, name: str, payload = None)`
- `def count(self)`
- `def list(self)`
- `def categories(self)`
- `def health(self)`

### Top-level functions

- None

## command_manager

- Path: `aletheus/runtime/managers/command_manager.py`
- Exists: **True**
- Lines: **53**

### Imports

- `from aletheus.runtime.command_bootstrap.bootstrapper import RuntimeCommandBootstrapper`

### Classes

#### `CommandManager(object)`

Methods:

- `def __init__(self, runtime)`
- `def bootstrap(self)`
- `def count(self)`
- `def list(self)`
- `def status(self)`

### Top-level functions

- None

## runtime_core

- Path: `aletheus/runtime/core.py`
- Exists: **True**
- Lines: **1384**

### Imports

- `from __future__ import annotations`
- `from aletheus.runtime.governance.architecture_rules import ArchitectureGovernanceRules`
- `from aletheus.runtime.governance.registry_rules import RegistryGovernanceRules`
- `from aletheus.runtime.governance.history import GovernanceHistory`
- `from aletheus.runtime.registry.runtime_registry import runtime_registry`
- `from aletheus.runtime.registry.compatibility import RegistryCompatibility`
- `from aletheus.runtime.certification.boot_certification import BootCertification`
- `from aletheus.runtime.readiness.snapshot import RuntimeReadinessSnapshot`
- `from aletheus.runtime.release.genesis6_report import Genesis6CertificationReport`
- `from aletheus.runtime.release.genesis6_review import Genesis6FreezeReview`
- `from aletheus.runtime.release.genesis6_validator import Genesis6Validator`
- `from aletheus.runtime.architecture.validator import ArchitectureValidator`
- `from aletheus.runtime.audit.command_surface import CommandSurfaceAuditor`
- `from aletheus.runtime.intelligence.spa_bridge import RuntimeSPABridge`
- `from typing import Any`
- `from aletheus.memory import memory_core`
- `from aletheus.cognition import cognition_core`
- `from aletheus.knowledge import knowledge_core`
- `from aletheus.mission import mission_core`
- `from aletheus.workspace import workspace_core`
- `from aletheus.applications import application_core`
- `from aletheus.release import release_core`
- `from aletheus.semantic import semantic_core`
- `from aletheus.executive import executive_core`
- `from aletheus.agents import agent_core`
- `from aletheus.planning import planning_core`
- `from aletheus.copilot import copilot_core`
- `from aletheus.intelligence import intelligence_core`
- `from aletheus.prediction import prediction_core`
- `from aletheus.learning import learning_core`
- `from aletheus.kernel_v2 import kernel_core`
- `from aletheus.missions_v2 import mission_v2_core`
- `from aletheus.workflows_v2 import workflow_v2_core`
- `from aletheus.enterprise import enterprise_core`
- `from aletheus.memory_mesh import memory_mesh_core`
- `from aletheus.knowledge_graph import knowledge_graph_core`
- `from aletheus.reasoning import reasoning_core`
- `from aletheus.decision_v2 import decision_core`
- `from aletheus.agents_v2 import agent_core`
- `from aletheus.workflow_v3 import workflow_core`
- `from aletheus.planning_v2 import planning_core`
- `from aletheus.distributed_v3 import distributed_v3_core`
- `from aletheus.plugins_v3 import plugin_core`
- `from aletheus.persistence_v3 import persistence_core`
- `from aletheus.event_bus_v3 import event_bus_core`
- `from aletheus.federation_v3 import federation_core`
- `from aletheus.telemetry_v3 import telemetry_core`
- `from aletheus.high_availability_v3 import high_availability_core`
- `from aletheus.security_v3 import security_core`
- `from aletheus.tenancy_v3 import tenancy_core`
- `from aletheus.runtime.kernel import intelligence_orchestrator, intelligence_scheduler, intelligence_dispatcher, intelligence_supervisor, KernelExecutor`
- `from aletheus.plugins.runtime_plugin_manager import RuntimePluginManager`
- `from aletheus.runtime.commands import CommandBus`
- `from aletheus.runtime.context import RuntimeContext`
- `from aletheus.runtime.compat import compatibility_registry`
- `from aletheus.runtime.diagnostics import RuntimeDiagnostics`
- `from aletheus.runtime.events import EventBus`
- `from aletheus.runtime.job_queue import JobQueue`
- `from aletheus.runtime.metrics import RuntimeMetrics`
- `from aletheus.runtime.pipeline import Pipeline, PipelineExecutor`
- `from aletheus.runtime.registries import EngineRegistry`
- `from aletheus.runtime.scheduler import Scheduler`
- `from aletheus.runtime.workflow import WorkflowExecutor, WorkflowGraph`
- `from aletheus.runtime.hardening import RuntimeHardening`
- `from aletheus.runtime.integrity import RuntimeDoctor`
- `from aletheus.runtime.governance import GovernanceEngine, PrincipleXValidator`
- `from aletheus.runtime.services import ServiceRegistry`
- `from aletheus.runtime.integrity import RuntimeInvariantEngine, RuntimeBootValidator`
- `from aletheus.runtime.command_bootstrap.bootstrapper import RuntimeCommandBootstrapper`
- `from aletheus.runtime.managers import CertificationManager, SnapshotManager, InvariantManager, HealthManager, ValidationManager, RegistryManager, CommandManager, GovernanceManager`
- `from aletheus.runtime.managers.runtime_facade import RuntimeFacade`
- `from aletheus.runtime.adapters.graph_adapter import GraphCommandAdapter`
- `from aletheus.runtime.adapters.mission_adapter import MissionCommandAdapter`
- `from aletheus.runtime.adapters.event_adapter import EventCommandAdapter`
- `from aletheus.runtime.adapters.runtime_adapter import RuntimeCommandAdapter`
- `from aletheus.runtime.adapters.compatibility_adapter import CompatibilityCommandAdapter`
- `from aletheus.runtime.anchors.registry import AnchorRegistry`
- `from aletheus.runtime.anchors import AnchorRegistry, AnchorLifecycleController, AnchorDependencyGraph, AnchorGovernanceCouncil, IntelligenceAnchorCircuit, MemoryAnchorCircuit, KnowledgeAnchorCircuit, ApplicationAnchorCircuit`

### Classes

#### `AletheusRuntime(object)`

Methods:

- `def __init__(self) -> Constant(value=None)`
- `def boot(self) -> Constant(value=None)`
- `def register_engine(self, name: str, handler: Any) -> Constant(value=None)`
- `def register_service(self, name: str, service: Any) -> Constant(value=None)`
- `def register_pipeline(self, pipeline: Pipeline) -> Constant(value=None)`
- `def register_workflow(self, workflow: WorkflowGraph) -> Constant(value=None)`
- `def bootstrap_registry(self)`
- `def _cmd_goal_create(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_goal_complete(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_goal_list(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_reason_history(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_decision_record(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_decision_history(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_cognition_stats(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_event_bootstrap(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_event_publish(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_event_subscribe(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_event_unsubscribe(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_event_history(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_event_replay(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_event_statistics(self, context: RuntimeContext) -> RuntimeContext`
- `def _bootstrap_compatibility(self)`
- `def _register_compatibility_services(self)`
- `def _apply_compatibility_aliases(self)`
- `def _cmd_registry_inspect(self, context)`
- `def _register_runtime_domains(self)`
- `def _bootstrap_runtime_registry(self)`
- `def _cmd_runtime_selftest(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_runtime_dashboard(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_runtime_snapshot(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_runtime_audit(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_runtime_docs(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_runtime_doctor(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_runtime_invariants(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_runtime_boot_validate(self, context: RuntimeContext) -> RuntimeContext`
- `def _cmd_runtime_health_report(self, context: RuntimeContext) -> RuntimeContext`
- `def _job_runtime_pulse(self) -> dict`
- `def health(self)`
- `def genesis6_validate(self)`
- `def genesis6_freeze_review(self)`
- `def boot_certification_validate(self)`
- `def governance_record(self, event_type, payload)`
- `def registry_snapshot(self)`
- `def _cmd_spa_assess(self, context)`
- `def _cmd_spa_drift(self, context)`
- `def _cmd_architecture_governance_check(self, context)`
- `def _cmd_architecture_validate(self, context)`
- `def _cmd_runtime_audit(self, context)`
- `def command_surface_audit(self)`
- `def anchor_governance_status(self)`
- `def anchor_lifecycle_status(self)`
- `def anchor_dependency_status(self)`
- `def anchor_contract_status(self)`
- `def anchor_discovery_status(self)`
- `def anchor_healing_status(self)`
- `def anchor_intelligence_status(self)`
- `def anchor_optimization_status(self)`
- `def anchor_learning_status(self)`
- `def anchor_predictive_status(self)`
- `def anchor_constitution_status(self)`
- `def anchor_simulation_status(self)`
- `def anchor_research_status(self)`
- `def anchor_proposal_status(self)`
- `def anchor_negotiation_status(self)`
- `def anchor_execution_status(self)`
- `def anchor_verification_status(self)`
- `def anchor_evolution_graph_status(self)`
- `def anchor_analytics_status(self)`
- `def anchor_strategy_status(self)`
- `def anchor_portfolio_status(self)`
- `def anchor_resource_status(self)`
- `def anchor_performance_status(self)`
- `def anchor_improvement_status(self)`
- `def anchor_architect_status(self)`
- `def anchor_architecture_simulator_status(self)`
- `def anchor_architecture_selection_status(self)`
- `def anchor_deployment_status(self)`
- `def anchor_migration_status(self)`
- `def anchor_continuity_status(self)`
- `def anchor_institutional_memory_status(self)`
- `def anchor_pattern_status(self)`
- `def anchor_forecasting_status(self)`
- `def anchor_steward_status(self)`
- `def anchor_constitution_reasoning_status(self)`
- `def anchor_council_status(self)`
- `def anchor_consensus_status(self)`
- `def anchor_judgment_status(self)`
- `def anchor_meta_reasoning_status(self)`
- `def anchor_cognitive_status(self)`
- `def anchor_cognitive_optimization_status(self)`
- `def anchor_cognitive_self_improvement_status(self)`
- `def anchor_cognitive_architect_status(self)`
- `def anchor_cognitive_simulation_status(self)`
- `def anchor_cognitive_selection_status(self)`

#### `RuntimeContext(object)`

Methods:

- `def __init__(self)`
- `def add_result(self, key, value)`

#### `RuntimeContext(object)`

Methods:

- `def __init__(self)`
- `def add_result(self, key, value)`

### Top-level functions

- None

## Command References

### `aletheus/agents/economy/engine.py`

- L58: `self.identity.register(agent),`

### `aletheus/aos_search/core.py`

- L28: `results = self.router.execute(`

### `aletheus/aos_search/providers.py`

- L67: `self.register(`

### `aletheus/boot_runtime/core.py`

- L17: `return self.executor.execute(plan)`

### `aletheus/canonical_identity/core.py`

- L66: `canonical_identity_registry.register(identity)`

### `aletheus/capabilities/host.py`

- L37: `capability.register(runtime)`
- L102: `return capability.execute(request)`

### `aletheus/capability_engine/profiles.py`

- L24: `self.register(`
- L32: `self.register(`
- L41: `self.register(`
- L50: `self.register(`
- L59: `self.register(`
- L68: `self.register(`
- L77: `self.register(`
- L86: `self.register(`

### `aletheus/collectible_automation/engine.py`

- L36: `return self.runtime.execute(`

### `aletheus/concept_collision_engine/registry.py`

- L26: `self.register(concept)`

### `aletheus/concept_collision_engine/service.py`

- L35: `self.registry.register(concept)`

### `aletheus/constitutional_library/core.py`

- L85: `constitutional_library_registry.register(`

### `aletheus/constitutional_policy/core.py`

- L43: `self.registry.register(policy)`

### `aletheus/copilot/copilot_core.py`

- L27: `summary = runtime.commands.dispatch("executive.summary", {}).results.get("summary", {})`
- L28: `recommendations = runtime.commands.dispatch("executive.recommendations", {}).results.get("recommendations", [])`
- L29: `risks = runtime.commands.dispatch("executive.risks", {}).results.get("risks", [])`
- L44: `result = runtime.commands.dispatch("executive.summary", {})`
- L49: `result = runtime.commands.dispatch(`
- L57: `result = runtime.commands.dispatch("executive.recommendations", {})`
- L62: `result = runtime.commands.dispatch("executive.system_report", {})`
- L67: `result = runtime.commands.dispatch("workspace.overview", {})`
- L81: `health = runtime.commands.dispatch("runtime.health", {}).results.get("health", {})`
- L118: `events = runtime.commands.dispatch("runtime.events", {}).results.get("events", [])`
- L119: `memory = runtime.commands.dispatch("memory.recall", {"limit": 20}).results.get("memory", [])`

### `aletheus/council_registry/core.py`

- L93: `self.registry.register(member)`

### `aletheus/decision_v2/decision_core.py`

- L147: `reasoning = runtime.commands.dispatch(`
- L188: `decision.execute()`

### `aletheus/double_hedron/core.py`

- L77: `double_hedron_registry.register(memory)`

### `aletheus/engine_registry/core.py`

- L29: `self.registry.register(`

### `aletheus/execution_engine/core.py`

- L94: `search = aos_search.execute(query)`

### `aletheus/executive/executive_core.py`

- L16: `health = runtime.commands.dispatch("runtime.health").results.get("health", {})`
- L17: `diagnostics = runtime.commands.dispatch("runtime.diagnostics").results`

### `aletheus/executive_kernel/bootstrap.py`

- L32: `self.composition_engine.register(`
- L40: `self.composition_engine.register(`
- L48: `self.composition_engine.register(`
- L56: `self.composition_engine.register(`
- L64: `self.composition_engine.register(`
- L81: `self.composition_engine.register(`
- L98: `self.composition_engine.register(`

### `aletheus/executive_kernel/kernel.py`

- L87: `self.kernel_registry.register(descriptor)`
- L102: `self.capability_registry.register(descriptor)`
- L120: `self.policy_registry.register(descriptor)`

### `aletheus/foundation/core.py`

- L93: `self.registry.register(engine)`

### `aletheus/foundation_service_bus/registry.py`

- L116: `self.register(capability)`

### `aletheus/identity_engine/core.py`

- L44: `self.registry.register(founder)`

### `aletheus/intelligence/evolution/IntelligenceEvolutionAccelerator.py`

- L31: `return self.execute(`

### `aletheus/intelligence/evolution/MetaReasoningEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/evolution/ReflectionEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/intelligence_core.py`

- L15: `diagnostics = runtime.commands.dispatch("runtime.diagnostics", {}).results`
- L16: `health = runtime.commands.dispatch("runtime.health", {}).results.get("health", {})`
- L139: `"runtime_health": runtime.commands.dispatch("runtime.health", {}).results.get("health", {}),`

### `aletheus/intelligence/knowledge/KnowledgeDiscoveryEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/knowledge/KnowledgeEvolutionEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/knowledge/KnowledgeGraphEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/knowledge/KnowledgeLineageEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/learning/AdaptationEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/learning/ContinuousLearningEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/learning/SkillAcquisitionEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/memory/EpisodicMemoryEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/memory/LongTermMemoryEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/memory/MemoryConsolidationEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/memory/SemanticMemoryEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/memory/ShortTermMemoryEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/perception/ContextAwarenessEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/perception/PerceptionIntelligenceEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/perception/SignalDetectionEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/prediction/FutureModelingEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/prediction/PredictiveIntelligenceEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/prediction/ScenarioSimulationEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/reasoning/AdvancedReasoningEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/reasoning/HypothesisEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/reasoning/IntelligenceSynthesisEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/reasoning/LogicalInferenceEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/reasoning/ProblemDecompositionEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/strategy/DecisionIntelligenceEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/strategy/GoalFormationEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/strategy/OpportunityDetectionEngine.py`

- L31: `return self.execute(`

### `aletheus/intelligence/strategy/StrategicPlanningEngine.py`

- L31: `return self.execute(`

### `aletheus/intent_registry/bootstrap.py`

- L8: `registry.register(IntentRecord(`
- L17: `registry.register(IntentRecord(`
- L27: `registry.register(IntentRecord(`

### `aletheus/kernel_v2/kernel_core.py`

- L16: `health = runtime.commands.dispatch("runtime.health", {}).results.get("health", {})`
- L73: `diagnostics = runtime.commands.dispatch("runtime.diagnostics", {}).results`
- L74: `health = runtime.commands.dispatch("runtime.health", {}).results.get("health", {})`
- L77: `self.register(`
- L84: `apps = runtime.commands.dispatch("application.list", {}).results.get("applications", [])`
- L86: `self.register(`
- L93: `agents = runtime.commands.dispatch("agent.list", {}).results.get("agents", [])`
- L95: `self.register(`

### `aletheus/learning/learning_core.py`

- L115: `health = runtime.commands.dispatch("runtime.health", {}).results.get("health", {})`

### `aletheus/marketplace_intelligence/runtime/runtime.py`

- L40: `self.registry.register(`

### `aletheus/missions_v2/mission_core.py`

- L130: `plan = runtime.commands.dispatch(`
- L164: `assignment = runtime.commands.dispatch(`
- L179: `agent_run = runtime.commands.dispatch(`
- L225: `learning = runtime.commands.dispatch(`

### `aletheus/module_registry/engine.py`

- L62: `self.registry.register(`

### `aletheus/neural/envelope/bootstrap.py`

- L39: `self.brain.cortex.register(`
- L73: `self.brain.neurons.register(`
- L98: `self.brain.synapses.register(`

### `aletheus/neural/envelope/core.py`

- L104: `return self.neurons.register(`
- L124: `return self.synapses.register(`

### `aletheus/orchestrator/registry_service.py`

- L14: `return self.registry.register(component)`

### `aletheus/overlay_manager/core.py`

- L35: `registered = self.registry.register(definition)`
- L146: `self.register(definition)`

### `aletheus/planning/planning_core.py`

- L85: `assignment = runtime.commands.dispatch(`
- L99: `run = runtime.commands.dispatch(`

### `aletheus/planning_v2/planning_core.py`

- L180: `plan.execute()`

### `aletheus/platform_events/core.py`

- L29: `dispatch_result = platform_subscriptions.dispatch(event_dict)`

### `aletheus/platform_lifecycle/core.py`

- L39: `report = boot_runtime.execute(plan)`

### `aletheus/platform_subscriptions/core.py`

- L22: `return self.registry.register(`

### `aletheus/platform_verification/bootstrap.py`

- L15: `registry.register(compile_check)`
- L16: `registry.register(unit_test_check)`
- L17: `registry.register(repository_dna_check)`
- L18: `registry.register(runtime_boot_check)`
- L19: `registry.register(capability_check)`

### `aletheus/reason_engine/core.py`

- L133: `reason_registry.register(reason)`

### `aletheus/reasoning/reasoning_core.py`

- L67: `graph_ctx = runtime.commands.dispatch("knowledge.search", {"query": question})`
- L68: `memory_ctx = runtime.commands.dispatch("memory.mesh.search", {"query": question})`
- L69: `infer_ctx = runtime.commands.dispatch("knowledge.infer", {})`

### `aletheus/release/core.py`

- L64: `health = runtime.commands.dispatch("runtime.health").results.get("health", {})`
- L65: `diagnostics = runtime.commands.dispatch("runtime.diagnostics").results`

### `aletheus/runtime/adapter.py`

- L246: `result = commands.execute(`
- L260: `result = commands.dispatch(`

### `aletheus/runtime/adapters/__init__.py`

- L7: `CommandBus and runtime capabilities.`

### `aletheus/runtime/boot_phases/scheduler.py`

- L10: `runtime.scheduler.register(`

### `aletheus/runtime/boot_phases/service_groups/ai_platform.py`

- L5: `runtime.services.register(`
- L13: `runtime.services.register(`
- L21: `runtime.services.register(`
- L29: `runtime.services.register(`

### `aletheus/runtime/boot_phases/service_groups/core.py`

- L4: `runtime.services.register(`
- L9: `runtime.services.register(`
- L14: `runtime.services.register(`
- L19: `runtime.services.register(`

### `aletheus/runtime/boot_phases/service_groups/foundation.py`

- L4: `runtime.services.register(`
- L9: `runtime.services.register(`
- L14: `runtime.services.register(`
- L19: `runtime.services.register(`

### `aletheus/runtime/boot_phases/service_groups/intelligence.py`

- L4: `runtime.services.register(`
- L9: `runtime.services.register(`
- L14: `runtime.services.register(`
- L19: `runtime.services.register(`

### `aletheus/runtime/boot_phases/service_registration.py`

- L27: `registered += registrar.register(runtime)`

### `aletheus/runtime/capabilities/synchronizer.py`

- L21: `registry.register(`

### `aletheus/runtime/commands/__init__.py`

- L1: `from .command_bus import CommandBus`
- L23: `"CommandBus",`

### `aletheus/runtime/commands/command_bus.py`

- L6: `CommandBus preserves the stable runtime command interface while delegating:`
- L8: `- registration and low-level routing to RuntimeCommandRegistry`
- L10: `- lifecycle/bootstrap ownership to CommandManager`
- L18: `RuntimeCommandRegistry,`
- L25: `class CommandBus:`
- L29: `CommandBus is intentionally a thin façade. It coordinates command`
- L36: `registry: RuntimeCommandRegistry | None = None,`
- L39: `self.registry = registry or RuntimeCommandRegistry()`
- L66: `self.register_context_handler(`
- L72: `def register_context_handler(`
- L121: `return self.registry.register(`
- L156: `payload handlers are dispatched through RuntimeCommandRegistry and`
- L200: `result = self.registry.dispatch(`
- L253: `return self.dispatch(`
- L325: `"CommandBus",`

### `aletheus/runtime/commands/tests/test_dispatcher.py`

- L67: `result = await dispatcher.dispatch("math.add", AddRequest(2, 3))`
- L78: `result = await dispatcher.dispatch("math.sum", AddRequest(4, 6))`
- L94: `await dispatcher.dispatch("math.add", AddRequest(1, 1))`
- L111: `await dispatcher.dispatch("math.add", object())`
- L130: `await dispatcher.dispatch("math.bad", AddRequest(1, 2))`
- L138: `await dispatcher.dispatch("missing.command", AddRequest(1, 2))`

### `aletheus/runtime/commands_v2/__init__.py`

- L2: `from .registry import RuntimeCommandRegistry`
- L3: `from .reporter import RuntimeCommandRegistryReporter`
- L8: `"RuntimeCommandRegistry",`
- L9: `"RuntimeCommandRegistryReporter",`

### `aletheus/runtime/commands_v2/registry.py`

- L14: `class RuntimeCommandRegistry:`
- L139: `"RuntimeCommandRegistry",`

### `aletheus/runtime/commands_v2/reporter.py`

- L1: `class RuntimeCommandRegistryReporter:`

### `aletheus/runtime/compatibility_layer/layer.py`

- L67: `self.registry.register(`

### `aletheus/runtime/convergence/engine.py`

- L35: `self.registry.register(`
- L44: `self.apps.register(`

### `aletheus/runtime/core.py`

- L67: `from aletheus.runtime.commands import CommandBus`
- L102: `CommandManager,`
- L147: `self.commands = CommandBus(self)`
- L181: `self.anchor_registry.register(`
- L186: `self.anchor_registry.register(`
- L191: `self.anchor_registry.register(`
- L196: `self.anchor_registry.register(`
- L217: `self.command_manager = CommandManager(self)`
- L339: `RuntimeServiceProvider().register(self)`
- L356: `self.engines.register(name, handler)`
- L361: `self.services.register(`
- L371: `self.pipelines.register(pipeline)`
- L375: `self.workflows.register(workflow)`
- L932: `Delegated to CommandManager.`

### `aletheus/runtime/core_bridge/lifecycle.py`

- L30: `boot_report = boot_pipeline.execute()`

### `aletheus/runtime/domains/decision.py`

- L47: `result = self.runtime.decision.execute(`

### `aletheus/runtime/domains/kernel.py`

- L15: `return self.runtime.intelligence_orchestrator.execute(`
- L36: `dispatched = self.runtime.intelligence_dispatcher.dispatch(`

### `aletheus/runtime/domains/mission.py`

- L17: `return self.runtime.missions_v2.execute(`

### `aletheus/runtime/job_queue.py`

- L26: `context = self.runtime.commands.dispatch(job.command, job.payload, application=job.application)`

### `aletheus/runtime/kernel/dispatcher.py`

- L10: `return runtime.commands.dispatch(command, payload or {})`

### `aletheus/runtime/kernel/executor.py`

- L22: `return self.runtime.intelligence_orchestrator.execute(`

### `aletheus/runtime/kernel/orchestrator.py`

- L80: `context = runtime.commands.dispatch(`

### `aletheus/runtime/managers/__init__.py`

- L8: `from .command_manager import CommandManager`
- L20: `"CommandManager",`

### `aletheus/runtime/managers/command_manager.py`

- L14: `class CommandManager:`

### `aletheus/runtime/orchestration/orchestrator.py`

- L40: `self.service_provider.register(runtime)`

### `aletheus/runtime/providers/service_provider.py`

- L10: `runtime.services.register("commands", runtime.commands)`
- L11: `runtime.services.register("events", runtime.events)`
- L12: `runtime.services.register("metrics", runtime.metrics)`
- L13: `runtime.services.register("compatibility", runtime.compat)`
- L14: `runtime.services.register("kernel", runtime.kernel)`
- L15: `runtime.services.register("governance", runtime.governance)`
- L16: `runtime.services.register("doctor", runtime.runtime_doctor)`
- L17: `runtime.services.register(`
- L21: `runtime.services.register(`

### `aletheus/runtime/registrations/agent_commands.py`

- L14: `commands.register(`
- L19: `commands.register(`
- L24: `commands.register(`
- L29: `commands.register(`
- L34: `commands.register(`
- L39: `commands.register(`
- L44: `commands.register(`
- L49: `commands.register(`
- L54: `commands.register(`

### `aletheus/runtime/registrations/application_commands.py`

- L12: `commands.register(`
- L17: `commands.register(`
- L22: `commands.register(`
- L27: `commands.register(`
- L32: `commands.register(`
- L37: `commands.register(`
- L42: `commands.register(`
- L47: `commands.register(`
- L52: `commands.register(`
- L57: `commands.register(`
- L62: `commands.register(`
- L67: `commands.register(`

### `aletheus/runtime/registrations/architecture_commands.py`

- L10: `runtime.commands.register(`

### `aletheus/runtime/registrations/cluster_commands.py`

- L14: `commands.register("cluster.join", domain.join)`
- L15: `commands.register("cluster.leave", domain.leave)`
- L16: `commands.register("cluster.nodes", domain.nodes)`
- L17: `commands.register("cluster.services", domain.services)`
- L18: `commands.register("cluster.heartbeat", domain.heartbeat)`
- L19: `commands.register("cluster.elect_leader", domain.elect_leader)`
- L20: `commands.register("cluster.statistics", domain.statistics)`

### `aletheus/runtime/registrations/compatibility_commands.py`

- L15: `commands.register(`
- L21: `commands.register(`
- L27: `commands.register(`
- L33: `commands.register(`

### `aletheus/runtime/registrations/copilot_commands.py`

- L19: `runtime.commands.register(`
- L24: `runtime.commands.register(`
- L29: `runtime.commands.register(`
- L34: `runtime.commands.register(`
- L39: `runtime.commands.register(`
- L44: `runtime.commands.register(`

### `aletheus/runtime/registrations/decision_commands.py`

- L15: `runtime.commands.register(`
- L20: `runtime.commands.register(`
- L25: `runtime.commands.register(`
- L30: `runtime.commands.register(`
- L35: `runtime.commands.register(`
- L40: `runtime.commands.register(`
- L45: `runtime.commands.register(`
- L50: `runtime.commands.register(`

### `aletheus/runtime/registrations/enterprise_commands.py`

- L15: `commands.register(`
- L20: `commands.register(`
- L25: `commands.register(`
- L30: `commands.register(`
- L35: `commands.register(`
- L40: `commands.register(`
- L45: `commands.register(`
- L50: `commands.register(`
- L55: `commands.register(`

### `aletheus/runtime/registrations/event_commands.py`

- L15: `commands.register(`
- L21: `commands.register(`
- L27: `commands.register(`
- L33: `commands.register(`
- L39: `commands.register(`
- L45: `commands.register(`
- L51: `commands.register(`

### `aletheus/runtime/registrations/executive_commands.py`

- L12: `commands.register(`
- L17: `commands.register(`
- L22: `commands.register(`
- L27: `commands.register(`
- L32: `commands.register(`
- L37: `commands.register(`
- L42: `commands.register(`

### `aletheus/runtime/registrations/federation_commands.py`

- L13: `commands.register("federation.bootstrap", domain.bootstrap)`
- L14: `commands.register("federation.join", domain.join)`
- L15: `commands.register("federation.leave", domain.leave)`
- L16: `commands.register("federation.discover", domain.discover)`
- L17: `commands.register("federation.query", domain.query)`
- L18: `commands.register("federation.broadcast", domain.broadcast)`
- L19: `commands.register("federation.statistics", domain.statistics)`

### `aletheus/runtime/registrations/governance_architecture_commands.py`

- L10: `runtime.commands.register(`

### `aletheus/runtime/registrations/governance_commands.py`

- L12: `commands.register(`
- L17: `commands.register(`
- L22: `commands.register(`
- L27: `commands.register(`

### `aletheus/runtime/registrations/graph_commands.py`

- L14: `commands.register(`
- L19: `commands.register(`
- L24: `commands.register(`
- L29: `commands.register(`
- L34: `commands.register(`
- L39: `commands.register(`
- L44: `commands.register(`

### `aletheus/runtime/registrations/ha_commands.py`

- L13: `commands.register("ha.bootstrap", domain.bootstrap)`
- L14: `commands.register("ha.join", domain.join)`
- L15: `commands.register("ha.leave", domain.leave)`
- L16: `commands.register("ha.promote", domain.promote)`
- L17: `commands.register("ha.demote", domain.demote)`
- L18: `commands.register("ha.failover", domain.failover)`
- L19: `commands.register("ha.recover", domain.recover)`
- L20: `commands.register("ha.replicate", domain.replicate)`
- L21: `commands.register("ha.status", domain.status)`
- L22: `commands.register("ha.statistics", domain.statistics)`

### `aletheus/runtime/registrations/kernel_commands.py`

- L13: `commands.register("kernel.bootstrap", domain.bootstrap)`
- L14: `commands.register("kernel.execute", domain.execute)`
- L15: `commands.register("kernel.tasks", domain.tasks)`
- L16: `commands.register("kernel.scheduler", domain.scheduler)`
- L17: `commands.register("kernel.dispatcher", domain.dispatcher)`
- L18: `commands.register("kernel.supervisor", domain.supervisor)`
- L19: `commands.register("kernel.statistics", domain.statistics)`

### `aletheus/runtime/registrations/knowledge_graph_commands.py`

- L15: `commands.register(`
- L20: `commands.register(`
- L25: `commands.register(`
- L30: `commands.register(`
- L35: `commands.register(`
- L40: `commands.register(`
- L45: `commands.register(`
- L50: `commands.register(`
- L55: `commands.register(`
- L60: `commands.register(`
- L65: `commands.register(`

### `aletheus/runtime/registrations/learning_commands.py`

- L15: `commands.register(`
- L20: `commands.register(`
- L25: `commands.register(`
- L30: `commands.register(`
- L35: `commands.register(`
- L40: `commands.register(`
- L45: `commands.register(`

### `aletheus/runtime/registrations/memory_commands.py`

- L19: `runtime.commands.register(`
- L24: `runtime.commands.register(`
- L29: `runtime.commands.register(`
- L34: `runtime.commands.register(`

### `aletheus/runtime/registrations/memory_mesh_commands.py`

- L15: `commands.register("memory.mesh.store", domain.store)`
- L16: `commands.register("memory.mesh.retrieve", domain.retrieve)`
- L17: `commands.register("memory.mesh.search", domain.search)`
- L18: `commands.register("memory.mesh.snapshot", domain.snapshot)`
- L19: `commands.register("memory.mesh.restore", domain.restore)`
- L20: `commands.register("memory.mesh.replicate", domain.replicate)`
- L21: `commands.register("memory.mesh.sync", domain.sync)`
- L22: `commands.register("memory.mesh.history", domain.history)`
- L23: `commands.register("memory.mesh.cache", domain.cache)`
- L24: `commands.register("memory.mesh.stats", domain.stats)`

### `aletheus/runtime/registrations/mission_commands.py`

- L15: `commands.register(`
- L21: `commands.register(`
- L27: `commands.register(`
- L33: `commands.register(`
- L39: `commands.register(`
- L45: `commands.register(`
- L51: `commands.register(`
- L57: `commands.register(`

### `aletheus/runtime/registrations/mission_v2_commands.py`

- L13: `commands.register("mission.create", domain.create)`
- L14: `commands.register("mission.list", domain.list)`
- L15: `commands.register("mission.execute", domain.execute)`
- L16: `commands.register("mission.complete", domain.complete)`
- L17: `commands.register("mission.statistics", domain.statistics)`

### `aletheus/runtime/registrations/planning_commands.py`

- L14: `commands.register(`
- L19: `commands.register(`

### `aletheus/runtime/registrations/plugin_commands.py`

- L14: `commands.register(`
- L19: `commands.register(`
- L24: `commands.register(`
- L29: `commands.register(`
- L34: `commands.register(`
- L39: `commands.register(`
- L44: `commands.register(`
- L49: `commands.register(`
- L54: `commands.register(`

### `aletheus/runtime/registrations/prediction_commands.py`

- L15: `commands.register(`
- L20: `commands.register(`
- L25: `commands.register(`
- L30: `commands.register(`
- L35: `commands.register(`
- L40: `commands.register(`
- L45: `commands.register(`

### `aletheus/runtime/registrations/reasoning_commands.py`

- L19: `runtime.commands.register(`
- L24: `runtime.commands.register(`
- L29: `runtime.commands.register(`
- L34: `runtime.commands.register(`
- L39: `runtime.commands.register(`
- L44: `runtime.commands.register(`
- L49: `runtime.commands.register(`
- L54: `runtime.commands.register(`

### `aletheus/runtime/registrations/registry_commands.py`

- L8: `commands.register(`
- L16: `commands.register(`
- L24: `commands.register(`
- L32: `commands.register(`
- L40: `commands.register(`

### `aletheus/runtime/registrations/runtime_commands.py`

- L15: `commands.register(`
- L21: `commands.register(`
- L27: `commands.register(`
- L33: `commands.register(`
- L39: `commands.register(`
- L45: `commands.register(`
- L51: `commands.register(`
- L57: `commands.register(`
- L63: `commands.register(`

### `aletheus/runtime/registrations/security_commands.py`

- L13: `commands.register("security.bootstrap", domain.bootstrap)`
- L14: `commands.register("security.authenticate", domain.authenticate)`
- L15: `commands.register("security.authorize", domain.authorize)`
- L16: `commands.register("security.policy", domain.policy)`
- L17: `commands.register("security.role_create", domain.role_create)`
- L18: `commands.register("security.role_assign", domain.role_assign)`
- L19: `commands.register("security.audit", domain.audit)`
- L20: `commands.register("security.statistics", domain.statistics)`

### `aletheus/runtime/registrations/semantic_commands.py`

- L12: `commands.register(`
- L17: `commands.register(`
- L22: `commands.register(`
- L27: `commands.register(`
- L32: `commands.register(`
- L37: `commands.register(`
- L42: `commands.register(`

### `aletheus/runtime/registrations/state_commands.py`

- L14: `commands.register(`
- L19: `commands.register(`
- L24: `commands.register(`
- L29: `commands.register(`
- L34: `commands.register(`
- L39: `commands.register(`
- L44: `commands.register(`
- L49: `commands.register(`

### `aletheus/runtime/registrations/telemetry_commands.py`

- L13: `commands.register("telemetry.bootstrap", domain.bootstrap)`
- L14: `commands.register("telemetry.record", domain.record)`
- L15: `commands.register("telemetry.metric", domain.metric)`
- L16: `commands.register("telemetry.log", domain.log)`
- L17: `commands.register("telemetry.trace", domain.trace)`
- L18: `commands.register("telemetry.health", domain.health)`
- L19: `commands.register("telemetry.timeline", domain.timeline)`
- L20: `commands.register("telemetry.statistics", domain.statistics)`

### `aletheus/runtime/registrations/tenancy_commands.py`

- L13: `commands.register("tenant.bootstrap", domain.bootstrap)`
- L14: `commands.register("tenant.create", domain.create)`
- L15: `commands.register("tenant.delete", domain.delete)`
- L16: `commands.register("tenant.list", domain.list)`
- L17: `commands.register("tenant.select", domain.select)`
- L19: `commands.register("workspace.create", domain.workspace_create)`
- L20: `commands.register("workspace.delete", domain.workspace_delete)`
- L21: `commands.register("workspace.list", domain.workspace_list)`
- L23: `commands.register("organization.create", domain.organization_create)`
- L24: `commands.register("organization.update", domain.organization_update)`
- L26: `commands.register("tenant.statistics", domain.statistics)`
- L27: `commands.register("tenant.health", domain.health)`

### `aletheus/runtime/registrations/uil_commands.py`

- L12: `commands.register(`
- L17: `commands.register(`
- L22: `commands.register(`
- L27: `commands.register(`
- L32: `commands.register(`
- L37: `commands.register(`
- L42: `commands.register(`
- L47: `commands.register(`

### `aletheus/runtime/registrations/workflow_commands.py`

- L14: `commands.register(`
- L19: `commands.register(`
- L24: `commands.register(`
- L29: `commands.register(`
- L34: `commands.register(`
- L39: `commands.register(`
- L44: `commands.register(`
- L49: `commands.register(`

### `aletheus/runtime/registrations/workflow_v2_commands.py`

- L13: `commands.register("workflow.bootstrap", domain.bootstrap)`
- L14: `commands.register("workflow.create", domain.create)`
- L15: `commands.register("workflow.start", domain.start)`
- L16: `commands.register("workflow.pause", domain.pause)`
- L17: `commands.register("workflow.resume", domain.resume)`
- L18: `commands.register("workflow.cancel", domain.cancel)`
- L19: `commands.register("workflow.status", domain.status)`
- L20: `commands.register("workflow.statistics", domain.statistics)`

### `aletheus/runtime/registrations/workspace_commands.py`

- L12: `commands.register(`
- L17: `commands.register(`
- L22: `commands.register(`
- L27: `commands.register(`
- L32: `commands.register(`
- L37: `commands.register(`
- L42: `commands.register(`
- L47: `commands.register(`

### `aletheus/runtime/relay/network.py`

- L65: `return self.dispatch(packet)`

### `aletheus/runtime/services/registry_federation_registration.py`

- L26: `runtime.services.register(`

### `aletheus/runtime/universal/engine.py`

- L46: `self.registry.register(`

### `aletheus/runtime/workflow.py`

- L33: `result = self.runtime.commands.dispatch(node.command, node.payload, application=application)`

### `aletheus/runtime_engine_manager/core.py`

- L24: `self.lifecycle.register(`

### `aletheus/runtime_supervisor/core.py`

- L34: `recovery = runtime_recovery.execute(decision)`

### `aletheus/sdk/core.py`

- L24: `return execution_engine.execute(`

### `aletheus/sdk/runtime_sdk.py`

- L9: `def dispatch(self, command: str, payload: dict | None = None, application: str = 'system') -> dict: return runtime_core.commands.dispatch(command, payload or {}, application=application).to_dict()`

### `aletheus/self_assembly/core.py`

- L144: `platform_registry.register(`

### `aletheus/service_manager/core.py`

- L34: `return self.registry.register(`

### `aletheus/spa/adaptive_runtime/engine.py`

- L72: `return self.control.execute()`

### `aletheus/spa/optimization/engine.py`

- L83: `return self.loop.execute()`

### `aletheus/workflows_v2/workflow_core.py`

- L159: `context = runtime.commands.dispatch(node.command, node.payload, application=node.application)`
- L175: `assignment = runtime.commands.dispatch(`
- L183: `agent_run = runtime.commands.dispatch("agent.run", {"agent_name": node.assigned_agent})`
- L252: `runtime.commands.dispatch(`

### `aletheus/workspace/workspace_core.py`

- L83: `health = runtime.commands.dispatch("runtime.health").results.get("health", {})`
- L84: `diagnostics = runtime.commands.dispatch("runtime.diagnostics").results`
