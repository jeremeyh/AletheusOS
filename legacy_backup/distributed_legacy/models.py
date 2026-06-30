from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List
import uuid


def now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class DistributedNode:
    name: str
    node_type: str = "runtime"
    status: str = "online"
    version: str = "2.2.0"
    capabilities: List[str] = field(default_factory=list)
    address: str = "local"
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    last_heartbeat: str = field(default_factory=now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def heartbeat(self) -> None:
        self.last_heartbeat = now()
        self.status = "online"

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class DistributedTask:
    title: str
    objective: str
    assigned_node_id: str = ""
    status: str = "queued"
    result: Dict[str, Any] = field(default_factory=dict)
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    started_at: str | None = None
    completed_at: str | None = None

    def start(self) -> None:
        self.status = "running"
        self.started_at = now()

    def complete(self, result: Dict[str, Any] | None = None) -> None:
        self.status = "completed"
        self.completed_at = now()
        self.result = result or {}

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class DistributedCluster:
    name: str
    status: str = "online"
    nodes: List[DistributedNode] = field(default_factory=list)
    tasks: List[DistributedTask] = field(default_factory=list)
    cluster_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        data = self.__dict__.copy()
        data["nodes"] = [node.to_dict() for node in self.nodes]
        data["tasks"] = [task.to_dict() for task in self.tasks]
        return data


@dataclass
class DistributedEvent:
    event_type: str
    message: str
    source: str = "distributed_fabric"
    payload: Dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
