# SPAN™ Architectural Analysis Report

Generated: `2026-07-19T09:46:50.731800+00:00`
Repository: `/Users/master_lord_6ixth/Development/AletheusOS`

## Summary

- Analyzers: **1**
- Successful analyzers: **1**
- Failed analyzers: **0**
- Findings: **40**
- Evidence records: **5351**
- Graph nodes: **3955**
- Graph edges: **3267**

## dependency v1.0.0

Status: **passed**

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.agents → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.agents_v2 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.distributed_v3 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.event_bus_v3 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.federation_v3 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.high_availability_v3 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.persistence_v3 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.planning → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.planning_v2 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.plugins_v3 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.security_v3 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.telemetry_v3 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.tenancy_v3 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus → aletheus.runtime → aletheus.runtime.core → aletheus.workflow_v3 → aletheus

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.agents → aletheus.runtime → aletheus.runtime.core → aletheus.agents

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.intelligence.civilization_core → aletheus.intelligence.civilization_core

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.intelligence.knowledge_network → aletheus.intelligence.knowledge_network

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.marketplace_intelligence.runtime → aletheus.marketplace_intelligence.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.platform_intelligence.orchestrator → aletheus.platform_intelligence.orchestrator

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.anchors → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.anchors → aletheus.runtime.lifecycle → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.anchors → aletheus.runtime.migration → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.boot_pipeline → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.command_bootstrap.bootstrapper → aletheus.runtime.registrations.decision_commands → aletheus.runtime.domains → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.commands → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.commands → aletheus.runtime.registry → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.compat → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.compatibility_layer → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.governance → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.integrity → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.kernel → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.managers → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.providers → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime → aletheus.runtime.core → aletheus.runtime.services → aletheus.runtime

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime.builder → aletheus.runtime.builder

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime.container → aletheus.runtime.container

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime.dashboard → aletheus.runtime.dashboard

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime.discovery → aletheus.runtime.discovery

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.runtime.kernel → aletheus.runtime.kernel

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.

### [HIGH] Python dependency cycle detected

aletheus.spa.council → aletheus.spa.council

**Recommendation:** Break the cycle using an interface, event boundary, shared contract, or dependency inversion.
