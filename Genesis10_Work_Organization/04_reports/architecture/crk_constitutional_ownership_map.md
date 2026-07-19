# CRK Constitutional Ownership Map™

## Purpose

Identify the existing constitutional owner for each responsibility proposed for the Constitutional Runtime Kernel™ before any new kernel implementation is admitted.

## Repository Summary

- Parsed source modules: **3906**
- Concerns evaluated: **9**
- Concerns requiring review: **2**

## Constitutional Ownership Matrix

| Concern | Resolution | Existing Owner or Finding | Permitted CRK Role |
|---|---|---|---|
| **Identity** | `existing_owner` | `aletheus/canonical_identity/models.py` | Require stable, nonblank constitutional identifiers during capability admission. |
| **Ownership** | `review_required` | `Multiple strong owner candidates require constitutional review.` | Enforce unique constitutional ownership during capability admission. |
| **Registration** | `existing_owner` | `aletheus/runtime/core.py` | Apply constitutional admission checks before delegating registration to the existing owner. |
| **Lifecycle** | `existing_owner` | `aletheus/runtime/core.py` | Validate allowed constitutional lifecycle transitions. |
| **Governance** | `existing_owner` | `aletheus/platform_intelligence/constitutional_runtime_council/models.py` | Require governance evidence when admission or mutation policy demands it. |
| **Policy** | `existing_owner` | `aletheus/platform_intelligence/constitutional_policy_engine/exceptions.py` | Evaluate a minimal immutable set of kernel admission invariants. |
| **Evidence** | `review_required` | `Multiple strong owner candidates require constitutional review.` | Require evidence and provenance references where constitutional contracts demand them. |
| **Replay** | `existing_owner` | `aletheus/constitutional_events/registry.py` | Require replay declarations and publish admission events through existing authorities. |
| **Validation** | `existing_owner` | `aletheus/institutional_civilization/readiness.py` | Compose bounded invariant checks and produce typed admission results. |

## Detailed Candidate Analysis

### Identity

**Resolution:** `existing_owner`

**Existing owner or finding:** `aletheus/canonical_identity/models.py`

**Permitted CRK role:** Require stable, nonblank constitutional identifiers during capability admission.

**CRK must never:** Generate domain-specific identifiers or own application entity models.

#### Leading candidates

- `aletheus/canonical_identity/models.py` — score **27**
  - class CanonicalIdentity
  - class IdentityRelationship
  - class IdentityStatus
  - class IdentityType
  - function new_identity_id
- `aletheus/constitutional_ledger/institutional_events.py` — score **17**
  - function new_institutional_event_id
- `aletheus/application_runtime/contracts.py` — score **16**
- `aletheus/application_runtime/core.py` — score **16**
- `aletheus/application_runtime/loader.py` — score **16**
- `aletheus/application_runtime/models.py` — score **16**
- `aletheus/application_runtime/proof_application.py` — score **16**
- `aletheus/application_runtime/registry.py` — score **16**

### Ownership

**Resolution:** `review_required`

**Existing owner or finding:** `Multiple strong owner candidates require constitutional review.`

**Permitted CRK role:** Enforce unique constitutional ownership during capability admission.

**CRK must never:** Replace governance authorities or perform domain authorization.

#### Leading candidates

- `aletheus/institutional_civilization/civilization_registry.py` — score **34**
- `aletheus/institutional_civilization/registry.py` — score **34**
- `aletheus/institutional_civilization/bootstrap.py` — score **26**
- `aletheus/institutional_civilization/canonical_catalog.py` — score **26**
- `aletheus/institutional_civilization/catalog.py` — score **26**
- `aletheus/institutional_civilization/civilization_catalog.py` — score **26**
- `aletheus/institutional_civilization/civilization_models.py` — score **26**
- `aletheus/institutional_civilization/civilization_projection.py` — score **26**

### Registration

**Resolution:** `existing_owner`

**Existing owner or finding:** `aletheus/runtime/core.py`

**Permitted CRK role:** Apply constitutional admission checks before delegating registration to the existing owner.

**CRK must never:** Create a second service, application, runtime, or civilization registry.

#### Leading candidates

- `aletheus/runtime/core.py` — score **40**
  - function _bootstrap_runtime_registry
  - function _cmd_registry_inspect
  - function _register_compatibility_services
  - function _register_runtime_domains
  - function bootstrap_registry
  - function register_engine
  - function register_pipeline
  - function register_service
  - function register_workflow
  - function registry_snapshot
- `aletheus/application_runtime/services.py` — score **36**
  - class ApplicationServiceResolver
  - function resolve
  - function resolve_many
- `aletheus/runtime/services/service_registry.py` — score **34**
  - class ServiceRegistry
  - function register
  - function unregister
- `aletheus/application_runtime/registry.py` — score **33**
  - class ConstitutionalApplicationRegistry
  - function install
- `aletheus/application_runtime/core.py` — score **30**
  - function install
  - function uninstall
- `aletheus/application_runtime/loader.py` — score **30**
  - function install
  - function uninstall
- `aletheus/application_runtime/runtime.py` — score **30**
  - function install
  - function uninstall
- `aletheus/platform/application_runtime.py` — score **30**
  - function install
  - function register

### Lifecycle

**Resolution:** `existing_owner`

**Existing owner or finding:** `aletheus/runtime/core.py`

**Permitted CRK role:** Validate allowed constitutional lifecycle transitions.

**CRK must never:** Execute lifecycle operations already owned by runtime and application managers.

#### Leading candidates

- `aletheus/runtime/core.py` — score **145**
  - function anchor_analytics_status
  - function anchor_architect_status
  - function anchor_architecture_selection_status
  - function anchor_architecture_simulator_status
  - function anchor_cognitive_architect_status
  - function anchor_cognitive_optimization_status
  - function anchor_cognitive_selection_status
  - function anchor_cognitive_self_improvement_status
  - function anchor_cognitive_simulation_status
  - function anchor_cognitive_status
  - function anchor_consensus_status
  - function anchor_constitution_reasoning_status
  - function anchor_constitution_status
  - function anchor_continuity_status
  - function anchor_contract_status
  - function anchor_council_status
  - function anchor_dependency_status
  - function anchor_deployment_status
  - function anchor_discovery_status
  - function anchor_evolution_graph_status
  - function anchor_execution_status
  - function anchor_forecasting_status
  - function anchor_governance_status
  - function anchor_healing_status
  - function anchor_improvement_status
  - function anchor_institutional_memory_status
  - function anchor_intelligence_status
  - function anchor_judgment_status
  - function anchor_learning_status
  - function anchor_lifecycle_status
  - function anchor_meta_reasoning_status
  - function anchor_migration_status
  - function anchor_negotiation_status
  - function anchor_optimization_status
  - function anchor_pattern_status
  - function anchor_performance_status
  - function anchor_portfolio_status
  - function anchor_predictive_status
  - function anchor_proposal_status
  - function anchor_research_status
  - function anchor_resource_status
  - function anchor_simulation_status
  - function anchor_steward_status
  - function anchor_strategy_status
  - function anchor_verification_status
- `aletheus/application_runtime/contracts.py` — score **33**
  - function initialize
  - function start
  - function stop
- `aletheus/application_runtime/core.py` — score **33**
  - function restart
  - function start
  - function stop
- `aletheus/application_runtime/loader.py` — score **33**
  - function restart
  - function start
  - function stop
- `aletheus/application_runtime/proof_application.py` — score **33**
  - function initialize
  - function start
  - function stop
- `aletheus/application_runtime/runtime.py` — score **33**
  - function initialize
  - function start
  - function stop
- `aletheus/platform/application_runtime.py` — score **33**
  - function restart
  - function start
  - function stop
- `aletheus/application_runtime/models.py` — score **30**
  - class ApplicationStatus

### Governance

**Resolution:** `existing_owner`

**Existing owner or finding:** `aletheus/platform_intelligence/constitutional_runtime_council/models.py`

**Permitted CRK role:** Require governance evidence when admission or mutation policy demands it.

**CRK must never:** Replace Council, Conclave, cases, missions, security, or existing governance services.

#### Leading candidates

- `aletheus/platform_intelligence/constitutional_runtime_council/models.py` — score **66**
  - class ConstitutionalCouncilMember
  - class CouncilDecision
  - class CouncilDecisionOutcome
  - class CouncilMemberKind
  - class CouncilProposal
  - class CouncilProposalKind
  - class CouncilProposalState
  - class CouncilStatistics
  - class CouncilVote
  - class CouncilVoteChoice
  - class CouncilVotingStrategy
- `aletheus/platform_intelligence/constitutional_runtime_council/exceptions.py` — score **42**
  - class ConstitutionalRuntimeCouncilError
  - class CouncilDecisionError
  - class CouncilMemberAlreadyExistsError
  - class CouncilMemberNotFoundError
  - class CouncilProposalAlreadyExistsError
  - class CouncilProposalNotFoundError
  - class CouncilVotingError
- `aletheus/institutional_civilization/wiring.py` — score **25**
  - function escalate_to_council
- `aletheus/institutional_civilization/bootstrap.py` — score **22**
- `aletheus/institutional_civilization/canonical_catalog.py` — score **22**
- `aletheus/institutional_civilization/catalog.py` — score **22**
- `aletheus/institutional_civilization/civilization_catalog.py` — score **22**
- `aletheus/institutional_civilization/civilization_models.py` — score **22**

### Policy

**Resolution:** `existing_owner`

**Existing owner or finding:** `aletheus/platform_intelligence/constitutional_policy_engine/exceptions.py`

**Permitted CRK role:** Evaluate a minimal immutable set of kernel admission invariants.

**CRK must never:** Own business rules, application policy, or security-domain policy.

#### Leading candidates

- `aletheus/platform_intelligence/constitutional_policy_engine/exceptions.py` — score **44**
  - class ConstitutionalPolicyEngineError
  - class PolicyAlreadyRegisteredError
  - class PolicyEvaluationError
  - class PolicyNotFoundError
  - class PolicyRegistryFrozenError
- `aletheus/platform_intelligence/constitutional_policy_engine/models.py` — score **32**
  - class ConstitutionalPolicyEngineState
  - class PolicyEngineStatistics
  - class PolicyEvaluation
- `aletheus/executive_kernel/policies.py` — score **30**
  - class ExecutivePolicyRegistry
  - class PolicyDecision
  - class PolicyDescriptor
  - class PolicyScope
  - class PolicyTrustLevel
- `aletheus/platform_intelligence/constitutional_runtime_executive/policies.py` — score **30**
  - class CriticalRuntimePolicy
  - class DegradedRuntimePolicy
  - class ExecutivePolicy
  - class HealthyRuntimePolicy
  - class WarningRuntimePolicy
- `aletheus/experience_gateway/security/default_policy.py` — score **21**
  - class DefaultAuthorizationPolicy
  - function create_default_authorization_policy
- `aletheus/institutional_civilization/security_catalog.py` — score **20**
- `aletheus/institutional_civilization/security_lifecycle.py` — score **20**
- `aletheus/institutional_civilization/security_projection.py` — score **20**

### Evidence

**Resolution:** `review_required`

**Existing owner or finding:** `Multiple strong owner candidates require constitutional review.`

**Permitted CRK role:** Require evidence and provenance references where constitutional contracts demand them.

**CRK must never:** Persist evidence payloads or replace ledger, case, cognition, or knowledge authorities.

#### Leading candidates

- `aletheus/constitutional_ledger/core.py` — score **17**
  - function temporal_provenance
- `aletheus/constitutional_ledger/institutional_event_store.py` — score **17**
  - function by_source
- `aletheus/constitutional_ledger/transtemporal.py` — score **17**
  - function provenance
- `aletheus/constitutional_cases/engine.py` — score **15**
  - function attach_evidence
- `aletheus/constitutional_cognition/models.py` — score **14**
  - class VirtueFinding
- `aletheus/constitutional_ledger/certification.py` — score **14**
- `aletheus/constitutional_ledger/institutional_events.py` — score **14**
- `aletheus/constitutional_ledger/models.py` — score **14**

### Replay

**Resolution:** `existing_owner`

**Existing owner or finding:** `aletheus/constitutional_events/registry.py`

**Permitted CRK role:** Require replay declarations and publish admission events through existing authorities.

**CRK must never:** Become a second event bus, ledger, history, timeline, or replay store.

#### Leading candidates

- `aletheus/constitutional_events/registry.py` — score **38**
  - class ConstitutionalEventRegistry
  - class DuplicateEventTypeError
  - class EventTypeDefinition
  - function build_canonical_event_registry
  - function canonical_event_definitions
- `aletheus/constitutional_ledger/core.py` — score **33**
  - class ConstitutionalLedger
  - function institutional_event
  - function institutional_history
  - function record_event
  - function replay
  - function replay_events
- `aletheus/constitutional_events/fabric.py` — score **32**
  - class ConstitutionalEventFabric
  - class EventDelivery
  - function events
  - function replay
- `aletheus/constitutional_events/models.py` — score **29**
  - class ConstitutionalEvent
  - class ConstitutionalEventType
  - function new_event_id
- `aletheus/runtime/core.py` — score **27**
  - function _cmd_decision_history
  - function _cmd_event_bootstrap
  - function _cmd_event_history
  - function _cmd_event_publish
  - function _cmd_event_replay
  - function _cmd_event_statistics
  - function _cmd_event_subscribe
  - function _cmd_event_unsubscribe
  - function _cmd_reason_history
- `aletheus/constitutional_events/contracts.py` — score **26**
  - class ConstitutionalEventPublisher
  - class ConstitutionalEventSubscriber
- `aletheus/constitutional_events/security.py` — score **26**
  - class SecurityEventType
  - function canonical_security_event_definitions
  - function register_security_event_types
- `aletheus/constitutional_events/subscribers.py` — score **26**
  - class EventCollector
  - class LedgerEventSubscriber

### Validation

**Resolution:** `existing_owner`

**Existing owner or finding:** `aletheus/institutional_civilization/readiness.py`

**Permitted CRK role:** Compose bounded invariant checks and produce typed admission results.

**CRK must never:** Absorb domain validation or application-level business validation.

#### Leading candidates

- `aletheus/institutional_civilization/readiness.py` — score **38**
  - class CivilizationReadinessReport
  - class ReadinessCheck
  - class ReadinessState
- `aletheus/institutional_civilization/civilization_validation.py` — score **35**
  - class CivilizationValidationError
  - class CivilizationValidationIssue
  - function validate_civilization
- `aletheus/institutional_civilization/validation.py` — score **35**
  - class InstitutionValidationError
  - class InstitutionValidationIssue
  - function validate_institution
- `aletheus/application_runtime/validation.py` — score **29**
  - class ApplicationValidationError
  - class ApplicationValidationIssue
  - function validate_manifest
- `aletheus/institutional_civilization/contracts.py` — score **29**
  - class InstitutionHealthProvider
  - function health
- `aletheus/institutional_civilization/bootstrap.py` — score **23**
  - function health
- `aletheus/institutional_civilization/civilization_registry.py` — score **23**
  - function health
- `aletheus/institutional_civilization/engine.py` — score **23**
  - function health

## Constitutional CRK Boundary

### CRK Owns

- Constitutional capability admission contracts.
- Kernel-level invariant evaluation.
- Typed admission and rejection results.
- Composition of existing constitutional authorities.
- Kernel admission-event requests through the existing event authority.

### CRK Does Not Own

- Domain business logic.
- Application authorization.
- Lifecycle execution already owned by runtime and application managers.
- A second application, service, runtime, or civilization registry.
- Evidence persistence.
- Replay persistence.
- Ledger persistence.
- Event-bus implementation.
- Mission execution.
- Governance deliberation.
- Security-domain policy.

## Required Constitutional Review

- **ownership** — `review_required`: Multiple strong owner candidates require constitutional review.
  - `aletheus/institutional_civilization/civilization_registry.py`
  - `aletheus/institutional_civilization/registry.py`
- **evidence** — `review_required`: Multiple strong owner candidates require constitutional review.
  - `aletheus/constitutional_ledger/core.py`
  - `aletheus/constitutional_ledger/institutional_event_store.py`
  - `aletheus/constitutional_ledger/transtemporal.py`
  - `aletheus/constitutional_cases/engine.py`

## Admission Decision

The CRK may only be implemented as a small constitutional admission and invariant boundary. Existing registries, event buses, ledgers, lifecycle managers, governance authorities, and evidence stores remain the single owners of their concepts.
