# Genesis 11 RUF012 AST Analysis

## Summary

- Repository: `/Users/master_lord_6ixth/Development/AletheusOS`
- Python files discovered: **6478**
- Files parsed successfully: **6478**
- Syntax/read failures: **0**
- Mutable class attributes found: **90**
- Safe `ClassVar` candidates: **64**
- Shared-state candidates: **23**
- Manual-review candidates: **3**

## Candidates

| File | Class | Attribute | Type | Line | Classification |
|---|---|---|---:|---:|---|
| `core/engine_base.py` | `EngineBase` | `events` | `list` | 15 | `manual-review` |
| `intelligence/projections/base.py` | `Projection` | `events` | `list` | 13 | `manual-review` |
| `timeline/engine/timeline_projection.py` | `TimelineProjection` | `events` | `list` | 9 | `manual-review` |
| `Genesis14_SPAN_Constitutional_Intelligence/package/aletheus/span/constitutional_context.py` | `ProjectInspector` | `EXCLUDED_PARTS` | `set` | 74 | `safe-classvar` |
| `adaptive_intelligence/deployment/deployment_profiles.py` | `DeploymentProfiles` | `PROFILES` | `dict` | 4 | `safe-classvar` |
| `aletheus/application_runtime/services.py` | `ApplicationServiceResolver` | `SERVICE_NAMES` | `set` | 19 | `safe-classvar` |
| `aletheus/apps/demo/application.py` | `DemoApplication` | `PERMISSIONS` | `list` | 11 | `safe-classvar` |
| `aletheus/apps/demo/application.py` | `DemoApplication` | `SERVICES` | `list` | 16 | `safe-classvar` |
| `aletheus/apps/demo/application.py` | `DemoApplication` | `DEPENDENCIES` | `list` | 20 | `safe-classvar` |
| `aletheus/civilization/adapters.py` | `SecurityCivilizationAdapter` | `EVENT_EVIDENCE_MAP` | `dict` | 26 | `safe-classvar` |
| `aletheus/constitutional_memory/precedent.py` | `ConstitutionalPrecedentEngine` | `PRECEDENT_ORDER` | `dict` | 8 | `safe-classvar` |
| `aletheus/neural/state/manager.py` | `BrainStateManager` | `VALID_STATES` | `set` | 12 | `safe-classvar` |
| `aletheus/overlay_manager/validation.py` | `OverlayValidator` | `RESERVED_TERMS` | `set` | 8 | `safe-classvar` |
| `aletheus/platform/platform_layer.py` | `PlatformLayer` | `REQUIRED_DIRS` | `list` | 22 | `safe-classvar` |
| `aletheus/platform/platform_layer.py` | `PlatformLayer` | `REQUIRED_TOOLS` | `list` | 30 | `safe-classvar` |
| `aletheus/platform/platform_layer.py` | `PlatformLayer` | `OPTIONAL_TOOLS` | `list` | 34 | `safe-classvar` |
| `aletheus/platform_intelligence/engine.py` | `PlatformIntelligenceEngine` | `IGNORED_DIRS` | `set` | 14 | `safe-classvar` |
| `aletheus/platform_intelligence/runtime_health.py` | `RuntimeHealthService` | `STAT_FIELDS` | `list` | 11 | `safe-classvar` |
| `aletheus/platform_intelligence/runtime_snapshot.py` | `RuntimeSnapshotService` | `COMPONENTS` | `list` | 13 | `safe-classvar` |
| `aletheus/platform_lifecycle/state.py` | `PlatformStateEngine` | `VALID_STATES` | `set-comprehension` | 23 | `safe-classvar` |
| `aletheus/repository_dna/collision_auditor.py` | `RepositoryDNACollisionAuditor` | `KNOWN_CLUSTERS` | `dict` | 11 | `safe-classvar` |
| `aletheus/runtime/commands_v2/dispatcher.py` | `CompiledRuntimeCommandDispatcher` | `RESULT_KEY_CONTRACTS` | `dict` | 45 | `safe-classvar` |
| `aletheus/runtime/compatibility_layer/layer.py` | `CompatibilityLayer` | `SERVICE_REGISTRY` | `list` | 12 | `safe-classvar` |
| `aletheus/runtime/compatibility_layer/layer.py` | `CompatibilityLayer` | `SAFE_ALIASES` | `list` | 30 | `safe-classvar` |
| `aletheus/runtime/decomposition/responsibility.py` | `ResponsibilityExtractor` | `RESPONSIBILITIES` | `dict` | 11 | `safe-classvar` |
| `aletheus/runtime_supervisor/core.py` | `RuntimeSupervisor` | `WATCHED_EVENTS` | `list` | 14 | `safe-classvar` |
| `aletheus/sdk/application.py` | `Application` | `PERMISSIONS` | `list` | 18 | `safe-classvar` |
| `aletheus/sdk/application.py` | `Application` | `SERVICES` | `list` | 19 | `safe-classvar` |
| `aletheus/sdk/application.py` | `Application` | `DEPENDENCIES` | `list` | 20 | `safe-classvar` |
| `aletheus/span/constitutional_context.py` | `ProjectInspector` | `EXCLUDED_PARTS` | `set` | 74 | `safe-classvar` |
| `aletheus/spectrum_platform_analyzer/boundary_analysis.py` | `BoundaryAnalyzer` | `ALLOWED` | `dict` | 25 | `safe-classvar` |
| `architecture/import_migrator.py` | `ImportMigrator` | `REPLACEMENTS` | `dict` | 12 | `safe-classvar` |
| `architecture/project_auditor.py` | `ProjectAuditor` | `DEPRECATED_PATTERNS` | `dict` | 35 | `safe-classvar` |
| `asset_core/runtime/image_service.py` | `AssetImageService` | `IMAGE_FIELDS` | `list` | 8 | `safe-classvar` |
| `asset_core/runtime/image_service.py` | `AssetImageService` | `EXTENSIONS` | `list` | 14 | `safe-classvar` |
| `asset_core/workflows/asset_pipeline.py` | `AssetPipeline` | `STAGES` | `list` | 7 | `safe-classvar` |
| `card_hawk/assets/categories.py` | `AssetCategories` | `TYPES` | `list` | 11 | `safe-classvar` |
| `card_hawk/assets/lifecycle.py` | `AssetLifecycle` | `STATES` | `list` | 11 | `safe-classvar` |
| `card_hawk/collector_app/subscriptions.py` | `SubscriptionEngine` | `TIERS` | `list` | 11 | `safe-classvar` |
| `card_hawk/founder_console/modules.py` | `ConsoleModules` | `MODULES` | `list` | 11 | `safe-classvar` |
| `card_hawk/universal_collectibles/categories.py` | `Categories` | `TYPES` | `list` | 11 | `safe-classvar` |
| `cardhawkos/config/settings.py` | `Settings` | `FEATURE_FLAGS` | `dict` | 23 | `safe-classvar` |
| `commercial/commercial_readiness.py` | `CommercialReadiness` | `CHECKS` | `dict` | 4 | `safe-classvar` |
| `commercialization/permissions.py` | `Permissions` | `ROLE_PERMISSIONS` | `dict` | 2 | `safe-classvar` |
| `core/config.py` | `Config` | `FEATURE_FLAGS` | `dict` | 20 | `safe-classvar` |
| `hawk_aeye/brand_detector.py` | `BrandDetector` | `KNOWN_BRANDS` | `list` | 4 | `safe-classvar` |
| `hawk_aeye/parallel_detector.py` | `ParallelDetector` | `KNOWN_PARALLELS` | `list` | 4 | `safe-classvar` |
| `hawk_aeye/player_detector.py` | `PlayerDetector` | `KNOWN_PLAYERS` | `list` | 4 | `safe-classvar` |
| `intelligence_convergence/engines/digital_twin_2.py` | `DigitalTwin2` | `SCENARIOS` | `dict` | 7 | `safe-classvar` |
| `marketplace/connectors/manager.py` | `MarketplaceManager` | `PROVIDERS` | `list` | 14 | `safe-classvar` |
| `scheduler/runtime_scheduler.py` | `RuntimeScheduler` | `DEFAULT_JOBS` | `list` | 9 | `safe-classvar` |
| `security/config_validator.py` | `ConfigValidator` | `REQUIRED_DIRS` | `list` | 7 | `safe-classvar` |
| `thorx/liquidity.py` | `LiquidityScorer` | `PREMIUM_BRANDS` | `set` | 4 | `safe-classvar` |
| `thorx/market_strength.py` | `MarketStrengthScorer` | `HOT_SPORTS` | `set` | 4 | `safe-classvar` |
| `thorx/market_strength.py` | `MarketStrengthScorer` | `CORE_TEAMS` | `set` | 5 | `safe-classvar` |
| `thorx/player_thesis.py` | `PlayerThesisScorer` | `HIGH_CONVICTION` | `dict` | 4 | `safe-classvar` |
| `thorx/portfolio_fit.py` | `PortfolioFitScorer` | `CORE_TEAMS` | `set` | 4 | `safe-classvar` |
| `thorx/risk.py` | `RiskScorer` | `RISKY_BRANDS` | `set` | 4 | `safe-classvar` |
| `thorx/score.py` | `ThorxScore` | `WEIGHTS` | `dict` | 17 | `safe-classvar` |
| `thorx/visual_appeal.py` | `VisualAppealScorer` | `PREMIUM_PARALLELS` | `list` | 4 | `safe-classvar` |
| `tools/repository/rules.py` | `RepositoryPolicy` | `DEFAULT_ALLOWED_ROOT_FILES` | `set` | 24 | `safe-classvar` |
| `watch_tower/runtime/engine.py` | `WatchTowerEngine` | `SAFE_DELETE_NAMES` | `set` | 24 | `safe-classvar` |
| `watch_tower/runtime/engine.py` | `WatchTowerEngine` | `SAFE_DELETE_DIRS` | `set` | 28 | `safe-classvar` |
| `watch_tower/runtime/engine.py` | `WatchTowerEngine` | `REQUIRED_ROOT_FILES` | `list` | 35 | `safe-classvar` |
| `watch_tower/runtime/engine.py` | `WatchTowerEngine` | `REQUIRED_ROOT_DIRS` | `list` | 41 | `safe-classvar` |
| `watch_tower/runtime/engine.py` | `WatchTowerEngine` | `SUSPICIOUS_NAMES` | `list` | 49 | `safe-classvar` |
| `workflow_automation/workflow_service.py` | `WorkflowAutomationService` | `TEMPLATES` | `dict` | 24 | `safe-classvar` |
| `adaptive_intelligence/feedback/feedback_loop.py` | `IntelligenceFeedbackLoop` | `_feedback` | `list` | 21 | `shared-class-state` |
| `adaptive_intelligence/plugins/plugin_framework.py` | `PluginRegistry` | `_plugins` | `dict` | 16 | `shared-class-state` |
| `adaptive_intelligence/research/research_workspace.py` | `ResearchWorkspace` | `_notes` | `list` | 19 | `shared-class-state` |
| `background/job_queue.py` | `JobQueue` | `_jobs` | `list` | 21 | `shared-class-state` |
| `cardhawkos/runtime/cache.py` | `RuntimeCache` | `_cache` | `dict` | 11 | `shared-class-state` |
| `cardhawkos/runtime/registry.py` | `EngineRegistry` | `_engines` | `dict` | 8 | `shared-class-state` |
| `cardhawkos/runtime/service_registry.py` | `ServiceRegistry` | `_services` | `dict` | 18 | `shared-class-state` |
| `datalake/intelligence_store.py` | `IntelligenceStore` | `_records` | `list` | 16 | `shared-class-state` |
| `event_bus/runtime/bus.py` | `EventBus` | `_subscribers` | `dict` | 5 | `shared-class-state` |
| `eventbus/event_bus.py` | `EventBus` | `_events` | `list` | 17 | `shared-class-state` |
| `eventbus/event_bus.py` | `EventBus` | `_subscribers` | `dict` | 18 | `shared-class-state` |
| `founder/founder_memory.py` | `FounderMemory` | `_items` | `list` | 14 | `shared-class-state` |
| `founder_studio/studio_service.py` | `FounderStudioService` | `_items` | `list` | 17 | `shared-class-state` |
| `genome/cardhawk_genome.py` | `CardHawkGenome` | `_records` | `list` | 17 | `shared-class-state` |
| `genome/runtime/service.py` | `GenomeService` | `_genomes` | `dict` | 9 | `shared-class-state` |
| `jobs/runtime/manager.py` | `JobManager` | `_history` | `list` | 3 | `shared-class-state` |
| `jobs/runtime/scheduler.py` | `JobScheduler` | `_jobs` | `list` | 7 | `shared-class-state` |
| `live_data/watchlist/live_watchlist.py` | `LiveWatchlist` | `_targets` | `list` | 16 | `shared-class-state` |
| `negotiation/offer_tracker.py` | `OfferTracker` | `_offers` | `list` | 20 | `shared-class-state` |
| `observability/telemetry.py` | `Telemetry` | `_metrics` | `list` | 11 | `shared-class-state` |
| `performance/cache.py` | `ResultCache` | `_cache` | `dict` | 5 | `shared-class-state` |
| `timeline/timeline_service.py` | `IntelligenceTimelineService` | `_events` | `list` | 18 | `shared-class-state` |
| `workflow_automation/workflow_service.py` | `WorkflowAutomationService` | `_runs` | `list` | 51 | `shared-class-state` |

## Recommendations

### safe-classvar

- `Genesis14_SPAN_Constitutional_Intelligence/package/aletheus/span/constitutional_context.py:74` `ProjectInspector.EXCLUDED_PARTS` — Annotate as typing.ClassVar with an appropriate collection type.
- `adaptive_intelligence/deployment/deployment_profiles.py:4` `DeploymentProfiles.PROFILES` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/application_runtime/services.py:19` `ApplicationServiceResolver.SERVICE_NAMES` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/apps/demo/application.py:11` `DemoApplication.PERMISSIONS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/apps/demo/application.py:16` `DemoApplication.SERVICES` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/apps/demo/application.py:20` `DemoApplication.DEPENDENCIES` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/civilization/adapters.py:26` `SecurityCivilizationAdapter.EVENT_EVIDENCE_MAP` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/constitutional_memory/precedent.py:8` `ConstitutionalPrecedentEngine.PRECEDENT_ORDER` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/neural/state/manager.py:12` `BrainStateManager.VALID_STATES` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/overlay_manager/validation.py:8` `OverlayValidator.RESERVED_TERMS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/platform/platform_layer.py:22` `PlatformLayer.REQUIRED_DIRS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/platform/platform_layer.py:30` `PlatformLayer.REQUIRED_TOOLS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/platform/platform_layer.py:34` `PlatformLayer.OPTIONAL_TOOLS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/platform_intelligence/engine.py:14` `PlatformIntelligenceEngine.IGNORED_DIRS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/platform_intelligence/runtime_health.py:11` `RuntimeHealthService.STAT_FIELDS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/platform_intelligence/runtime_snapshot.py:13` `RuntimeSnapshotService.COMPONENTS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/platform_lifecycle/state.py:23` `PlatformStateEngine.VALID_STATES` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/repository_dna/collision_auditor.py:11` `RepositoryDNACollisionAuditor.KNOWN_CLUSTERS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/runtime/commands_v2/dispatcher.py:45` `CompiledRuntimeCommandDispatcher.RESULT_KEY_CONTRACTS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/runtime/compatibility_layer/layer.py:12` `CompatibilityLayer.SERVICE_REGISTRY` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/runtime/compatibility_layer/layer.py:30` `CompatibilityLayer.SAFE_ALIASES` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/runtime/decomposition/responsibility.py:11` `ResponsibilityExtractor.RESPONSIBILITIES` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/runtime_supervisor/core.py:14` `RuntimeSupervisor.WATCHED_EVENTS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/sdk/application.py:18` `Application.PERMISSIONS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/sdk/application.py:19` `Application.SERVICES` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/sdk/application.py:20` `Application.DEPENDENCIES` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/span/constitutional_context.py:74` `ProjectInspector.EXCLUDED_PARTS` — Annotate as typing.ClassVar with an appropriate collection type.
- `aletheus/spectrum_platform_analyzer/boundary_analysis.py:25` `BoundaryAnalyzer.ALLOWED` — Annotate as typing.ClassVar with an appropriate collection type.
- `architecture/import_migrator.py:12` `ImportMigrator.REPLACEMENTS` — Annotate as typing.ClassVar with an appropriate collection type.
- `architecture/project_auditor.py:35` `ProjectAuditor.DEPRECATED_PATTERNS` — Annotate as typing.ClassVar with an appropriate collection type.
- `asset_core/runtime/image_service.py:8` `AssetImageService.IMAGE_FIELDS` — Annotate as typing.ClassVar with an appropriate collection type.
- `asset_core/runtime/image_service.py:14` `AssetImageService.EXTENSIONS` — Annotate as typing.ClassVar with an appropriate collection type.
- `asset_core/workflows/asset_pipeline.py:7` `AssetPipeline.STAGES` — Annotate as typing.ClassVar with an appropriate collection type.
- `card_hawk/assets/categories.py:11` `AssetCategories.TYPES` — Annotate as typing.ClassVar with an appropriate collection type.
- `card_hawk/assets/lifecycle.py:11` `AssetLifecycle.STATES` — Annotate as typing.ClassVar with an appropriate collection type.
- `card_hawk/collector_app/subscriptions.py:11` `SubscriptionEngine.TIERS` — Annotate as typing.ClassVar with an appropriate collection type.
- `card_hawk/founder_console/modules.py:11` `ConsoleModules.MODULES` — Annotate as typing.ClassVar with an appropriate collection type.
- `card_hawk/universal_collectibles/categories.py:11` `Categories.TYPES` — Annotate as typing.ClassVar with an appropriate collection type.
- `cardhawkos/config/settings.py:23` `Settings.FEATURE_FLAGS` — Annotate as typing.ClassVar with an appropriate collection type.
- `commercial/commercial_readiness.py:4` `CommercialReadiness.CHECKS` — Annotate as typing.ClassVar with an appropriate collection type.
- `commercialization/permissions.py:2` `Permissions.ROLE_PERMISSIONS` — Annotate as typing.ClassVar with an appropriate collection type.
- `core/config.py:20` `Config.FEATURE_FLAGS` — Annotate as typing.ClassVar with an appropriate collection type.
- `hawk_aeye/brand_detector.py:4` `BrandDetector.KNOWN_BRANDS` — Annotate as typing.ClassVar with an appropriate collection type.
- `hawk_aeye/parallel_detector.py:4` `ParallelDetector.KNOWN_PARALLELS` — Annotate as typing.ClassVar with an appropriate collection type.
- `hawk_aeye/player_detector.py:4` `PlayerDetector.KNOWN_PLAYERS` — Annotate as typing.ClassVar with an appropriate collection type.
- `intelligence_convergence/engines/digital_twin_2.py:7` `DigitalTwin2.SCENARIOS` — Annotate as typing.ClassVar with an appropriate collection type.
- `marketplace/connectors/manager.py:14` `MarketplaceManager.PROVIDERS` — Annotate as typing.ClassVar with an appropriate collection type.
- `scheduler/runtime_scheduler.py:9` `RuntimeScheduler.DEFAULT_JOBS` — Annotate as typing.ClassVar with an appropriate collection type.
- `security/config_validator.py:7` `ConfigValidator.REQUIRED_DIRS` — Annotate as typing.ClassVar with an appropriate collection type.
- `thorx/liquidity.py:4` `LiquidityScorer.PREMIUM_BRANDS` — Annotate as typing.ClassVar with an appropriate collection type.
- `thorx/market_strength.py:4` `MarketStrengthScorer.HOT_SPORTS` — Annotate as typing.ClassVar with an appropriate collection type.
- `thorx/market_strength.py:5` `MarketStrengthScorer.CORE_TEAMS` — Annotate as typing.ClassVar with an appropriate collection type.
- `thorx/player_thesis.py:4` `PlayerThesisScorer.HIGH_CONVICTION` — Annotate as typing.ClassVar with an appropriate collection type.
- `thorx/portfolio_fit.py:4` `PortfolioFitScorer.CORE_TEAMS` — Annotate as typing.ClassVar with an appropriate collection type.
- `thorx/risk.py:4` `RiskScorer.RISKY_BRANDS` — Annotate as typing.ClassVar with an appropriate collection type.
- `thorx/score.py:17` `ThorxScore.WEIGHTS` — Annotate as typing.ClassVar with an appropriate collection type.
- `thorx/visual_appeal.py:4` `VisualAppealScorer.PREMIUM_PARALLELS` — Annotate as typing.ClassVar with an appropriate collection type.
- `tools/repository/rules.py:24` `RepositoryPolicy.DEFAULT_ALLOWED_ROOT_FILES` — Annotate as typing.ClassVar with an appropriate collection type.
- `watch_tower/runtime/engine.py:24` `WatchTowerEngine.SAFE_DELETE_NAMES` — Annotate as typing.ClassVar with an appropriate collection type.
- `watch_tower/runtime/engine.py:28` `WatchTowerEngine.SAFE_DELETE_DIRS` — Annotate as typing.ClassVar with an appropriate collection type.
- `watch_tower/runtime/engine.py:35` `WatchTowerEngine.REQUIRED_ROOT_FILES` — Annotate as typing.ClassVar with an appropriate collection type.
- `watch_tower/runtime/engine.py:41` `WatchTowerEngine.REQUIRED_ROOT_DIRS` — Annotate as typing.ClassVar with an appropriate collection type.
- `watch_tower/runtime/engine.py:49` `WatchTowerEngine.SUSPICIOUS_NAMES` — Annotate as typing.ClassVar with an appropriate collection type.
- `workflow_automation/workflow_service.py:24` `WorkflowAutomationService.TEMPLATES` — Annotate as typing.ClassVar with an appropriate collection type.

### shared-class-state

- `adaptive_intelligence/feedback/feedback_loop.py:21` `IntelligenceFeedbackLoop._feedback` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `adaptive_intelligence/plugins/plugin_framework.py:16` `PluginRegistry._plugins` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `adaptive_intelligence/research/research_workspace.py:19` `ResearchWorkspace._notes` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `background/job_queue.py:21` `JobQueue._jobs` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `cardhawkos/runtime/cache.py:11` `RuntimeCache._cache` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `cardhawkos/runtime/registry.py:8` `EngineRegistry._engines` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `cardhawkos/runtime/service_registry.py:18` `ServiceRegistry._services` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `datalake/intelligence_store.py:16` `IntelligenceStore._records` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `event_bus/runtime/bus.py:5` `EventBus._subscribers` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `eventbus/event_bus.py:17` `EventBus._events` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `eventbus/event_bus.py:18` `EventBus._subscribers` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `founder/founder_memory.py:14` `FounderMemory._items` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `founder_studio/studio_service.py:17` `FounderStudioService._items` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `genome/cardhawk_genome.py:17` `CardHawkGenome._records` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `genome/runtime/service.py:9` `GenomeService._genomes` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `jobs/runtime/manager.py:3` `JobManager._history` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `jobs/runtime/scheduler.py:7` `JobScheduler._jobs` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `live_data/watchlist/live_watchlist.py:16` `LiveWatchlist._targets` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `negotiation/offer_tracker.py:20` `OfferTracker._offers` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `observability/telemetry.py:11` `Telemetry._metrics` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `performance/cache.py:5` `ResultCache._cache` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `timeline/timeline_service.py:18` `IntelligenceTimelineService._events` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.
- `workflow_automation/workflow_service.py:51` `WorkflowAutomationService._runs` — Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.

### manual-review

- `core/engine_base.py:15` `EngineBase.events` — Mutable class attribute may be shared unintentionally; inspect usage before changing.
- `intelligence/projections/base.py:13` `Projection.events` — Mutable class attribute may be shared unintentionally; inspect usage before changing.
- `timeline/engine/timeline_projection.py:9` `TimelineProjection.events` — Mutable class attribute may be shared unintentionally; inspect usage before changing.

## Parse Failures

No syntax or file-read failures were detected.
