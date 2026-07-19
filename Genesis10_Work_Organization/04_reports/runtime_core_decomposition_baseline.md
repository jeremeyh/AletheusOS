========================================================
ALETHEUSOS RUNTIME CORE DECOMPOSITION PLAN
========================================================

Core Path........................aletheus/runtime/core.py
Line Count.......................3572
Functions........................328
Classes..........................1
Imports..........................56

Responsibilities Identified......12
Runtime Compression Index........92.51%

Responsibility Migration Map
  - workflow: 549 signals -> Workflow Circuit / Mission Registry (confidence 0.99)
  - commands: 478 signals -> Command Registry (confidence 0.99)
  - applications: 425 signals -> Application Registry / Application Circuit (confidence 0.99)
  - registration: 295 signals -> Runtime Registry (confidence 0.99)
  - memory: 237 signals -> Memory Circuit (confidence 0.99)
  - events: 169 signals -> Relay Network / Event Fabric (confidence 0.99)
  - services: 131 signals -> Service Manager / Service Mesh (confidence 0.99)
  - lifecycle: 117 signals -> Executive Kernel (confidence 0.99)
  - metrics: 101 signals -> Platform Intelligence (confidence 0.99)
  - governance: 34 signals -> Governance Circuit (confidence 0.89)
  - routing: 19 signals -> Service Mesh / Relay Network (confidence 0.74)
  - optimization: 5 signals -> Catalyst (confidence 0.6)

Largest Functions
  - boot at line 176 (397 lines)
  - __init__ at line 86 (88 lines)
  - _cmd_health at line 597 (67 lines)
  - _register_compatibility_services at line 3373 (33 lines)
  - _apply_compatibility_aliases at line 3407 (30 lines)
  - _cmd_kernel_dispatcher at line 3309 (28 lines)
  - _cmd_compat_resolve at line 3451 (25 lines)
  - _cmd_diagnostics at line 665 (24 lines)
  - _cmd_mission_create at line 914 (24 lines)
  - _cmd_compat_contract at line 3477 (23 lines)
  - _cmd_kernel_scheduler at line 3285 (22 lines)
  - _cmd_application_install at line 1140 (21 lines)
  - _job_runtime_pulse at line 3549 (21 lines)
  - _cmd_application_register at line 1068 (20 lines)
  - _cmd_cardhawk_foundation_bootstrap at line 1204 (20 lines)

========================================================
