from __future__ import annotations

from typing import Any, Dict

from services.context import PipelineContext, utc_now_iso
from services.founder_state import FounderState
from services.pipeline import Pipeline
from services.plugin_loader import PluginLoader
from services.runtime_cache import RuntimeCache
from services.runtime_commands import CommandBus
from services.runtime_events import EventStore, RuntimeEvent
from services.runtime_metrics import RuntimeMetrics
from services.runtime_scheduler import RuntimeScheduler
from services.runtime_state import RuntimeState


class RuntimeV3:
    def __init__(self) -> None:
        self.state = RuntimeState()
        self.founder_state = FounderState(self.state)
        self.cache = RuntimeCache()
        self.metrics = RuntimeMetrics()
        self.event_store = EventStore()
        self.scheduler = RuntimeScheduler()
        self.plugin_loader = PluginLoader()
        self.plugin_loader.load_defaults()
        self.pipeline = Pipeline(self.plugin_loader)
        self.command_bus = CommandBus(self)
        self._boot()

    def _boot(self) -> None:
        self.metrics.record("runtime.version", "v3")
        self.metrics.record("runtime.status", "online")
        self.events.append(RuntimeEvent("runtime.boot", {"version": "v3", "plugins": self.plugin_loader.manifests()}))
        self.command_bus.register("runtime.health", self._cmd_health)
        self.command_bus.register("runtime.registry", self._cmd_registry)
        self.command_bus.register("runtime.pipeline", self._cmd_pipeline)
        self.command_bus.register("runtime.metrics", self._cmd_metrics)
        self.command_bus.register("runtime.events", self._cmd_events)
        self.command_bus.register("runtime.snapshot", self._cmd_snapshot)
        self.scheduler.register("Daily Vault Pulse", "Create a runtime status pulse and event snapshot.", self._job_daily_vault_pulse)

    @property
    def events(self) -> EventStore:
        return self.event_store

    def _cmd_health(self, context: PipelineContext) -> PipelineContext:
        context.add_result("health", {
            "runtime": "CardHawkOS Runtime v3",
            "status": "online",
            "plugins": len(self.plugin_loader.plugins),
            "enabled_plugins": len(self.plugin_loader.enabled_plugins()),
            "jobs": len(self.scheduler.jobs),
            "cache_keys": self.cache.stats()["keys"],
            "timestamp": utc_now_iso(),
        })
        return context

    def _cmd_registry(self, context: PipelineContext) -> PipelineContext:
        context.add_result("registry", {
            "plugins": self.plugin_loader.manifests(),
            "jobs": self.scheduler.list_jobs(),
            "commands": sorted(self.command_bus.handlers.keys()),
        })
        return context

    def _cmd_pipeline(self, context: PipelineContext) -> PipelineContext:
        result = self.pipeline.run(payload=context.payload)
        context.add_result("pipeline", result.to_dict())
        self.events.append(RuntimeEvent("pipeline.completed", result.to_dict(), request_id=context.request_id))
        self.founder_state.record_decision({
            "timestamp": utc_now_iso(),
            "request_id": context.request_id,
            "payload": context.payload,
            "result": result.results,
            "errors": result.errors,
        })
        return context

    def _cmd_metrics(self, context: PipelineContext) -> PipelineContext:
        context.add_result("metrics", self.metrics.recent())
        return context

    def _cmd_events(self, context: PipelineContext) -> PipelineContext:
        context.add_result("events", self.events.read_recent(limit=int(context.payload.get("limit", 100))))
        return context

    def _cmd_snapshot(self, context: PipelineContext) -> PipelineContext:
        snap = self.state.snapshot("runtime_v3_snapshot", {
            "health": self.command_bus.dispatch("runtime.health").results.get("health"),
            "registry": self.command_bus.dispatch("runtime.registry").results.get("registry"),
            "metrics": self.metrics.recent(),
        })
        self.events.append(RuntimeEvent("runtime.snapshot", snap, request_id=context.request_id))
        context.add_result("snapshot", snap)
        return context

    def _job_daily_vault_pulse(self) -> Dict[str, Any]:
        health = self.command_bus.dispatch("runtime.health").results.get("health", {})
        snapshot = self.state.snapshot("daily_vault_pulse", health)
        return {"status": "completed", "health": health, "snapshot": snapshot}


runtime_v3 = RuntimeV3()
