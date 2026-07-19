# Genesis 8 Command Compatibility Manifest

## Summary

- test_command_requirements: **232**
- registered_requirements: **119**
- probable_aliases: **65**
- defined_but_not_registered: **38**
- missing_capabilities: **10**
- live_registry_commands: **170**
- generation: **170**
- fingerprint: **e2efbce77d549c63caa3a2ff7f3d7a82124c942864d946d72817b0398f2060a8**

## Probable Alias

### `Runtime Health Workflow`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_031.py:49`, `tests/test_aletheus_runtime_a3.py:32`
- Alias candidates: `runtime.health_report` (0.68)

### `agent.bootstrap`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v13_agents.py:11`, `tests/test_aletheus_v27_agents.py:11`
- Alias candidates: `event.bootstrap` (0.68), `tenant.bootstrap` (0.66), `ha.bootstrap` (0.65), `state.bootstrap` (0.64), `kernel.bootstrap` (0.62)
- Source references: `aletheus/runtime/registrations/agent_commands.py:15`

### `agent.heartbeat`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v27_agents.py:58`
- Alias candidates: `cluster.heartbeat` (0.56)
- Source references: `aletheus/agents_v2/agent_core.py:156`, `aletheus/runtime/registrations/agent_commands.py:50`

### `agent.statistics`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v27_agents.py:62`
- Alias candidates: `event.statistics` (0.65), `tenant.statistics` (0.63), `ha.statistics` (0.60), `state.statistics` (0.59), `learning.statistics` (0.59)
- Source references: `aletheus/runtime/registrations/agent_commands.py:55`

### `application.list`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_09a.py:11`, `tests/test_aletheus_genesis_10.py:19`
- Alias candidates: `plugin.list` (0.55)
- Source references: `aletheus/kernel_v2/kernel_core.py:84`, `aletheus/runtime/registrations/application_commands.py:18`

### `application.stats`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_09a.py:28`, `tests/test_aletheus_v20b_applications.py:5`
- Alias candidates: `plugin.statistics` (0.56), `mission.statistics` (0.55), `prediction.statistics` (0.55), `federation.statistics` (0.55)
- Source references: `aletheus/runtime/registrations/application_commands.py:43`

### `cardhawk.status`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_09a.py:22`
- Alias candidates: `ha.status` (0.60)
- Source references: `aletheus/applications/application_core.py:103`

### `cluster.bootstrap`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v22_distributed.py:11`, `tests/test_aletheus_v22_distributed.py:18`, `tests/test_aletheus_v22_distributed.py:41`, `tests/test_aletheus_v30_distributed.py:11`
- Alias candidates: `state.bootstrap` (0.64), `security.bootstrap` (0.60), `kernel.bootstrap` (0.59), `tenant.bootstrap` (0.59), `plugin.bootstrap` (0.59)

### `cluster.broadcast`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v22_distributed.py:44`
- Alias candidates: `cluster.nodes` (0.59), `cluster.services` (0.55), `cluster.statistics` (0.55)

### `cluster.stats`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v22_distributed.py:69`
- Alias candidates: `cluster.statistics` (1.00), `state.statistics` (0.60), `learning.statistics` (0.60), `cluster.heartbeat` (0.59), `cluster.leave` (0.57)

### `cluster.status`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v22_distributed.py:32`, `tests/test_aletheus_v30_distributed.py:84`
- Alias candidates: `cluster.statistics` (0.74), `cluster.heartbeat` (0.58), `cluster.services` (0.55), `plugin.status` (0.55), `cluster.leave` (0.55)

### `compat.statistics`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v41_compatibility.py:25`
- Alias candidates: `ha.statistics` (0.57), `state.statistics` (0.57), `tenant.statistics` (0.55)
- Source references: `aletheus/runtime/hardening.py:51`, `aletheus/runtime/hardening.py:64`, `aletheus/runtime/hardening.py:84`, `aletheus/runtime/adapters/compatibility_adapter.py:32`, `aletheus/runtime/integrity/boot_validator.py:16`, `aletheus/runtime/integrity/doctor.py:22`, `aletheus/runtime/integrity/invariants.py:25`, `aletheus/runtime/handlers/compatibility_handlers.py:26`, `aletheus/runtime/registrations/compatibility_commands.py:22`

### `copilot.recommend`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v15_copilot.py:27`
- Alias candidates: `prediction.recommend` (0.58)
- Source references: `aletheus/runtime/domains/copilot.py:49`, `aletheus/runtime/registrations/copilot_commands.py:30`

### `decision.bootstrap`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v26_decision_engine.py:11`
- Alias candidates: `reason.bootstrap` (0.65), `federation.bootstrap` (0.63), `event.bootstrap` (0.59), `security.bootstrap` (0.59), `kernel.bootstrap` (0.58)
- Source references: `aletheus/runtime/domains/decision.py:15`, `aletheus/runtime/registrations/decision_commands.py:16`

### `decision.evaluate`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v26_decision_engine.py:19`
- Alias candidates: `reason.evaluate` (0.64)
- Source references: `aletheus/runtime/domains/decision.py:35`, `aletheus/runtime/registrations/decision_commands.py:26`

### `decision.execute`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v26_decision_engine.py:52`
- Alias candidates: `mission.execute` (0.66), `kernel.execute` (0.55)
- Source references: `aletheus/decision_v2/decision_core.py:188`, `aletheus/runtime/domains/decision.py:47`, `aletheus/runtime/registrations/decision_commands.py:31`

### `decision.explain`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v26_decision_engine.py:59`
- Alias candidates: `reason.explain` (0.64)
- Source references: `aletheus/runtime/domains/decision.py:63`, `aletheus/runtime/registrations/decision_commands.py:41`

### `decision.history`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v26_decision_engine.py:75`
- Alias candidates: `audit.history` (0.56), `event.history` (0.56)
- Source references: `aletheus/runtime/domains/decision.py:73`, `aletheus/runtime/registrations/decision_commands.py:46`

### `decision.record`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_05.py:59`
- Alias candidates: `learning.record` (0.55)

### `decision.statistics`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v26_decision_engine.py:79`
- Alias candidates: `mission.statistics` (0.65), `reason.statistics` (0.62), `federation.statistics` (0.59)
- Source references: `aletheus/runtime/domains/decision.py:84`, `aletheus/runtime/registrations/decision_commands.py:51`

### `entity.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_06.py:11`, `tests/test_aletheus_genesis_06.py:34`, `tests/test_aletheus_genesis_06.py:39`
- Alias candidates: `knowledge.entity.create` (0.70), `tenant.create` (0.62), `enterprise.create` (0.59), `policy.create` (0.57), `team.create` (0.55)
- Source references: `aletheus/runtime/registrations/graph_commands.py:15`, `aletheus/runtime/registrations/knowledge_graph_commands.py:16`

### `goal.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_05.py:11`
- Alias candidates: `policy.create` (0.60), `team.create` (0.59), `workflow.create` (0.57), `tenant.create` (0.55), `workspace.create` (0.55)

### `graph.stats`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_06.py:66`
- Alias candidates: `ha.statistics` (0.60), `reason.statistics` (0.57)
- Source references: `aletheus/runtime/registrations/graph_commands.py:45`

### `kernel.boot`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20_kernel.py:11`
- Alias candidates: `kernel.bootstrap` (0.65), `kernel.tasks` (0.57), `kernel.statistics` (0.57)
- Source references: `aletheus/kernel_v2/kernel_core.py:25`, `aletheus/platform_kernel/kernel.py:159`, `aletheus/executive_kernel/kernel.py:7`, `aletheus/executive_kernel/__init__.py:1`, `aletheus/runtime/composition/root.py:65`, `aletheus/runtime/commands_v2/dispatcher.py:53`, `aletheus/runtime/registrations/kernel_commands.py:13`

### `kernel.publish`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20_kernel.py:25`
- Alias candidates: `event.publish` (0.60)

### `kernel.snapshot`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20_kernel.py:39`
- Alias candidates: `learning.snapshot` (0.65), `kernel.statistics` (0.60), `state.snapshot` (0.56), `kernel.supervisor` (0.56), `registry.snapshot` (0.56)

### `kernel.sync`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20_kernel.py:18`
- Alias candidates: `kernel.tasks` (0.57), `kernel.statistics` (0.57), `kernel.scheduler` (0.55)

### `learn.improve`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v18_learning.py:41`
- Alias candidates: `learning.improve` (1.00)

### `learn.lesson`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v18_learning.py:26`
- Alias candidates: `learning.lesson` (1.00), `learning.statistics` (0.57), `learning.snapshot` (0.57), `learning.record` (0.55)

### `learn.patterns`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v18_learning.py:40`
- Alias candidates: `learning.patterns` (1.00), `learning.statistics` (0.58)

### `learn.record`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v18_learning.py:11`
- Alias candidates: `learning.record` (1.00), `telemetry.record` (0.58), `learning.lesson` (0.55)
- Source references: `aletheus/missions_v2/mission_core.py:226`, `aletheus/workflows_v2/workflow_core.py:69`, `aletheus/workflows_v2/workflow_core.py:102`, `aletheus/workflows_v2/workflow_core.py:253`

### `learn.snapshot`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v18_learning.py:50`
- Alias candidates: `learning.snapshot` (1.00), `learning.statistics` (0.58), `state.snapshot` (0.58), `registry.snapshot` (0.58), `runtime.snapshot` (0.55)

### `mission.run`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_07.py:42`
- Alias candidates: `mission.create` (0.58), `mission.list` (0.57), `mission.execute` (0.57), `mission.statistics` (0.55)
- Source references: `aletheus/runtime/adapters/mission_adapter.py:143`, `aletheus/runtime/handlers/mission_handlers.py:137`, `aletheus/runtime/registrations/mission_commands.py:34`

### `mission.stats`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_07.py:53`
- Alias candidates: `mission.statistics` (1.00), `mission.list` (0.64), `mission.create` (0.60), `reason.statistics` (0.58)
- Source references: `aletheus/runtime/adapters/mission_adapter.py:224`, `aletheus/runtime/commands/runtime_commands.py:69`, `aletheus/runtime/registrations/mission_commands.py:58`

### `mission.v2.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20c_missions.py:11`, `tests/test_aletheus_v20c_missions.py:26`, `tests/test_aletheus_v20c_missions.py:54`
- Alias candidates: `mission.create` (0.82), `mission.complete` (0.56)
- Source references: `aletheus/workflows_v2/workflow_core.py:48`

### `mission.v2.execute`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20c_missions.py:44`
- Alias candidates: `mission.execute` (0.82)

### `mission.v2.execute_next`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20c_missions.py:64`
- Alias candidates: `mission.execute` (0.69)

### `mission.v2.stats`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20c_missions.py:77`
- Alias candidates: `mission.statistics` (0.82), `mission.list` (0.55)

### `node.heartbeat`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v22_distributed.py:22`
- Alias candidates: `cluster.heartbeat` (0.58)
- Source references: `aletheus/distributed_v3/distributed_core.py:183`

### `notification.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_08.py:53`
- Alias candidates: `organization.create` (0.60), `mission.create` (0.55)
- Source references: `aletheus/runtime/registrations/workspace_commands.py:43`

### `objective.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_08.py:17`
- Alias candidates: `enterprise.create` (0.55)
- Source references: `aletheus/runtime/registrations/workspace_commands.py:33`

### `plan.bootstrap`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v29_planning.py:11`
- Alias candidates: `plugin.bootstrap` (0.68), `ha.bootstrap` (0.67), `reason.bootstrap` (0.64), `tenant.bootstrap` (0.64), `event.bootstrap` (0.61)

### `plan.complete`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v29_planning.py:47`
- Alias candidates: `mission.complete` (0.56)
- Source references: `aletheus/planning/planning_core.py:80`, `aletheus/planning/planning_core.py:105`, `aletheus/planning_v2/planning_core.py:193`

### `plan.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v29_planning.py:17`
- Alias candidates: `tenant.create` (0.60), `policy.create` (0.60), `team.create` (0.59), `department.create` (0.58), `workspace.create` (0.55)

### `plan.execute`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v29_planning.py:26`
- Alias candidates: `kernel.execute` (0.57), `mission.execute` (0.55)
- Source references: `aletheus/planning_v2/planning_core.py:180`

### `plan.statistics`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v29_planning.py:61`
- Alias candidates: `learning.statistics` (0.67), `plugin.statistics` (0.65), `ha.statistics` (0.62), `tenant.statistics` (0.59), `reason.statistics` (0.59)

### `plan.status`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v29_planning.py:57`
- Alias candidates: `plugin.status` (0.66), `ha.status` (0.64)
- Source references: `aletheus/planning/planning_core.py:67`, `aletheus/planning/planning_core.py:121`, `aletheus/planning/planning_core.py:137`, `aletheus/planning/planning_core.py:138`, `aletheus/planning_v2/planning_core.py:209`

### `planning.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v14_planning.py:11`, `tests/test_aletheus_v14_planning.py:21`, `tests/test_aletheus_v14_planning.py:38`
- Alias candidates: `policy.create` (0.58)
- Source references: `aletheus/copilot/copilot_core.py:50`, `aletheus/copilot/copilot_core.py:54`, `aletheus/missions_v2/mission_core.py:131`, `aletheus/workflows_v2/workflow_core.py:94`, `aletheus/runtime/domains/planning.py:15`

### `predict.forecast`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v17_prediction.py:11`
- Alias candidates: `prediction.forecast` (1.00), `prediction.risks` (0.56), `prediction.statistics` (0.56), `prediction.recommend` (0.55)
- Source references: `aletheus/workflows_v2/workflow_core.py:40`

### `predict.opportunities`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v17_prediction.py:32`
- Alias candidates: `prediction.opportunities` (1.00)

### `predict.recommend`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v17_prediction.py:41`
- Alias candidates: `prediction.recommend` (1.00), `prediction.forecast` (0.55), `prediction.timeline` (0.55), `prediction.scenario` (0.55)

### `predict.risks`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v17_prediction.py:31`
- Alias candidates: `prediction.risks` (1.00), `prediction.statistics` (0.62), `prediction.forecast` (0.56), `prediction.scenario` (0.56)

### `predict.scenario`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v17_prediction.py:18`
- Alias candidates: `prediction.scenario` (1.00), `prediction.risks` (0.56), `prediction.statistics` (0.56), `prediction.recommend` (0.55)

### `relationship.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_06.py:44`
- Alias candidates: `knowledge.relationship.create` (0.75), `organization.create` (0.56)
- Source references: `aletheus/runtime/registrations/graph_commands.py:25`, `aletheus/runtime/registrations/knowledge_graph_commands.py:31`

### `release.status`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_10.py:5`
- Alias candidates: `ha.status` (0.57)

### `runtime.diagnostics`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_031.py:16`, `tests/test_aletheus_genesis_04.py:11`, `tests/test_aletheus_genesis_05.py:5`, `tests/test_aletheus_genesis_06.py:5`, `tests/test_aletheus_genesis_07.py:5`, `tests/test_aletheus_genesis_08.py:5`, `tests/test_aletheus_genesis_09a.py:5`, `tests/test_aletheus_v11_semantic.py:5`, `tests/test_aletheus_v12_executive.py:5`, `tests/test_aletheus_v13_agents.py:5`, `tests/test_aletheus_v14_planning.py:5`, `tests/test_aletheus_v15_copilot.py:5`, `tests/test_aletheus_v16_universal_intelligence.py:5`, `tests/test_aletheus_v17_prediction.py:5`, `tests/test_aletheus_v18_learning.py:5`, `tests/test_aletheus_v20_kernel.py:5`, `tests/test_aletheus_v20c_missions.py:5`, `tests/test_aletheus_v20d_workflows.py:5`, `tests/test_aletheus_v21_enterprise.py:5`, `tests/test_aletheus_v22_distributed.py:5`, `tests/test_aletheus_v23_memory_mesh.py:5`, `tests/test_aletheus_v24_graph.py:5`, `tests/test_aletheus_v25_reasoning.py:5`, `tests/test_aletheus_v26_decision_engine.py:5`, `tests/test_aletheus_v27_agents.py:5`, `tests/test_aletheus_v28_workflows.py:5`, `tests/test_aletheus_v29_planning.py:5`, `tests/test_aletheus_v30_distributed.py:5`, `tests/test_aletheus_v31_plugins.py:5`, `tests/test_aletheus_v32_persistence.py:5`, `tests/test_aletheus_v33_event_bus.py:6`, `tests/test_aletheus_v34_federation.py:6`, `tests/test_aletheus_v35_telemetry.py:6`, `tests/test_aletheus_v36_high_availability.py:6`, `tests/test_aletheus_v37_security.py:6`, `tests/test_aletheus_v39_tenancy.py:6`, `tests/test_aletheus_v40_kernel.py:134`, `tests/test_aletheus_v40_kernel.py:150`, `tests/test_aletheus_v41_compatibility.py:39`
- Alias candidates: `runtime.docs` (0.62), `runtime.audit` (0.56), `runtime.doctor` (0.55)
- Source references: `aletheus/kernel_v2/kernel_core.py:73`, `aletheus/kernel_v2/kernel_core.py:81`, `aletheus/intelligence/intelligence_core.py:15`, `aletheus/workspace/workspace_core.py:84`, `aletheus/runtime/core.py:70`, `aletheus/runtime/hardening.py:83`, `aletheus/release/core.py:65`, `aletheus/platform_intelligence/runtime_snapshot.py:42`, `aletheus/executive/executive_core.py:17`, `aletheus/runtime/managers/observability_manager.py:27`, `aletheus/runtime/managers/runtime_facade.py:66`, `aletheus/runtime/integrity/boot_validator.py:18`, `aletheus/runtime/commands/runtime_commands.py:36`, `aletheus/runtime/commands/command_bus.py:56`

### `runtime.health`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_031.py:10`, `tests/test_aletheus_genesis_04.py:5`, `tests/test_aletheus_runtime_a3.py:7`
- Alias candidates: `runtime.health_report` (0.75), `runtime.audit` (0.60), `runtime.selftest` (0.59), `tenant.health` (0.55), `runtime.snapshot` (0.55)
- Source references: `aletheus/kernel_v2/kernel_core.py:16`, `aletheus/kernel_v2/kernel_core.py:74`, `aletheus/copilot/copilot_core.py:81`, `aletheus/intelligence/intelligence_core.py:16`, `aletheus/intelligence/intelligence_core.py:139`, `aletheus/learning/learning_core.py:115`, `aletheus/workspace/workspace_core.py:83`, `aletheus/runtime/adapter.py:134`, `aletheus/runtime/adapter.py:137`, `aletheus/release/core.py:64`, `aletheus/executive/executive_core.py:16`, `aletheus/runtime/managers/validation_manager.py:21`, `aletheus/runtime/composition/root.py:9`, `aletheus/runtime/adapters/runtime_adapter.py:216`, `aletheus/runtime/adapters/runtime_adapter.py:234`, `aletheus/runtime/orchestration/orchestrator.py:48`, `aletheus/runtime/commands/command_bus.py:55`, `aletheus/runtime/registrations/runtime_commands.py:64`

### `security.role.assign`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v37_security.py:51`
- Alias candidates: `security.role_assign` (1.00), `security.role_create` (0.66)

### `security.role.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v37_security.py:29`
- Alias candidates: `security.role_create` (1.00), `security.role_assign` (0.66)

### `semantic.bootstrap.cardhawk`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v11_semantic.py:42`
- Alias candidates: `enterprise.bootstrap.cardhawk` (0.66), `knowledge.bootstrap.cardhawk` (0.65)
- Source references: `aletheus/runtime/registrations/semantic_commands.py:38`

### `semantic.explain`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v11_semantic.py:36`
- Alias candidates: `reason.explain` (0.55)
- Source references: `aletheus/runtime/registrations/semantic_commands.py:33`

### `workflow.v2.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20d_workflows.py:11`, `tests/test_aletheus_v20d_workflows.py:25`, `tests/test_aletheus_v20d_workflows.py:46`
- Alias candidates: `workflow.create` (0.82), `workflow.resume` (0.56)

### `workflow.v2.history`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20d_workflows.py:61`
- Alias candidates: `workflow.start` (0.56)

### `workflow.v2.stats`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20d_workflows.py:72`
- Alias candidates: `workflow.statistics` (0.82), `workflow.status` (0.66), `workflow.start` (0.63)

### `workspace.overview`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_08.py:11`
- Alias candidates: `workspace.delete` (0.58), `workspace.create` (0.58), `workspace.list` (0.56)
- Source references: `aletheus/copilot/copilot_core.py:67`, `aletheus/copilot/copilot_core.py:69`, `aletheus/runtime/registrations/workspace_commands.py:13`


## Defined But Not Registered

### `agent.assign`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v27_agents.py:26`
- Source references: `aletheus/agents_v2/agent_core.py:131`, `aletheus/agents/agent_core.py:127`, `aletheus/runtime/registrations/agent_commands.py:25`

### `agent.message`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v27_agents.py:33`
- Source references: `aletheus/runtime/registrations/agent_commands.py:30`

### `agent.orchestrate`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v13_agents.py:37`
- Source references: `aletheus/workflows_v2/workflow_core.py:61`

### `agent.pause`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v27_agents.py:44`
- Source references: `aletheus/runtime/registrations/agent_commands.py:35`

### `agent.resume`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v27_agents.py:48`
- Source references: `aletheus/runtime/registrations/agent_commands.py:40`

### `agent.run`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v13_agents.py:28`
- Source references: `aletheus/planning/planning_core.py:100`, `aletheus/missions_v2/mission_core.py:180`, `aletheus/workflows_v2/workflow_core.py:183`

### `agent.spawn`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v27_agents.py:17`
- Source references: `aletheus/runtime/registrations/agent_commands.py:20`

### `agent.stop`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v27_agents.py:52`
- Source references: `aletheus/runtime/registrations/agent_commands.py:45`

### `agent.task.assign`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v13_agents.py:17`
- Source references: `aletheus/planning/planning_core.py:86`, `aletheus/missions_v2/mission_core.py:165`, `aletheus/workflows_v2/workflow_core.py:176`

### `application.bootstrap.defaults`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20b_applications.py:11`, `tests/test_aletheus_v20b_applications.py:30`
- Source references: `aletheus/runtime/registrations/application_commands.py:68`

### `application.manifest`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20b_applications.py:19`
- Source references: `aletheus/runtime/registrations/application_commands.py:58`

### `application.start`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20b_applications.py:46`
- Source references: `aletheus/runtime_supervisor/core.py:19`, `aletheus/applications/models.py:92`, `aletheus/runtime/registrations/application_commands.py:23`

### `application.stop`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20b_applications.py:35`
- Source references: `aletheus/runtime_supervisor/core.py:20`, `aletheus/applications/models.py:99`, `aletheus/runtime/registrations/application_commands.py:28`

### `cardhawk.start`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_09a.py:18`
- Source references: `aletheus/applications/application_core.py:104`

### `compat.contract`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v41_compatibility.py:33`
- Source references: `aletheus/runtime/adapters/compatibility_adapter.py:61`, `aletheus/runtime/handlers/compatibility_handlers.py:55`, `aletheus/runtime/registrations/compatibility_commands.py:34`

### `compat.resolve`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v41_compatibility.py:29`
- Source references: `aletheus/runtime/hardening.py:35`, `aletheus/runtime/adapters/compatibility_adapter.py:44`, `aletheus/runtime/handlers/compatibility_handlers.py:36`, `aletheus/runtime/registrations/compatibility_commands.py:28`

### `copilot.ask`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v15_copilot.py:17`
- Source references: `aletheus/runtime/domains/copilot.py:13`, `aletheus/runtime/registrations/copilot_commands.py:20`

### `copilot.brief`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v15_copilot.py:11`
- Source references: `aletheus/runtime/domains/copilot.py:37`, `aletheus/runtime/registrations/copilot_commands.py:25`

### `decision.rollback`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v26_decision_engine.py:66`
- Source references: `aletheus/decision_v2/decision_core.py:196`, `aletheus/decision_v2/decision_core.py:199`, `aletheus/runtime/domains/decision.py:55`, `aletheus/runtime/registrations/decision_commands.py:36`

### `entity.search`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_06.py:24`
- Source references: `aletheus/runtime/registrations/graph_commands.py:20`

### `executive.daily_brief`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v12_executive.py:25`
- Source references: `aletheus/runtime/registrations/executive_commands.py:38`

### `executive.recommendations`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v12_executive.py:18`
- Source references: `aletheus/copilot/copilot_core.py:28`, `aletheus/copilot/copilot_core.py:57`, `aletheus/copilot/copilot_core.py:59`, `aletheus/runtime/registrations/executive_commands.py:28`

### `executive.summary`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v12_executive.py:11`
- Source references: `aletheus/copilot/copilot_core.py:27`, `aletheus/copilot/copilot_core.py:44`, `aletheus/copilot/copilot_core.py:46`, `aletheus/runtime/registrations/executive_commands.py:23`

### `founder.journal.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_08.py:35`
- Source references: `aletheus/runtime/registrations/workspace_commands.py:23`

### `founder.journal.list`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_08.py:48`
- Source references: `aletheus/runtime/registrations/workspace_commands.py:28`

### `graph.query`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_06.py:56`
- Source references: `aletheus/runtime/registrations/graph_commands.py:40`

### `mission.from_goal`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_07.py:31`
- Source references: `aletheus/runtime/registrations/mission_commands.py:22`

### `notification.list`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_08.py:65`
- Source references: `aletheus/runtime/registrations/workspace_commands.py:48`

### `objective.list`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_08.py:30`
- Source references: `aletheus/runtime/registrations/workspace_commands.py:38`

### `plan.generate`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_05.py:30`
- Source references: `aletheus/missions_v2/mission_core.py:138`, `aletheus/runtime/registrations/planning_commands.py:15`

### `planning.execute`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v14_planning.py:44`
- Source references: `aletheus/runtime/domains/planning.py:52`, `aletheus/runtime/domains/planning.py:76`

### `planning.execute_next`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v14_planning.py:27`
- Source references: `aletheus/runtime/domains/planning.py:52`

### `semantic.assert`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v11_semantic.py:22`
- Source references: `aletheus/runtime/registrations/semantic_commands.py:23`

### `semantic.concept.create`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v11_semantic.py:11`
- Source references: `aletheus/runtime/registrations/semantic_commands.py:13`

### `uil.brief`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v16_universal_intelligence.py:40`
- Source references: `aletheus/runtime/registrations/uil_commands.py:33`

### `uil.context`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v16_universal_intelligence.py:11`
- Source references: `aletheus/workflows_v2/workflow_core.py:32`, `aletheus/runtime/registrations/uil_commands.py:13`

### `uil.decide`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v16_universal_intelligence.py:30`
- Source references: `aletheus/runtime/registrations/uil_commands.py:28`

### `uil.reason`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v16_universal_intelligence.py:20`
- Source references: `aletheus/workflows_v2/workflow_core.py:86`, `aletheus/runtime/registrations/uil_commands.py:18`


## Missing Capability

### `Sample Pipeline`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_031.py:29`, `tests/test_aletheus_runtime_a3.py:17`

### `cluster.task.assign`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v22_distributed.py:55`

### `goal.list`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_05.py:24`

### `mission.v2.plan`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20c_missions.py:37`

### `mission.v2.telemetry`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20c_missions.py:66`

### `plan.progress`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v29_planning.py:33`

### `plan.replan`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v29_planning.py:40`

### `release.validate`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_genesis_10.py:11`

### `workflow.v2.execute`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20d_workflows.py:35`

### `workflow.v2.execute_next`

- Registered: `False`
- Handler: `None`
- Invocation mode: `None`
- Tests: `tests/test_aletheus_v20d_workflows.py:56`


## Registered

### `audit.history`

- Registered: `True`
- Handler: `aletheus.runtime.domains.enterprise.EnterpriseDomain.audit_history`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v21_enterprise.py:81`
- Alias candidates: `event.history` (0.57)
- Source references: `aletheus/runtime/registrations/enterprise_commands.py:56`

### `cluster.elect_leader`

- Registered: `True`
- Handler: `aletheus.runtime.domains.cluster.ClusterDomain.elect_leader`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v30_distributed.py:62`
- Alias candidates: `cluster.leave` (0.56)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:109`, `aletheus/runtime/registrations/cluster_commands.py:19`

### `cluster.heartbeat`

- Registered: `True`
- Handler: `aletheus.runtime.domains.cluster.ClusterDomain.heartbeat`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v30_distributed.py:73`
- Alias candidates: `cluster.statistics` (0.59), `cluster.leave` (0.59), `cluster.services` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:110`, `aletheus/runtime/registrations/cluster_commands.py:18`

### `cluster.join`

- Registered: `True`
- Handler: `aletheus.runtime.domains.cluster.ClusterDomain.join`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v30_distributed.py:22`
- Alias candidates: `cluster.nodes` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:108`, `aletheus/runtime/registrations/cluster_commands.py:14`

### `cluster.leave`

- Registered: `True`
- Handler: `aletheus.runtime.domains.cluster.ClusterDomain.leave`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v30_distributed.py:50`
- Alias candidates: `cluster.services` (0.61), `cluster.heartbeat` (0.59), `cluster.statistics` (0.57), `cluster.nodes` (0.57), `cluster.elect_leader` (0.56)
- Source references: `aletheus/runtime/registrations/cluster_commands.py:15`

### `cluster.nodes`

- Registered: `True`
- Handler: `aletheus.runtime.domains.cluster.ClusterDomain.nodes`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v30_distributed.py:42`
- Alias candidates: `cluster.join` (0.58), `cluster.statistics` (0.57), `cluster.leave` (0.57), `cluster.services` (0.56)
- Source references: `aletheus/distributed_v3/distributed_core.py:121`, `aletheus/distributed_v3/distributed_core.py:136`, `aletheus/distributed_v3/distributed_core.py:143`, `aletheus/distributed_v3/distributed_core.py:158`, `aletheus/distributed_v3/distributed_core.py:167`, `aletheus/distributed_v3/distributed_core.py:182`, `aletheus/distributed_v3/distributed_core.py:191`, `aletheus/distributed_v3/distributed_core.py:220`, `aletheus/runtime/registrations/cluster_commands.py:16`

### `cluster.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.cluster.ClusterDomain.statistics`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v30_distributed.py:92`
- Alias candidates: `state.statistics` (0.60), `learning.statistics` (0.60), `cluster.heartbeat` (0.59), `cluster.leave` (0.57), `cluster.nodes` (0.57)
- Source references: `aletheus/runtime/registrations/cluster_commands.py:20`

### `department.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.enterprise.EnterpriseDomain.department_create`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v21_enterprise.py:30`
- Alias candidates: `tenant.create` (0.59), `team.create` (0.58)
- Source references: `aletheus/enterprise/enterprise_core.py:120`, `aletheus/runtime/registrations/enterprise_commands.py:36`

### `enterprise.bootstrap.cardhawk`

- Registered: `True`
- Handler: `aletheus.runtime.domains.enterprise.EnterpriseDomain.bootstrap_cardhawk`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v21_enterprise.py:11`, `tests/test_aletheus_v21_enterprise.py:65`
- Alias candidates: `knowledge.bootstrap.cardhawk` (0.65)
- Source references: `aletheus/runtime/registrations/enterprise_commands.py:16`

### `enterprise.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.enterprise.EnterpriseDomain.create`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v21_enterprise.py:20`
- Alias candidates: `enterprise.stats` (0.63), `enterprise.list` (0.60), `tenant.create` (0.55)
- Source references: `aletheus/runtime/domains/enterprise.py:21`, `aletheus/runtime/domains/enterprise.py:47`, `aletheus/runtime/domains/enterprise.py:59`, `aletheus/runtime/domains/enterprise.py:73`, `aletheus/runtime/registrations/enterprise_commands.py:21`

### `enterprise.stats`

- Registered: `True`
- Handler: `aletheus.runtime.domains.enterprise.EnterpriseDomain.stats`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v21_enterprise.py:88`
- Alias candidates: `enterprise.list` (0.66), `enterprise.create` (0.63), `event.statistics` (0.55)
- Source references: `aletheus/runtime/domains/enterprise.py:40`, `aletheus/runtime/registrations/enterprise_commands.py:31`

### `event.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.event_adapter.EventCommandAdapter.bootstrap`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v33_event_bus.py:15`
- Alias candidates: `tenant.bootstrap` (0.66), `kernel.bootstrap` (0.62), `reason.bootstrap` (0.62), `telemetry.bootstrap` (0.61), `federation.bootstrap` (0.60)
- Source references: `aletheus/runtime/registrations/event_commands.py:16`

### `event.history`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.event_adapter.EventCommandAdapter.history`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v33_event_bus.py:77`
- Alias candidates: `audit.history` (0.57), `event.statistics` (0.55)
- Source references: `aletheus/runtime/registrations/event_commands.py:40`

### `event.publish`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.event_adapter.EventCommandAdapter.publish`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v33_event_bus.py:29`
- Source references: `aletheus/runtime/registrations/event_commands.py:22`

### `event.replay`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.event_adapter.EventCommandAdapter.replay`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v33_event_bus.py:93`
- Source references: `aletheus/runtime/registrations/event_commands.py:46`

### `event.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.event_adapter.EventCommandAdapter.statistics`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v33_event_bus.py:127`
- Alias candidates: `tenant.statistics` (0.63), `learning.statistics` (0.59), `kernel.statistics` (0.57), `reason.statistics` (0.57), `event.bootstrap` (0.57)
- Source references: `aletheus/runtime/registrations/event_commands.py:52`

### `event.subscribe`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.event_adapter.EventCommandAdapter.subscribe`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v33_event_bus.py:57`
- Alias candidates: `event.unsubscribe` (0.73)
- Source references: `aletheus/runtime/registrations/event_commands.py:28`

### `event.unsubscribe`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.event_adapter.EventCommandAdapter.unsubscribe`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v33_event_bus.py:111`
- Alias candidates: `event.subscribe` (0.73)
- Source references: `aletheus/runtime/registrations/event_commands.py:34`

### `federation.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.domains.federation.FederationDomain.bootstrap`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v34_federation.py:15`
- Alias candidates: `reason.bootstrap` (0.62), `federation.broadcast` (0.60), `event.bootstrap` (0.60), `federation.statistics` (0.59), `kernel.bootstrap` (0.59)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:70`, `aletheus/runtime/registrations/federation_commands.py:13`

### `federation.broadcast`

- Registered: `True`
- Handler: `aletheus.runtime.domains.federation.FederationDomain.broadcast`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v34_federation.py:89`
- Alias candidates: `federation.bootstrap` (0.60), `federation.statistics` (0.59), `federation.join` (0.56), `federation.query` (0.55), `federation.leave` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:74`, `aletheus/runtime/registrations/federation_commands.py:18`

### `federation.discover`

- Registered: `True`
- Handler: `aletheus.runtime.domains.federation.FederationDomain.discover`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v34_federation.py:61`, `tests/test_aletheus_v34_federation.py:107`
- Alias candidates: `federation.query` (0.60), `federation.leave` (0.60), `federation.join` (0.58), `federation.statistics` (0.56), `federation.bootstrap` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:72`, `aletheus/runtime/registrations/federation_commands.py:16`

### `federation.join`

- Registered: `True`
- Handler: `aletheus.runtime.domains.federation.FederationDomain.join`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v34_federation.py:29`
- Alias candidates: `federation.query` (0.58), `federation.statistics` (0.58), `federation.leave` (0.58), `federation.discover` (0.58), `federation.bootstrap` (0.56)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:71`, `aletheus/runtime/registrations/federation_commands.py:14`

### `federation.leave`

- Registered: `True`
- Handler: `aletheus.runtime.domains.federation.FederationDomain.leave`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v34_federation.py:119`
- Alias candidates: `federation.query` (0.60), `federation.statistics` (0.60), `federation.discover` (0.60), `federation.join` (0.58), `federation.bootstrap` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:75`, `aletheus/runtime/registrations/federation_commands.py:15`

### `federation.query`

- Registered: `True`
- Handler: `aletheus.runtime.domains.federation.FederationDomain.query`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v34_federation.py:73`
- Alias candidates: `federation.leave` (0.60), `federation.discover` (0.60), `federation.join` (0.58), `federation.statistics` (0.56), `federation.bootstrap` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:73`, `aletheus/runtime/registrations/federation_commands.py:17`

### `federation.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.federation.FederationDomain.statistics`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v34_federation.py:133`
- Alias candidates: `federation.bootstrap` (0.62), `federation.leave` (0.60), `federation.broadcast` (0.59), `reason.statistics` (0.58), `federation.join` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:76`, `aletheus/runtime/registrations/federation_commands.py:19`

### `governance.check`

- Registered: `True`
- Handler: `aletheus.runtime.domains.enterprise.EnterpriseDomain.governance_check`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v21_enterprise.py:68`
- Alias candidates: `architecture.governance.check` (0.70)
- Source references: `aletheus/runtime/registrations/governance_architecture_commands.py:11`, `aletheus/runtime/registrations/enterprise_commands.py:51`

### `ha.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.domains.high_availability.HighAvailabilityDomain.bootstrap`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v36_high_availability.py:15`
- Alias candidates: `state.bootstrap` (0.65), `reason.bootstrap` (0.63), `tenant.bootstrap` (0.63), `event.bootstrap` (0.60), `kernel.bootstrap` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:87`, `aletheus/runtime/registrations/ha_commands.py:13`

### `ha.failover`

- Registered: `True`
- Handler: `aletheus.runtime.domains.high_availability.HighAvailabilityDomain.failover`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v36_high_availability.py:87`
- Alias candidates: `ha.recover` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:91`, `aletheus/runtime/registrations/ha_commands.py:18`

### `ha.join`

- Registered: `True`
- Handler: `aletheus.runtime.domains.high_availability.HighAvailabilityDomain.join`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v36_high_availability.py:31`
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:88`, `aletheus/runtime/registrations/ha_commands.py:14`

### `ha.replicate`

- Registered: `True`
- Handler: `aletheus.runtime.domains.high_availability.HighAvailabilityDomain.replicate`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v36_high_availability.py:67`
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:90`, `aletheus/runtime/registrations/ha_commands.py:20`

### `ha.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.high_availability.HighAvailabilityDomain.statistics`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v36_high_availability.py:104`
- Alias candidates: `ha.status` (0.73), `state.statistics` (0.60), `learning.statistics` (0.60), `tenant.statistics` (0.57), `reason.statistics` (0.57)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:92`, `aletheus/runtime/registrations/ha_commands.py:22`

### `ha.status`

- Registered: `True`
- Handler: `aletheus.runtime.domains.high_availability.HighAvailabilityDomain.status`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v36_high_availability.py:51`
- Alias candidates: `ha.statistics` (0.73)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:89`, `aletheus/runtime/registrations/ha_commands.py:21`

### `kernel.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.bootstrap`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v40_kernel.py:6`
- Alias candidates: `event.bootstrap` (0.62), `reason.bootstrap` (0.60), `tenant.bootstrap` (0.60), `federation.bootstrap` (0.59), `ha.bootstrap` (0.58)
- Source references: `aletheus/executive_kernel/kernel.py:7`, `aletheus/executive_kernel/__init__.py:1`, `aletheus/runtime/commands_v2/dispatcher.py:53`, `aletheus/runtime/registrations/kernel_commands.py:13`

### `kernel.dispatcher`

- Registered: `True`
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.dispatcher`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v40_kernel.py:79`
- Alias candidates: `kernel.scheduler` (0.59), `kernel.statistics` (0.56)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:57`, `aletheus/runtime/registrations/kernel_commands.py:17`

### `kernel.execute`

- Registered: `True`
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.execute`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v40_kernel.py:20`
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:54`, `aletheus/runtime/registrations/kernel_commands.py:14`

### `kernel.scheduler`

- Registered: `True`
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.scheduler`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v40_kernel.py:60`
- Alias candidates: `kernel.dispatcher` (0.59), `kernel.supervisor` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:56`, `aletheus/runtime/registrations/kernel_commands.py:16`

### `kernel.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.statistics`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v40_kernel.py:114`
- Alias candidates: `kernel.tasks` (0.66), `learning.statistics` (0.63), `kernel.bootstrap` (0.58), `event.statistics` (0.57), `kernel.dispatcher` (0.56)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:59`, `aletheus/runtime/registrations/kernel_commands.py:19`

### `kernel.supervisor`

- Registered: `True`
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.supervisor`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v40_kernel.py:100`
- Alias candidates: `kernel.scheduler` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:58`, `aletheus/runtime/registrations/kernel_commands.py:18`

### `kernel.tasks`

- Registered: `True`
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.tasks`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v40_kernel.py:41`
- Alias candidates: `kernel.statistics` (0.66)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:55`, `aletheus/runtime/registrations/kernel_commands.py:15`

### `knowledge.bootstrap.cardhawk`

- Registered: `True`
- Handler: `aletheus.runtime.domains.knowledge_graph.KnowledgeGraphDomain.bootstrap_cardhawk`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v24_graph.py:64`, `tests/test_aletheus_v25_reasoning.py:17`
- Alias candidates: `enterprise.bootstrap.cardhawk` (0.68)
- Source references: `aletheus/runtime/registrations/knowledge_graph_commands.py:61`

### `knowledge.entity.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.knowledge_graph.KnowledgeGraphDomain.entity_create`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v24_graph.py:11`, `tests/test_aletheus_v24_graph.py:19`
- Alias candidates: `knowledge.entity.update` (0.74), `knowledge.entity.delete` (0.74), `knowledge.relationship.create` (0.68)
- Source references: `aletheus/runtime/registrations/knowledge_graph_commands.py:16`

### `knowledge.infer`

- Registered: `True`
- Handler: `aletheus.runtime.domains.knowledge_graph.KnowledgeGraphDomain.infer`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v24_graph.py:70`
- Alias candidates: `knowledge.search` (0.62), `knowledge.graph` (0.59), `knowledge.neighbors` (0.58), `knowledge.statistics` (0.55)
- Source references: `aletheus/reasoning/reasoning_core.py:69`, `aletheus/runtime/registrations/knowledge_graph_commands.py:56`

### `knowledge.neighbors`

- Registered: `True`
- Handler: `aletheus.runtime.domains.knowledge_graph.KnowledgeGraphDomain.neighbors`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v24_graph.py:54`
- Alias candidates: `knowledge.infer` (0.61), `knowledge.graph` (0.58), `knowledge.search` (0.56)
- Source references: `aletheus/runtime/registrations/knowledge_graph_commands.py:51`

### `knowledge.relationship.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.knowledge_graph.KnowledgeGraphDomain.relationship_create`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v24_graph.py:31`
- Alias candidates: `knowledge.relationship.delete` (0.76), `knowledge.entity.create` (0.68)
- Source references: `aletheus/runtime/registrations/knowledge_graph_commands.py:31`

### `knowledge.search`

- Registered: `True`
- Handler: `aletheus.runtime.domains.knowledge_graph.KnowledgeGraphDomain.search`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v24_graph.py:45`
- Alias candidates: `knowledge.statistics` (0.62), `knowledge.graph` (0.62), `knowledge.infer` (0.62)
- Source references: `aletheus/reasoning/reasoning_core.py:67`, `aletheus/runtime/adapters/graph_adapter.py:62`, `aletheus/runtime/adapters/graph_adapter.py:123`, `aletheus/runtime/handlers/graph_handlers.py:56`, `aletheus/runtime/handlers/graph_handlers.py:113`, `aletheus/runtime/registrations/knowledge_graph_commands.py:41`

### `knowledge.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.knowledge_graph.KnowledgeGraphDomain.statistics`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v24_graph.py:76`
- Alias candidates: `knowledge.search` (0.62), `knowledge.graph` (0.59), `kernel.statistics` (0.55), `knowledge.infer` (0.55)
- Source references: `aletheus/runtime/adapters/graph_adapter.py:178`, `aletheus/runtime/commands/runtime_commands.py:62`, `aletheus/runtime/handlers/graph_handlers.py:155`, `aletheus/runtime/registrations/knowledge_graph_commands.py:66`

### `memory.mesh.cache`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory_mesh.MemoryMeshDomain.cache`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v23_memory_mesh.py:100`
- Alias candidates: `memory.mesh.search` (0.73), `memory.mesh.replicate` (0.69), `memory.mesh.sync` (0.69), `memory.mesh.stats` (0.67), `memory.mesh.store` (0.67)
- Source references: `aletheus/runtime/registrations/memory_mesh_commands.py:23`

### `memory.mesh.history`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory_mesh.MemoryMeshDomain.history`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v23_memory_mesh.py:93`
- Alias candidates: `memory.mesh.store` (0.75), `memory.mesh.restore` (0.72), `memory.mesh.sync` (0.69), `memory.mesh.stats` (0.68), `memory.mesh.cache` (0.64)
- Source references: `aletheus/runtime/registrations/memory_mesh_commands.py:22`

### `memory.mesh.replicate`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory_mesh.MemoryMeshDomain.replicate`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v23_memory_mesh.py:79`
- Alias candidates: `memory.mesh.restore` (0.69), `memory.mesh.cache` (0.69), `memory.mesh.retrieve` (0.68), `memory.mesh.stats` (0.65), `memory.mesh.store` (0.65)
- Source references: `aletheus/runtime/registrations/memory_mesh_commands.py:20`

### `memory.mesh.restore`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory_mesh.MemoryMeshDomain.restore`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v23_memory_mesh.py:59`
- Alias candidates: `memory.mesh.store` (0.79), `memory.mesh.retrieve` (0.74), `memory.mesh.history` (0.72), `memory.mesh.replicate` (0.69), `memory.mesh.stats` (0.68)
- Source references: `aletheus/runtime/registrations/memory_mesh_commands.py:19`

### `memory.mesh.retrieve`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory_mesh.MemoryMeshDomain.retrieve`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v23_memory_mesh.py:25`
- Alias candidates: `memory.mesh.restore` (0.74), `memory.mesh.replicate` (0.68), `memory.mesh.store` (0.67), `memory.mesh.stats` (0.63), `memory.mesh.cache` (0.63)
- Source references: `aletheus/runtime/registrations/memory_mesh_commands.py:16`

### `memory.mesh.search`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory_mesh.MemoryMeshDomain.search`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v23_memory_mesh.py:32`
- Alias candidates: `memory.mesh.cache` (0.73), `memory.mesh.sync` (0.71), `memory.mesh.stats` (0.69), `memory.mesh.store` (0.69), `memory.mesh.snapshot` (0.69)
- Source references: `aletheus/reasoning/reasoning_core.py:68`, `aletheus/runtime/registrations/memory_mesh_commands.py:17`

### `memory.mesh.snapshot`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory_mesh.MemoryMeshDomain.snapshot`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v23_memory_mesh.py:51`
- Alias candidates: `memory.mesh.stats` (0.70), `memory.mesh.search` (0.69), `memory.mesh.sync` (0.68), `memory.mesh.store` (0.67), `memory.mesh.cache` (0.67)
- Source references: `aletheus/runtime/registrations/memory_mesh_commands.py:18`

### `memory.mesh.stats`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory_mesh.MemoryMeshDomain.stats`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v23_memory_mesh.py:109`
- Alias candidates: `memory.stats` (0.77), `memory.mesh.store` (0.71), `memory.mesh.search` (0.69), `memory.mesh.sync` (0.69), `memory.mesh.history` (0.68)
- Source references: `aletheus/runtime/registrations/memory_mesh_commands.py:24`

### `memory.mesh.store`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory_mesh.MemoryMeshDomain.store`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v23_memory_mesh.py:11`, `tests/test_aletheus_v23_memory_mesh.py:41`, `tests/test_aletheus_v23_memory_mesh.py:68`, `tests/test_aletheus_v25_reasoning.py:18`
- Alias candidates: `memory.mesh.restore` (0.79), `memory.mesh.history` (0.75), `memory.mesh.stats` (0.71), `memory.mesh.search` (0.69), `memory.mesh.sync` (0.69)
- Source references: `aletheus/runtime/registrations/memory_mesh_commands.py:15`

### `memory.mesh.sync`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory_mesh.MemoryMeshDomain.sync`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v23_memory_mesh.py:86`
- Alias candidates: `memory.mesh.search` (0.71), `memory.mesh.history` (0.69), `memory.mesh.stats` (0.69), `memory.mesh.store` (0.69), `memory.mesh.cache` (0.69)
- Source references: `aletheus/runtime/registrations/memory_mesh_commands.py:21`

### `memory.recall`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory.MemoryDomain.recall`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_genesis_04.py:31`
- Source references: `aletheus/copilot/copilot_core.py:119`, `aletheus/runtime/domains/memory.py:35`, `aletheus/runtime/registrations/memory_commands.py:25`

### `memory.remember`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory.MemoryDomain.remember`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_genesis_04.py:17`
- Source references: `aletheus/runtime/core.py:424`, `aletheus/runtime/core.py:443`, `aletheus/runtime/core.py:466`, `aletheus/runtime/domains/memory.py:15`, `aletheus/runtime/domains/copilot.py:18`, `aletheus/runtime/domains/prediction.py:46`, `aletheus/runtime/domains/planning.py:22`, `aletheus/runtime/domains/planning.py:57`, `aletheus/runtime/domains/planning.py:81`, `aletheus/runtime/domains/learning.py:24`, `aletheus/runtime/domains/learning.py:46`, `aletheus/runtime/boot_phases/memory_initialization.py:10`, `aletheus/runtime/adapters/graph_adapter.py:37`, `aletheus/runtime/adapters/graph_adapter.py:98`, `aletheus/runtime/adapters/mission_adapter.py:45`, `aletheus/runtime/adapters/mission_adapter.py:107`, `aletheus/runtime/adapters/mission_adapter.py:150`, `aletheus/runtime/handlers/mission_handlers.py:39`, `aletheus/runtime/handlers/mission_handlers.py:101`, `aletheus/runtime/handlers/mission_handlers.py:144`

### `memory.stats`

- Registered: `True`
- Handler: `aletheus.runtime.domains.memory.MemoryDomain.statistics`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_genesis_04.py:47`
- Alias candidates: `memory.mesh.stats` (0.77), `telemetry.statistics` (0.60), `learning.statistics` (0.57), `security.statistics` (0.57), `kernel.statistics` (0.55)
- Source references: `aletheus/runtime/domains/memory.py:50`, `aletheus/runtime/commands/runtime_commands.py:42`, `aletheus/runtime/registrations/memory_commands.py:30`

### `mission.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.mission.MissionDomain.create`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_genesis_07.py:11`
- Alias candidates: `mission.complete` (0.64), `mission.execute` (0.61), `mission.statistics` (0.60), `mission.list` (0.57), `organization.create` (0.55)
- Source references: `aletheus/missions_v2/mission_core.py:52`, `aletheus/runtime/adapters/mission_adapter.py:22`, `aletheus/runtime/handlers/mission_handlers.py:16`, `aletheus/runtime/registrations/mission_v2_commands.py:13`, `aletheus/runtime/registrations/mission_commands.py:16`

### `organization.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.tenancy.TenancyDomain.organization_create`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v39_tenancy.py:33`
- Alias candidates: `organization.update` (0.66), `mission.create` (0.55)
- Source references: `aletheus/enterprise/enterprise_core.py:47`, `aletheus/runtime/commands_v2/dispatcher.py:102`, `aletheus/runtime/registrations/tenancy_commands.py:23`

### `plugin.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.domains.plugin.PluginDomain.bootstrap`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v31_plugins.py:11`
- Alias candidates: `ha.bootstrap` (0.58), `event.bootstrap` (0.58), `security.bootstrap` (0.58), `plugin.status` (0.56), `kernel.bootstrap` (0.56)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:46`, `aletheus/runtime/registrations/plugin_commands.py:15`

### `plugin.disable`

- Registered: `True`
- Handler: `aletheus.runtime.domains.plugin.PluginDomain.disable`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v31_plugins.py:38`
- Alias candidates: `plugin.enable` (0.65), `plugin.install` (0.63), `plugin.update` (0.60), `plugin.list` (0.58), `plugin.statistics` (0.57)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:49`, `aletheus/runtime/registrations/plugin_commands.py:30`

### `plugin.enable`

- Registered: `True`
- Handler: `aletheus.runtime.domains.plugin.PluginDomain.enable`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v31_plugins.py:31`
- Alias candidates: `plugin.disable` (0.65), `plugin.install` (0.60), `plugin.remove` (0.57), `plugin.list` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:48`, `aletheus/runtime/registrations/plugin_commands.py:25`

### `plugin.install`

- Registered: `True`
- Handler: `aletheus.runtime.domains.plugin.PluginDomain.install`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v31_plugins.py:18`
- Alias candidates: `plugin.list` (0.64), `plugin.disable` (0.63), `plugin.statistics` (0.62), `plugin.status` (0.60), `plugin.enable` (0.60)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:47`, `aletheus/runtime/registrations/plugin_commands.py:20`

### `plugin.remove`

- Registered: `True`
- Handler: `aletheus.runtime.domains.plugin.PluginDomain.remove`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v31_plugins.py:45`
- Alias candidates: `plugin.enable` (0.57)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:50`, `aletheus/runtime/registrations/plugin_commands.py:40`

### `plugin.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.plugin.PluginDomain.statistics`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v31_plugins.py:55`
- Alias candidates: `plugin.status` (0.74), `plugin.list` (0.63), `plugin.install` (0.62), `plugin.update` (0.58), `plugin.bootstrap` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:51`, `aletheus/runtime/registrations/plugin_commands.py:55`

### `policy.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.enterprise.EnterpriseDomain.policy_create`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v21_enterprise.py:52`
- Source references: `aletheus/enterprise/enterprise_core.py:167`, `aletheus/runtime/registrations/enterprise_commands.py:46`

### `reason.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.domains.reasoning.ReasoningDomain.bootstrap`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v25_reasoning.py:11`, `tests/test_aletheus_v26_decision_engine.py:17`
- Alias candidates: `tenant.bootstrap` (0.64), `ha.bootstrap` (0.63), `federation.bootstrap` (0.62), `event.bootstrap` (0.62), `kernel.bootstrap` (0.60)
- Source references: `aletheus/runtime/registrations/reasoning_commands.py:20`

### `reason.confidence`

- Registered: `True`
- Handler: `aletheus.runtime.domains.reasoning.ReasoningDomain.confidence`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v25_reasoning.py:53`
- Source references: `aletheus/reason_engine/evaluation.py:69`, `aletheus/reason_engine/statistics.py:36`, `aletheus/reason_engine/justification.py:53`, `aletheus/reason_engine/justification.py:64`, `aletheus/reason_engine/justification.py:75`, `aletheus/reason_engine/justification.py:86`, `aletheus/runtime/registrations/reasoning_commands.py:50`

### `reason.decision`

- Registered: `True`
- Handler: `aletheus.runtime.domains.reasoning.ReasoningDomain.decision`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v25_reasoning.py:41`
- Alias candidates: `reason.explain` (0.56)
- Source references: `aletheus/runtime/registrations/reasoning_commands.py:45`

### `reason.evaluate`

- Registered: `True`
- Handler: `aletheus.runtime.domains.reasoning.ReasoningDomain.evaluate`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_genesis_05.py:44`, `tests/test_aletheus_v25_reasoning.py:28`
- Alias candidates: `reason.statistics` (0.55)
- Source references: `aletheus/decision_v2/decision_core.py:148`, `aletheus/runtime/registrations/reasoning_commands.py:30`

### `reason.explain`

- Registered: `True`
- Handler: `aletheus.runtime.domains.reasoning.ReasoningDomain.explain`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v25_reasoning.py:37`
- Alias candidates: `reason.decision` (0.56), `reason.evaluate` (0.56)
- Source references: `aletheus/runtime/registrations/reasoning_commands.py:35`

### `reason.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.reasoning.ReasoningDomain.statistics`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v25_reasoning.py:58`
- Alias candidates: `learning.statistics` (0.63), `tenant.statistics` (0.60), `reason.trace` (0.60), `mission.statistics` (0.58), `federation.statistics` (0.58)
- Source references: `aletheus/runtime/registrations/reasoning_commands.py:55`

### `reason.trace`

- Registered: `True`
- Handler: `aletheus.runtime.domains.reasoning.ReasoningDomain.trace`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v25_reasoning.py:50`
- Alias candidates: `reason.statistics` (0.60), `reason.bootstrap` (0.58), `reason.evaluate` (0.55)
- Source references: `aletheus/runtime/registrations/reasoning_commands.py:40`

### `runtime.audit`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.audit`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v411_foundation.py:27`
- Alias candidates: `runtime.doctor` (0.60), `runtime.docs` (0.58), `runtime.invariants` (0.58), `runtime.snapshot` (0.56), `runtime.dashboard` (0.55)
- Source references: `aletheus/runtime/core.py:18`, `aletheus/runtime/registrations/governance_commands.py:28`, `aletheus/runtime/registrations/runtime_commands.py:34`

### `runtime.boot.validate`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.boot_validate`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v421_runtime_integrity.py:18`
- Source references: `aletheus/runtime/registrations/runtime_commands.py:58`

### `runtime.dashboard`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.dashboard`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v411_foundation.py:12`
- Alias candidates: `runtime.snapshot` (0.59), `runtime.doctor` (0.58), `runtime.docs` (0.56)
- Source references: `aletheus/runtime/registrations/runtime_commands.py:22`

### `runtime.docs`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.docs`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v411_foundation.py:34`
- Alias candidates: `runtime.doctor` (0.67), `runtime.audit` (0.58), `runtime.dashboard` (0.56)
- Source references: `aletheus/runtime/registrations/runtime_commands.py:40`

### `runtime.doctor`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.doctor`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v421_runtime_integrity.py:6`
- Alias candidates: `runtime.docs` (0.67), `runtime.audit` (0.60), `runtime.dashboard` (0.58), `runtime.snapshot` (0.55)
- Source references: `aletheus/runtime/managers/runtime_facade.py:60`, `aletheus/runtime/registrations/runtime_commands.py:46`

### `runtime.health_report`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.health_report`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v421_runtime_integrity.py:24`
- Source references: `aletheus/runtime/adapter.py:134`, `aletheus/runtime/registrations/runtime_commands.py:64`

### `runtime.invariants`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.invariants`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v421_runtime_integrity.py:12`
- Source references: `aletheus/runtime/certification/certifier.py:70`, `aletheus/runtime/registrations/runtime_commands.py:52`

### `runtime.selftest`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.selftest`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v411_foundation.py:6`
- Source references: `aletheus/runtime/registrations/runtime_commands.py:16`

### `runtime.snapshot`

- Registered: `True`
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.snapshot`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v411_foundation.py:18`
- Alias candidates: `learning.snapshot` (0.59), `state.snapshot` (0.59), `runtime.dashboard` (0.59), `runtime.audit` (0.56), `runtime.selftest` (0.56)
- Source references: `aletheus/runtime/registrations/runtime_commands.py:28`

### `security.audit`

- Registered: `True`
- Handler: `aletheus.runtime.domains.security.SecurityDomain.audit`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v37_security.py:128`
- Alias candidates: `security.statistics` (0.63), `security.authorize` (0.60), `security.authenticate` (0.60), `security.policy` (0.56)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:98`, `aletheus/runtime/registrations/security_commands.py:19`

### `security.authenticate`

- Registered: `True`
- Handler: `aletheus.runtime.domains.security.SecurityDomain.authenticate`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v37_security.py:70`
- Alias candidates: `security.authorize` (0.58), `security.statistics` (0.56), `security.audit` (0.56)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:95`, `aletheus/runtime/registrations/security_commands.py:14`

### `security.authorize`

- Registered: `True`
- Handler: `aletheus.runtime.domains.security.SecurityDomain.authorize`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v37_security.py:88`
- Alias candidates: `security.authenticate` (0.62), `security.audit` (0.60), `security.statistics` (0.56), `security.policy` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:96`, `aletheus/runtime/registrations/security_commands.py:15`

### `security.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.domains.security.SecurityDomain.bootstrap`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v37_security.py:15`
- Alias candidates: `event.bootstrap` (0.59), `state.bootstrap` (0.59), `kernel.bootstrap` (0.58), `tenant.bootstrap` (0.58), `plugin.bootstrap` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:94`, `aletheus/runtime/registrations/security_commands.py:13`

### `security.policy`

- Registered: `True`
- Handler: `aletheus.runtime.domains.security.SecurityDomain.policy`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v37_security.py:107`
- Alias candidates: `security.audit` (0.56), `security.authorize` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:97`, `aletheus/runtime/registrations/security_commands.py:16`

### `security.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.security.SecurityDomain.statistics`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v37_security.py:147`
- Alias candidates: `security.bootstrap` (0.60), `security.audit` (0.58), `memory.stats` (0.57), `security.authenticate` (0.56), `prediction.statistics` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:99`, `aletheus/runtime/registrations/security_commands.py:20`

### `state.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.domains.persistence.PersistenceDomain.bootstrap`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v32_persistence.py:13`
- Alias candidates: `ha.bootstrap` (0.65), `tenant.bootstrap` (0.62), `event.bootstrap` (0.59), `security.bootstrap` (0.59), `kernel.bootstrap` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:61`, `aletheus/runtime/registrations/state_commands.py:15`

### `state.export`

- Registered: `True`
- Handler: `aletheus.runtime.domains.persistence.PersistenceDomain.export`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v32_persistence.py:71`
- Alias candidates: `state.import` (0.66), `state.restore` (0.58), `state.snapshot` (0.57)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:66`, `aletheus/runtime/registrations/state_commands.py:40`

### `state.import`

- Registered: `True`
- Handler: `aletheus.runtime.domains.persistence.PersistenceDomain.import_state`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v32_persistence.py:78`
- Alias candidates: `state.export` (0.66), `state.snapshot` (0.57)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:67`, `aletheus/runtime/registrations/state_commands.py:45`

### `state.load`

- Registered: `True`
- Handler: `aletheus.runtime.domains.persistence.PersistenceDomain.load`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v32_persistence.py:34`
- Alias candidates: `state.save` (0.57), `state.statistics` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:63`, `aletheus/runtime/registrations/state_commands.py:25`

### `state.restore`

- Registered: `True`
- Handler: `aletheus.runtime.domains.persistence.PersistenceDomain.restore`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v32_persistence.py:57`
- Alias candidates: `state.export` (0.58), `state.statistics` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:65`, `aletheus/runtime/registrations/state_commands.py:35`

### `state.save`

- Registered: `True`
- Handler: `aletheus.runtime.domains.persistence.PersistenceDomain.save`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v32_persistence.py:27`
- Alias candidates: `state.statistics` (0.61), `state.load` (0.57), `state.restore` (0.57), `state.snapshot` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:62`, `aletheus/runtime/registrations/state_commands.py:20`

### `state.snapshot`

- Registered: `True`
- Handler: `aletheus.runtime.domains.persistence.PersistenceDomain.snapshot`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v32_persistence.py:46`
- Alias candidates: `runtime.snapshot` (0.59), `state.statistics` (0.58), `learning.snapshot` (0.58), `registry.snapshot` (0.58), `state.export` (0.57)
- Source references: `aletheus/intelligence_singularity/engine.py:58`, `aletheus/runtime/commands_v2/dispatcher.py:64`, `aletheus/runtime/registrations/state_commands.py:30`

### `state.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.persistence.PersistenceDomain.statistics`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v32_persistence.py:90`
- Alias candidates: `state.save` (0.61), `cluster.statistics` (0.60), `ha.statistics` (0.60), `tenant.statistics` (0.57), `state.bootstrap` (0.57)
- Source references: `aletheus/neural/envelope/statistics.py:15`, `aletheus/runtime/commands_v2/dispatcher.py:68`, `aletheus/runtime/registrations/state_commands.py:50`

### `team.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.enterprise.EnterpriseDomain.team_create`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v21_enterprise.py:41`
- Alias candidates: `tenant.create` (0.66)
- Source references: `aletheus/enterprise/enterprise_core.py:141`, `aletheus/runtime/registrations/enterprise_commands.py:41`

### `telemetry.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.domains.telemetry.TelemetryDomain.bootstrap`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v35_telemetry.py:15`
- Alias candidates: `telemetry.trace` (0.61), `tenant.bootstrap` (0.60), `telemetry.statistics` (0.58), `state.bootstrap` (0.58), `telemetry.log` (0.56)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:78`, `aletheus/runtime/registrations/telemetry_commands.py:13`

### `telemetry.health`

- Registered: `True`
- Handler: `aletheus.runtime.domains.telemetry.TelemetryDomain.health`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v35_telemetry.py:111`
- Alias candidates: `telemetry.statistics` (0.62), `telemetry.log` (0.61), `telemetry.metric` (0.60), `registry.health` (0.58), `telemetry.trace` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:83`, `aletheus/runtime/registrations/telemetry_commands.py:18`

### `telemetry.log`

- Registered: `True`
- Handler: `aletheus.runtime.domains.telemetry.TelemetryDomain.log`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v35_telemetry.py:69`
- Alias candidates: `telemetry.health` (0.61), `telemetry.record` (0.61), `telemetry.statistics` (0.58), `telemetry.trace` (0.58), `telemetry.timeline` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:81`, `aletheus/runtime/registrations/telemetry_commands.py:16`

### `telemetry.metric`

- Registered: `True`
- Handler: `aletheus.runtime.domains.telemetry.TelemetryDomain.metric`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v35_telemetry.py:29`
- Alias candidates: `telemetry.trace` (0.66), `telemetry.timeline` (0.61), `telemetry.health` (0.60), `telemetry.record` (0.60), `telemetry.statistics` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:79`, `aletheus/runtime/registrations/telemetry_commands.py:15`

### `telemetry.record`

- Registered: `True`
- Handler: `aletheus.runtime.domains.telemetry.TelemetryDomain.record`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v35_telemetry.py:53`
- Alias candidates: `telemetry.trace` (0.62), `telemetry.log` (0.61), `telemetry.metric` (0.60), `learning.record` (0.58), `telemetry.health` (0.56)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:80`, `aletheus/runtime/registrations/telemetry_commands.py:14`

### `telemetry.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.telemetry.TelemetryDomain.statistics`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v35_telemetry.py:151`
- Alias candidates: `telemetry.trace` (0.64), `telemetry.bootstrap` (0.61), `memory.stats` (0.60), `telemetry.log` (0.58), `telemetry.health` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:85`, `aletheus/runtime/registrations/telemetry_commands.py:20`

### `telemetry.timeline`

- Registered: `True`
- Handler: `aletheus.runtime.domains.telemetry.TelemetryDomain.timeline`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v35_telemetry.py:131`
- Alias candidates: `telemetry.metric` (0.61), `telemetry.trace` (0.59), `telemetry.log` (0.58), `telemetry.statistics` (0.55)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:84`, `aletheus/runtime/registrations/telemetry_commands.py:19`

### `telemetry.trace`

- Registered: `True`
- Handler: `aletheus.runtime.domains.telemetry.TelemetryDomain.trace`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v35_telemetry.py:91`
- Alias candidates: `telemetry.metric` (0.66), `telemetry.statistics` (0.64), `telemetry.record` (0.62), `telemetry.bootstrap` (0.61), `telemetry.timeline` (0.59)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:82`, `aletheus/runtime/registrations/telemetry_commands.py:17`

### `tenant.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.domains.tenancy.TenancyDomain.bootstrap`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v39_tenancy.py:15`
- Alias candidates: `event.bootstrap` (0.66), `ha.bootstrap` (0.63), `state.bootstrap` (0.62), `kernel.bootstrap` (0.60), `reason.bootstrap` (0.60)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:101`, `aletheus/runtime/registrations/tenancy_commands.py:13`

### `tenant.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.tenancy.TenancyDomain.create`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v39_tenancy.py:57`
- Alias candidates: `team.create` (0.66), `tenant.health` (0.62), `tenant.delete` (0.62), `department.create` (0.59), `tenant.statistics` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:103`, `aletheus/runtime/registrations/tenancy_commands.py:14`

### `tenant.health`

- Registered: `True`
- Handler: `aletheus.runtime.domains.tenancy.TenancyDomain.health`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v39_tenancy.py:119`, `tests/test_aletheus_v40_kernel.py:155`
- Alias candidates: `tenant.create` (0.62), `tenant.select` (0.62), `tenant.delete` (0.62), `tenant.list` (0.60), `tenant.statistics` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:106`, `aletheus/runtime/registrations/tenancy_commands.py:27`

### `tenant.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.tenancy.TenancyDomain.statistics`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v39_tenancy.py:105`
- Alias candidates: `event.statistics` (0.63), `tenant.list` (0.63), `tenant.create` (0.58), `tenant.select` (0.58), `tenant.bootstrap` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:105`, `aletheus/runtime/registrations/tenancy_commands.py:26`

### `workflow.bootstrap`

- Registered: `True`
- Handler: `aletheus.runtime.domains.workflow.WorkflowDomain.bootstrap`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v28_workflows.py:11`
- Alias candidates: `workflow.start` (0.60), `workflow.status` (0.59), `kernel.bootstrap` (0.58), `workflow.statistics` (0.56), `ha.bootstrap` (0.55)
- Source references: `aletheus/runtime/registrations/workflow_v2_commands.py:13`, `aletheus/runtime/registrations/workflow_commands.py:15`

### `workflow.cancel`

- Registered: `True`
- Handler: `aletheus.runtime.domains.workflow.WorkflowDomain.cancel`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v28_workflows.py:52`
- Alias candidates: `workflow.create` (0.64), `workflow.pause` (0.61), `workflow.start` (0.56), `workflow.statistics` (0.56), `workflow.resume` (0.55)
- Source references: `aletheus/workflows_v2/workflow_core.py:290`, `aletheus/workflow_v3/workflow_core.py:143`, `aletheus/runtime/registrations/workflow_v2_commands.py:18`, `aletheus/runtime/registrations/workflow_commands.py:40`

### `workflow.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.workflow.WorkflowDomain.create`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v28_workflows.py:17`
- Alias candidates: `workflow.resume` (0.64), `workflow.start` (0.61), `workflow.statistics` (0.61), `workflow.cancel` (0.59), `workflow.status` (0.59)
- Source references: `aletheus/workflows_v2/workflow_core.py:142`, `aletheus/runtime/registrations/workflow_v2_commands.py:14`, `aletheus/runtime/registrations/workflow_commands.py:20`

### `workflow.pause`

- Registered: `True`
- Handler: `aletheus.runtime.domains.workflow.WorkflowDomain.pause`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v28_workflows.py:38`
- Alias candidates: `workflow.status` (0.65), `workflow.statistics` (0.63), `workflow.resume` (0.61), `workflow.create` (0.61), `workflow.cancel` (0.61)
- Source references: `aletheus/workflows_v2/workflow_core.py:274`, `aletheus/workflow_v3/workflow_core.py:127`, `aletheus/runtime/registrations/workflow_v2_commands.py:16`, `aletheus/runtime/registrations/workflow_commands.py:30`

### `workflow.resume`

- Registered: `True`
- Handler: `aletheus.runtime.domains.workflow.WorkflowDomain.resume`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v28_workflows.py:45`
- Alias candidates: `workflow.create` (0.64), `workflow.status` (0.59), `workflow.pause` (0.56), `workflow.start` (0.56), `workflow.statistics` (0.56)
- Source references: `aletheus/workflows_v2/workflow_core.py:282`, `aletheus/workflow_v3/workflow_core.py:135`, `aletheus/runtime/registrations/workflow_v2_commands.py:17`, `aletheus/runtime/registrations/workflow_commands.py:35`

### `workflow.start`

- Registered: `True`
- Handler: `aletheus.runtime.domains.workflow.WorkflowDomain.start`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v28_workflows.py:31`
- Alias candidates: `workflow.statistics` (0.72), `workflow.status` (0.70), `workflow.bootstrap` (0.60), `workflow.pause` (0.58), `workflow.resume` (0.56)
- Source references: `aletheus/runtime/workflow.py:30`, `aletheus/workflows_v2/workflow_core.py:206`, `aletheus/workflows_v2/workflow_core.py:207`, `aletheus/workflow_v3/workflow_core.py:119`, `aletheus/runtime/registrations/workflow_v2_commands.py:15`, `aletheus/runtime/registrations/workflow_commands.py:25`

### `workflow.statistics`

- Registered: `True`
- Handler: `aletheus.runtime.domains.workflow.WorkflowDomain.statistics`
- Invocation mode: `context`
- Tests: `tests/test_aletheus_v28_workflows.py:62`
- Alias candidates: `workflow.status` (0.74), `workflow.start` (0.72), `workflow.create` (0.61), `workflow.bootstrap` (0.60), `workflow.pause` (0.58)
- Source references: `aletheus/runtime/registrations/workflow_v2_commands.py:20`, `aletheus/runtime/registrations/workflow_commands.py:50`

### `workspace.create`

- Registered: `True`
- Handler: `aletheus.runtime.domains.tenancy.TenancyDomain.workspace_create`
- Invocation mode: `payload`
- Tests: `tests/test_aletheus_v39_tenancy.py:86`
- Alias candidates: `workspace.delete` (0.64), `workspace.list` (0.59), `workflow.create` (0.58)
- Source references: `aletheus/runtime/commands_v2/dispatcher.py:104`, `aletheus/runtime/registrations/tenancy_commands.py:19`
