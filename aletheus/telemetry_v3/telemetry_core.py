from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from typing import Any

from aletheus.time_utils import utc_now, utc_now_iso


def utc_now():
    return utc_now_iso()


@dataclass
class TelemetryMetric:
    metric_id: str
    name: str
    value: Any
    category: str = "runtime"
    timestamp: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TelemetryLog:
    log_id: str
    level: str
    message: str
    source: str = "runtime"
    timestamp: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TelemetryTrace:
    trace_id: str
    span_id: str
    name: str
    status: str = "completed"
    parent_span: str | None = None
    correlation_id: str | None = None
    started_at: str = field(default_factory=utc_now)
    ended_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)


class AletheusTelemetryEngine:
    VERSION = "3.5.0"

    def __init__(self):
        self.metrics: list[TelemetryMetric] = []
        self.logs: list[TelemetryLog] = []
        self.traces: list[TelemetryTrace] = []
        self.health_registry: dict[str, str] = {}
        self.timeline_events: list[dict[str, Any]] = []

    @property
    def version(self):
        return self.VERSION

    def bootstrap(self):
        self.health_registry["runtime"] = "healthy"
        self.timeline("Telemetry Engine bootstrapped", source="telemetry")
        return self.statistics()

    def record(self, name: str, value: Any = None, category: str = "runtime", metadata=None):
        return self.metric(name=name, value=value, category=category, metadata=metadata or {})

    def metric(self, name: str, value: Any, category: str = "runtime", metadata=None):
        item = TelemetryMetric(
            metric_id=str(uuid.uuid4()),
            name=name,
            value=value,
            category=category,
            metadata=metadata or {},
        )
        self.metrics.append(item)
        return asdict(item)

    def log(self, level: str, message: str, source: str = "runtime", metadata=None):
        item = TelemetryLog(
            log_id=str(uuid.uuid4()),
            level=level,
            message=message,
            source=source,
            metadata=metadata or {},
        )
        self.logs.append(item)
        self.timeline(message, source=source)
        return asdict(item)

    def trace(self, name: str, status: str = "completed", parent_span=None, correlation_id=None, metadata=None):
        item = TelemetryTrace(
            trace_id=str(uuid.uuid4()),
            span_id=str(uuid.uuid4()),
            name=name,
            status=status,
            parent_span=parent_span,
            correlation_id=correlation_id,
            metadata=metadata or {},
        )
        self.traces.append(item)
        return asdict(item)

    def health(self, component: str = "runtime", status: str = "healthy"):
        self.health_registry[component] = status
        return {
            "component": component,
            "status": status,
            "registry": self.health_registry,
        }

    def timeline(self, message: str, source: str = "runtime", metadata=None):
        event = {
            "timeline_id": str(uuid.uuid4()),
            "timestamp": utc_now(),
            "source": source,
            "message": message,
            "metadata": metadata or {},
        }
        self.timeline_events.append(event)
        return event

    def statistics(self):
        unhealthy = [
            name for name, status in self.health_registry.items()
            if status not in {"healthy", "online"}
        ]

        return {
            "version": self.VERSION,
            "metrics": len(self.metrics),
            "logs": len(self.logs),
            "traces": len(self.traces),
            "health_checks": len(self.health_registry),
            "timeline_events": len(self.timeline_events),
            "errors": sum(1 for log in self.logs if log.level.lower() == "error"),
            "health": "healthy" if not unhealthy else "warning",
        }


telemetry_core = AletheusTelemetryEngine()
