# Genesis 7 Runtime Core Responsibility Audit

Generated: `2026-07-10T08:18:38.175705+00:00`

- File: `aletheus/runtime/core.py`
- Total file lines: **1384**
- Runtime methods: **94**
- Implementation-pressure score: **15.17%**

## Responsibility Summary

| Classification | Methods |
|---|---:|
| COMPOSITION | 2 |
| REGISTRATION | 10 |
| DELEGATION | 4 |
| OBSERVABILITY | 50 |
| IMPLEMENTATION | 28 |
| UNKNOWN | 0 |

## Method Classification

| Method | Line | Lines | Classification | Reason |
|---|---:|---:|---|---|
| `__init__` | 133 | 207 | COMPOSITION | recognized composition/lifecycle method |
| `boot` | 342 | 11 | COMPOSITION | recognized composition/lifecycle method |
| `register_engine` | 355 | 3 | REGISTRATION | registration/bootstrap naming |
| `register_service` | 359 | 10 | REGISTRATION | registration/bootstrap naming |
| `register_pipeline` | 370 | 3 | REGISTRATION | registration/bootstrap naming |
| `register_workflow` | 374 | 3 | REGISTRATION | registration/bootstrap naming |
| `bootstrap_registry` | 379 | 35 | REGISTRATION | registration/bootstrap naming |
| `_cmd_goal_create` | 415 | 18 | IMPLEMENTATION | runtime command handler |
| `_cmd_goal_complete` | 434 | 4 | IMPLEMENTATION | runtime command handler |
| `_cmd_goal_list` | 439 | 13 | IMPLEMENTATION | runtime command handler |
| `_cmd_reason_history` | 453 | 3 | IMPLEMENTATION | runtime command handler |
| `_cmd_decision_record` | 457 | 18 | IMPLEMENTATION | runtime command handler |
| `_cmd_decision_history` | 476 | 3 | IMPLEMENTATION | runtime command handler |
| `_cmd_cognition_stats` | 480 | 3 | IMPLEMENTATION | runtime command handler |
| `_cmd_event_bootstrap` | 500 | 6 | REGISTRATION | registration/bootstrap naming |
| `_cmd_event_publish` | 507 | 15 | IMPLEMENTATION | runtime command handler |
| `_cmd_event_subscribe` | 523 | 13 | IMPLEMENTATION | runtime command handler |
| `_cmd_event_unsubscribe` | 537 | 13 | IMPLEMENTATION | runtime command handler |
| `_cmd_event_history` | 551 | 10 | IMPLEMENTATION | runtime command handler |
| `_cmd_event_replay` | 562 | 10 | IMPLEMENTATION | runtime command handler |
| `_cmd_event_statistics` | 573 | 8 | IMPLEMENTATION | runtime command handler |
| `_bootstrap_compatibility` | 611 | 5 | REGISTRATION | registration/bootstrap naming |
| `_register_compatibility_services` | 617 | 4 | REGISTRATION | registration/bootstrap naming |
| `_apply_compatibility_aliases` | 622 | 4 | DELEGATION | small forwarding method |
| `_cmd_registry_inspect` | 636 | 8 | IMPLEMENTATION | runtime command handler |
| `_register_runtime_domains` | 647 | 31 | REGISTRATION | registration/bootstrap naming |
| `_bootstrap_runtime_registry` | 680 | 51 | REGISTRATION | registration/bootstrap naming |
| `_cmd_runtime_selftest` | 732 | 3 | IMPLEMENTATION | runtime command handler |
| `_cmd_runtime_dashboard` | 736 | 3 | IMPLEMENTATION | runtime command handler |
| `_cmd_runtime_snapshot` | 740 | 3 | IMPLEMENTATION | runtime command handler |
| `_cmd_runtime_audit` | 744 | 3 | IMPLEMENTATION | runtime command handler |
| `_cmd_runtime_docs` | 748 | 4 | IMPLEMENTATION | runtime command handler |
| `_cmd_runtime_doctor` | 758 | 3 | IMPLEMENTATION | runtime command handler |
| `_cmd_runtime_invariants` | 762 | 3 | IMPLEMENTATION | runtime command handler |
| `_cmd_runtime_boot_validate` | 766 | 3 | IMPLEMENTATION | runtime command handler |
| `_cmd_runtime_health_report` | 770 | 3 | IMPLEMENTATION | runtime command handler |
| `_job_runtime_pulse` | 775 | 10 | DELEGATION | small forwarding method |
| `health` | 788 | 9 | OBSERVABILITY | observability or validation naming |
| `genesis6_validate` | 807 | 9 | OBSERVABILITY | observability or validation naming |
| `genesis6_freeze_review` | 817 | 8 | DELEGATION | delegates through attached components: 1 call(s) |
| `boot_certification_validate` | 828 | 9 | OBSERVABILITY | observability or validation naming |
| `governance_record` | 838 | 13 | DELEGATION | delegates through attached components: 1 call(s) |
| `registry_snapshot` | 858 | 9 | OBSERVABILITY | observability or validation naming |
| `_cmd_spa_assess` | 870 | 6 | IMPLEMENTATION | runtime command handler |
| `_cmd_spa_drift` | 878 | 6 | IMPLEMENTATION | runtime command handler |
| `_cmd_architecture_governance_check` | 888 | 11 | IMPLEMENTATION | runtime command handler |
| `_cmd_architecture_validate` | 901 | 10 | IMPLEMENTATION | runtime command handler |
| `_cmd_runtime_audit` | 913 | 10 | IMPLEMENTATION | runtime command handler |
| `command_surface_audit` | 927 | 15 | OBSERVABILITY | observability or validation naming |
| `anchor_governance_status` | 945 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_lifecycle_status` | 954 | 14 | OBSERVABILITY | observability or validation naming |
| `anchor_dependency_status` | 971 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_contract_status` | 980 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_discovery_status` | 989 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_healing_status` | 998 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_intelligence_status` | 1007 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_optimization_status` | 1016 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_learning_status` | 1025 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_predictive_status` | 1034 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_constitution_status` | 1043 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_simulation_status` | 1052 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_research_status` | 1061 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_proposal_status` | 1070 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_negotiation_status` | 1079 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_execution_status` | 1088 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_verification_status` | 1097 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_evolution_graph_status` | 1106 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_analytics_status` | 1115 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_strategy_status` | 1124 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_portfolio_status` | 1133 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_resource_status` | 1142 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_performance_status` | 1151 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_improvement_status` | 1160 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_architect_status` | 1169 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_architecture_simulator_status` | 1178 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_architecture_selection_status` | 1187 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_deployment_status` | 1196 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_migration_status` | 1205 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_continuity_status` | 1214 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_institutional_memory_status` | 1223 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_pattern_status` | 1232 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_forecasting_status` | 1241 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_steward_status` | 1250 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_constitution_reasoning_status` | 1259 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_council_status` | 1268 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_consensus_status` | 1277 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_judgment_status` | 1286 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_meta_reasoning_status` | 1295 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_cognitive_status` | 1304 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_cognitive_optimization_status` | 1313 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_cognitive_self_improvement_status` | 1322 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_cognitive_architect_status` | 1331 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_cognitive_simulation_status` | 1340 | 6 | OBSERVABILITY | observability or validation naming |
| `anchor_cognitive_selection_status` | 1349 | 6 | OBSERVABILITY | observability or validation naming |

## Highest-Priority Extraction Candidates

| Method | Classification | Lines | Recommended Direction |
|---|---|---:|---|
| `_cmd_goal_create` | IMPLEMENTATION | 18 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_decision_record` | IMPLEMENTATION | 18 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_event_publish` | IMPLEMENTATION | 15 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_goal_list` | IMPLEMENTATION | 13 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_event_subscribe` | IMPLEMENTATION | 13 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_event_unsubscribe` | IMPLEMENTATION | 13 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_architecture_governance_check` | IMPLEMENTATION | 11 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_event_history` | IMPLEMENTATION | 10 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_event_replay` | IMPLEMENTATION | 10 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_architecture_validate` | IMPLEMENTATION | 10 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_runtime_audit` | IMPLEMENTATION | 10 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_event_statistics` | IMPLEMENTATION | 8 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_registry_inspect` | IMPLEMENTATION | 8 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_spa_assess` | IMPLEMENTATION | 6 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_spa_drift` | IMPLEMENTATION | 6 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_goal_complete` | IMPLEMENTATION | 4 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_runtime_docs` | IMPLEMENTATION | 4 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_reason_history` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_decision_history` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_cognition_stats` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_runtime_selftest` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_runtime_dashboard` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_runtime_snapshot` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_runtime_audit` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_runtime_doctor` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_runtime_invariants` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_runtime_boot_validate` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |
| `_cmd_runtime_health_report` | IMPLEMENTATION | 3 | Move handler logic into command-family component; retain thin compatibility delegate if needed |

## Certification Interpretation

- **0–10% pressure:** composition root is highly disciplined.
- **10–20% pressure:** generally healthy; targeted extraction recommended.
- **20–35% pressure:** meaningful implementation accumulation exists.
- **Above 35%:** strong God Object pressure; freeze should be withheld.

This score is a heuristic. Manual review remains authoritative.
