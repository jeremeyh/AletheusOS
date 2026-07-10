from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


def now() -> str:
    return utc_now_iso()


@dataclass
class ApplicationManifest:
    app_id: str
    name: str
    version: str = "1.0.0"
    author: str = "6th Dimension Multimedia"
    description: str = ""
    autostart: bool = False
    permissions: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    commands: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class ApplicationEvent:
    app_id: str
    event_type: str
    message: str
    payload: Dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class NativeApplication:
    manifest: ApplicationManifest
    status: str = "installed"
    health: str = "unknown"
    lifecycle: str = "installed"
    events: List[ApplicationEvent] = field(default_factory=list)
    app_runtime_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    installed_at: str = field(default_factory=now)
    started_at: str | None = None
    stopped_at: str | None = None
    last_heartbeat: str | None = None

    @property
    def application_id(self) -> str:
        return self.manifest.app_id

    @property
    def name(self) -> str:
        return self.manifest.name

    @property
    def version(self) -> str:
        return self.manifest.version

    @property
    def dependencies(self) -> List[str]:
        return self.manifest.dependencies

    @property
    def commands(self) -> List[str]:
        return self.manifest.commands

    def emit(self, event_type: str, message: str, payload: Dict[str, Any] | None = None) -> ApplicationEvent:
        event = ApplicationEvent(
            app_id=self.manifest.app_id,
            event_type=event_type,
            message=message,
            payload=payload or {},
        )
        self.events.append(event)
        return event

    def start(self) -> None:
        self.status = "running"
        self.lifecycle = "running"
        self.health = "healthy"
        self.started_at = now()
        self.last_heartbeat = now()
        self.emit("application.started", f"{self.name} started.")

    def stop(self) -> None:
        self.status = "stopped"
        self.lifecycle = "stopped"
        self.health = "offline"
        self.stopped_at = now()
        self.emit("application.stopped", f"{self.name} stopped.")

    def restart(self) -> None:
        self.emit("application.restarting", f"{self.name} restarting.")
        self.stop()
        self.start()
        self.emit("application.restarted", f"{self.name} restarted.")

    def heartbeat(self) -> None:
        self.last_heartbeat = now()
        self.emit("application.heartbeat", f"{self.name} heartbeat recorded.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "application_id": self.application_id,
            "app_runtime_id": self.app_runtime_id,
            "name": self.name,
            "version": self.version,
            "status": self.status,
            "health": self.health,
            "lifecycle": self.lifecycle,
            "manifest": self.manifest.to_dict(),
            "dependencies": self.dependencies,
            "commands": self.commands,
            "services": self.manifest.services,
            "permissions": self.manifest.permissions,
            "events": [event.to_dict() for event in self.events],
            "event_count": len(self.events),
            "installed_at": self.installed_at,
            "started_at": self.started_at,
            "stopped_at": self.stopped_at,
            "last_heartbeat": self.last_heartbeat,
        }
