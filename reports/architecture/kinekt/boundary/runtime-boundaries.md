# Kinekt™ Runtime Boundary Analyzer

- Generated: `2026-07-31T23:23:30.533097+00:00`
- Findings: **10**
- Unresolved relationships: **2828**

## Findings

### [HIGH] RUNTIME_LAYER_LEAK

- Source: `.aletheus_restore_points.repository_conflicts.20260719T065403Z.aletheus.runtime.core` (runtime)
- Target: `aletheus.applications` (product)
- Runtime must not depend on experience or product implementation.
- Recommendation: Introduce a runtime-facing contract or invert the dependency.
- Evidence: .aletheus_restore_points/repository_conflicts/20260719T065403Z/aletheus/runtime/core.py, aletheus/applications/__init__.py

### [HIGH] RUNTIME_LAYER_LEAK

- Source: `.aletheus_restore_points.repository_conflicts.20260719T070434Z.aletheus.runtime.core` (runtime)
- Target: `aletheus.applications` (product)
- Runtime must not depend on experience or product implementation.
- Recommendation: Introduce a runtime-facing contract or invert the dependency.
- Evidence: .aletheus_restore_points/repository_conflicts/20260719T070434Z/aletheus/runtime/core.py, aletheus/applications/__init__.py

### [HIGH] RUNTIME_LAYER_LEAK

- Source: `aletheus.runtime.core` (runtime)
- Target: `aletheus.applications` (product)
- Runtime must not depend on experience or product implementation.
- Recommendation: Introduce a runtime-facing contract or invert the dependency.
- Evidence: aletheus/runtime/core.py, aletheus/applications/__init__.py

### [HIGH] RUNTIME_LAYER_LEAK

- Source: `backups.runtime.core_v4.6.2_stable` (runtime)
- Target: `aletheus.applications` (product)
- Runtime must not depend on experience or product implementation.
- Recommendation: Introduce a runtime-facing contract or invert the dependency.
- Evidence: backups/runtime/core_v4.6.2_stable.py, aletheus/applications/__init__.py

### [HIGH] RUNTIME_LAYER_LEAK

- Source: `components.chds.runtime_monitor` (runtime)
- Target: `cardhawkos.boot.boot_manager` (product)
- Runtime must not depend on experience or product implementation.
- Recommendation: Introduce a runtime-facing contract or invert the dependency.
- Evidence: components/chds/runtime_monitor.py, cardhawkos/boot/boot_manager.py

### [HIGH] RUNTIME_LAYER_LEAK

- Source: `components.chds.runtime_status` (runtime)
- Target: `cardhawkos.config.settings` (product)
- Runtime must not depend on experience or product implementation.
- Recommendation: Introduce a runtime-facing contract or invert the dependency.
- Evidence: components/chds/runtime_status.py, cardhawkos/config/settings.py

### [MEDIUM] EXPERIENCE_RUNTIME_INTERNAL_COUPLING

- Source: `aletheus.experience_gateway.api` (experience)
- Target: `runtime` (runtime)
- Experience code should depend on runtime contracts, not internals.
- Recommendation: Route the dependency through the runtime facade or public API.
- Evidence: aletheus/experience_gateway/api/__init__.py, runtime/__init__.py

### [MEDIUM] EXPERIENCE_RUNTIME_INTERNAL_COUPLING

- Source: `aletheus.experience_gateway.api.missions` (experience)
- Target: `runtime` (runtime)
- Experience code should depend on runtime contracts, not internals.
- Recommendation: Route the dependency through the runtime facade or public API.
- Evidence: aletheus/experience_gateway/api/missions.py, runtime/__init__.py

### [MEDIUM] EXPERIENCE_RUNTIME_INTERNAL_COUPLING

- Source: `tools.genesis.genesis_8.build_compatibility_manifest` (experience)
- Target: `aletheus.runtime` (runtime)
- Experience code should depend on runtime contracts, not internals.
- Recommendation: Route the dependency through the runtime facade or public API.
- Evidence: tools/genesis/genesis_8/build_compatibility_manifest.py, aletheus/runtime/__init__.py

### [MEDIUM] EXPERIENCE_RUNTIME_INTERNAL_COUPLING

- Source: `ui.pages.aletheus_founder_workspace` (experience)
- Target: `aletheus.runtime` (runtime)
- Experience code should depend on runtime contracts, not internals.
- Recommendation: Route the dependency through the runtime facade or public API.
- Evidence: ui/pages/aletheus_founder_workspace.py, aletheus/runtime/__init__.py


## Lowest package boundary scores

- `.aletheus_restore_points` — score **48.10**, status **critical**, violations 2, outbound 159, inbound 0
- `aletheus.experience_gateway` — score **61.00**, status **degraded**, violations 2, outbound 30, inbound 20
- `aletheus.runtime` — score **62.00**, status **degraded**, violations 1, outbound 260, inbound 734
- `components.chds` — score **62.10**, status **degraded**, violations 2, outbound 19, inbound 15
- `backups.runtime` — score **76.70**, status **watch**, violations 1, outbound 53, inbound 0
- `tools.genesis` — score **81.40**, status **watch**, violations 1, outbound 6, inbound 0
- `ui.pages` — score **81.80**, status **watch**, violations 1, outbound 2, inbound 0
- `Genesis10_Work_Organization.04_reports` — score **82.00**, status **watch**, violations 0, outbound 180, inbound 0
- `reports.genesis_8_command_dispatch` — score **82.10**, status **watch**, violations 0, outbound 179, inbound 0
- `aletheus.platform_intelligence` — score **88.70**, status **watch**, violations 0, outbound 113, inbound 94
- `migrations.genesis6` — score **94.70**, status **healthy**, violations 0, outbound 53, inbound 0
- `aletheus.services_economy` — score **94.90**, status **healthy**, violations 0, outbound 51, inbound 0
- `aletheus.span` — score **95.40**, status **healthy**, violations 0, outbound 46, inbound 37
- `aletheus.autonomy` — score **96.10**, status **healthy**, violations 0, outbound 39, inbound 0
- `aletheus.consciousness` — score **96.30**, status **healthy**, violations 0, outbound 37, inbound 0
- `aletheus.evolution` — score **96.30**, status **healthy**, violations 0, outbound 37, inbound 0
- `aletheus.economy` — score **96.40**, status **healthy**, violations 0, outbound 36, inbound 0
- `aletheus.card_hawk` — score **96.60**, status **healthy**, violations 0, outbound 34, inbound 1
- `aletheus.intelligence` — score **96.60**, status **healthy**, violations 0, outbound 34, inbound 10
- `aletheus.executive_kernel` — score **96.90**, status **healthy**, violations 0, outbound 31, inbound 32
- `aletheus.civilization` — score **97.00**, status **healthy**, violations 0, outbound 30, inbound 3
- `tools.maintenance` — score **97.30**, status **healthy**, violations 0, outbound 27, inbound 35
- `aletheus.security` — score **97.40**, status **healthy**, violations 0, outbound 26, inbound 0
- `tests.platform_intelligence` — score **97.40**, status **healthy**, violations 0, outbound 26, inbound 0
- `aletheus.adaptive_intelligence` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.collective` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.genesis_engine` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.governance` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.immortality` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.legacy` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.mastery` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.optimization` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.reliability` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.replication` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.synthesis` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.transcendence` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.wisdom` — score **97.50**, status **healthy**, violations 0, outbound 25, inbound 0
- `aletheus.federation` — score **97.60**, status **healthy**, violations 0, outbound 24, inbound 0
- `aletheus.foresight` — score **97.60**, status **healthy**, violations 0, outbound 24, inbound 0
- `aletheus.metasystem` — score **97.60**, status **healthy**, violations 0, outbound 24, inbound 0
- `aletheus.strategy` — score **97.60**, status **healthy**, violations 0, outbound 24, inbound 0
- `aletheus.civilization_expansion` — score **97.70**, status **healthy**, violations 0, outbound 23, inbound 0
- `aletheus.institutional_civilization` — score **97.70**, status **healthy**, violations 0, outbound 23, inbound 6
- `tests.tools` — score **97.70**, status **healthy**, violations 0, outbound 23, inbound 0
- `aletheus.singularity` — score **97.80**, status **healthy**, violations 0, outbound 22, inbound 0
- `aletheus.neural` — score **98.00**, status **healthy**, violations 0, outbound 20, inbound 5
- `tools.verification` — score **98.00**, status **healthy**, violations 0, outbound 20, inbound 0
- `aletheus.infrastructure` — score **98.10**, status **healthy**, violations 0, outbound 19, inbound 0
- `tests.experience_gateway` — score **98.10**, status **healthy**, violations 0, outbound 19, inbound 0
- `aletheus.strategic` — score **98.20**, status **healthy**, violations 0, outbound 18, inbound 13
- `falcon.runtime` — score **98.20**, status **healthy**, violations 0, outbound 18, inbound 6
- `aletheus.platform_surface` — score **98.30**, status **healthy**, violations 0, outbound 17, inbound 4
- `aletheus.tooling` — score **98.30**, status **healthy**, violations 0, outbound 17, inbound 7
- `tools.repository` — score **98.30**, status **healthy**, violations 0, outbound 17, inbound 7
- `aletheusos_kernel_sprint1.src` — score **98.40**, status **healthy**, violations 0, outbound 16, inbound 0
- `aletheus.enterprise` — score **98.60**, status **healthy**, violations 0, outbound 14, inbound 10
- `aletheus.trust` — score **98.60**, status **healthy**, violations 0, outbound 14, inbound 0
- `executive_experience.pages` — score **98.60**, status **healthy**, violations 0, outbound 14, inbound 0
- `aletheus.application_runtime` — score **98.70**, status **healthy**, violations 0, outbound 13, inbound 3
- `aletheus.atlas` — score **98.70**, status **healthy**, violations 0, outbound 13, inbound 3
- `aletheus.constitutional_library` — score **98.70**, status **healthy**, violations 0, outbound 13, inbound 1
- `aletheus.identity_engine` — score **98.70**, status **healthy**, violations 0, outbound 13, inbound 1
- `aletheus.sdk` — score **98.70**, status **healthy**, violations 0, outbound 13, inbound 6
- `live_platform.pages` — score **98.70**, status **healthy**, violations 0, outbound 13, inbound 0
- `tests.institutional_civilization` — score **98.70**, status **healthy**, violations 0, outbound 13, inbound 0
- `aletheus.autonomous_ecosystem` — score **98.80**, status **healthy**, violations 0, outbound 12, inbound 0
- `aletheus.civilization_intelligence` — score **98.80**, status **healthy**, violations 0, outbound 12, inbound 0
- `aletheus.constitutional_events` — score **98.80**, status **healthy**, violations 0, outbound 12, inbound 20
- `aletheus.constitutional_scenarios` — score **98.80**, status **healthy**, violations 0, outbound 12, inbound 4
- `aletheus.double_hedron` — score **98.80**, status **healthy**, violations 0, outbound 12, inbound 1
- `aletheus.execution_graph` — score **98.80**, status **healthy**, violations 0, outbound 12, inbound 1
- `aletheus.intelligence_expansion` — score **98.80**, status **healthy**, violations 0, outbound 12, inbound 0
- `aletheus.operating_intelligence` — score **98.80**, status **healthy**, violations 0, outbound 12, inbound 0
- `aletheus.constitutional_ledger` — score **98.90**, status **healthy**, violations 0, outbound 11, inbound 11
- `aletheus.foundation` — score **98.90**, status **healthy**, violations 0, outbound 11, inbound 3
- `aletheus.ontology` — score **98.90**, status **healthy**, violations 0, outbound 11, inbound 0
- `applications.cardhawk_foundation` — score **98.90**, status **healthy**, violations 0, outbound 11, inbound 0
- `thorx.score` — score **98.90**, status **healthy**, violations 0, outbound 11, inbound 0
- `aletheus.capability_engine` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 1
- `aletheus.civilization_federation` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 0
- `aletheus.civilization_platform` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 0
- `aletheus.concept_collision_engine` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 1
- `aletheus.constitutional_cases` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 4
- `aletheus.constitutional_instrumentation` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 5
- `aletheus.constitutional_missions` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 4
- `aletheus.mission_runtime` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 2
- `aletheus.operations` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 0
- `aletheus.platform_verification` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 7
- `aletheus.reason_engine` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 1
- `app` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 0
- `orchestrator.runtime` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 2
- `reports.span` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 0
- `services.runtime_v3` — score **99.00**, status **healthy**, violations 0, outbound 10, inbound 2
- `aletheus.constitutional_graph` — score **99.10**, status **healthy**, violations 0, outbound 9, inbound 9
- `aletheus.engine_registry` — score **99.10**, status **healthy**, violations 0, outbound 9, inbound 1
- `aletheus.foundation_service_bus` — score **99.10**, status **healthy**, violations 0, outbound 9, inbound 3
- `aletheus.genesis` — score **99.10**, status **healthy**, violations 0, outbound 9, inbound 1
- `aletheus.runtime_platform` — score **99.10**, status **healthy**, violations 0, outbound 9, inbound 11
- `aletheus.runtime_supervisor` — score **99.10**, status **healthy**, violations 0, outbound 9, inbound 0
- `aletheus.spa` — score **99.10**, status **healthy**, violations 0, outbound 9, inbound 0