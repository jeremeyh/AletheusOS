from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any


def utc_now():
    return datetime.utcnow().isoformat()


@dataclass
class HANode:
    node_id: str
    name: str
    role: str = "follower"
    status: str = "online"
    health: str = "healthy"
    last_heartbeat: str = field(default_factory=utc_now)
    replication_lag: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ReplicationEvent:
    event_id: str
    source_node: str
    target_node: str
    payload: dict[str, Any]
    status: str = "replicated"
    created_at: str = field(default_factory=utc_now)


class AletheusHighAvailabilityEngine:
    VERSION = "3.6.0"

    def __init__(self):
        self.nodes: dict[str, HANode] = {}
        self.replication_events: list[ReplicationEvent] = []
        self.failover_events: list[dict[str, Any]] = []
        self.recovery_events: list[dict[str, Any]] = []
        self.leader_id: str | None = None

    @property
    def version(self):
        return self.VERSION

    def bootstrap(self):
        if not self.nodes:
            leader = HANode(
                node_id=str(uuid.uuid4()),
                name="Primary Runtime",
                role="leader",
            )
            self.nodes[leader.node_id] = leader
            self.leader_id = leader.node_id

        return self.statistics()

    def join(self, name: str, metadata=None):
        self.bootstrap()

        node = HANode(
            node_id=str(uuid.uuid4()),
            name=name,
            role="follower",
            metadata=metadata or {},
        )

        self.nodes[node.node_id] = node
        return asdict(node)

    def leave(self, node_id: str):
        self.bootstrap()

        node = self.nodes.pop(node_id, None)

        if node is None:
            return {"error": "Node not found"}

        if self.leader_id == node_id:
            self.leader_id = None
            self._elect_leader()

        return asdict(node)

    def promote(self, node_id: str):
        self.bootstrap()

        if node_id not in self.nodes:
            return {"error": "Node not found"}

        for node in self.nodes.values():
            node.role = "follower"

        self.nodes[node_id].role = "leader"
        self.leader_id = node_id

        return asdict(self.nodes[node_id])

    def demote(self, node_id: str):
        self.bootstrap()

        if node_id not in self.nodes:
            return {"error": "Node not found"}

        self.nodes[node_id].role = "follower"

        if self.leader_id == node_id:
            self.leader_id = None
            self._elect_leader()

        return asdict(self.nodes[node_id])

    def failover(self):
        self.bootstrap()

        old_leader = self.leader_id

        if old_leader and old_leader in self.nodes:
            self.nodes[old_leader].status = "offline"
            self.nodes[old_leader].health = "critical"
            self.nodes[old_leader].role = "failed_leader"

        self.leader_id = None
        new_leader = self._elect_leader()

        event = {
            "event_id": str(uuid.uuid4()),
            "old_leader": old_leader,
            "new_leader": self.leader_id,
            "status": "completed" if new_leader else "failed",
            "created_at": utc_now(),
        }

        self.failover_events.append(event)
        return event

    def recover(self, node_id: str):
        self.bootstrap()

        if node_id not in self.nodes:
            return {"error": "Node not found"}

        node = self.nodes[node_id]
        node.status = "online"
        node.health = "healthy"
        node.role = "follower"
        node.last_heartbeat = utc_now()

        event = {
            "event_id": str(uuid.uuid4()),
            "node_id": node_id,
            "status": "recovered",
            "created_at": utc_now(),
        }

        self.recovery_events.append(event)
        return event

    def replicate(self, payload=None):
        self.bootstrap()

        leader = self.leader_id
        events = []

        for node in self.nodes.values():
            if node.node_id == leader:
                continue

            event = ReplicationEvent(
                event_id=str(uuid.uuid4()),
                source_node=leader or "unknown",
                target_node=node.node_id,
                payload=payload or {},
            )

            self.replication_events.append(event)
            node.replication_lag = 0
            events.append(asdict(event))

        return {
            "replicated": len(events),
            "events": events,
        }

    def status(self):
        self.bootstrap()

        return {
            "leader": self.leader_id,
            "nodes": [asdict(node) for node in self.nodes.values()],
            "health": "healthy" if self.leader_id else "warning",
        }

    def statistics(self):
        return {
            "version": self.VERSION,
            "nodes": len(self.nodes),
            "leader": self.leader_id,
            "followers": sum(1 for n in self.nodes.values() if n.role == "follower"),
            "replication_events": len(self.replication_events),
            "failover_events": len(self.failover_events),
            "recovery_events": len(self.recovery_events),
            "health": "healthy" if self.leader_id else "warning",
        }

    def _elect_leader(self):
        candidates = [
            node
            for node in self.nodes.values()
            if node.status == "online" and node.health == "healthy"
        ]

        if not candidates:
            return None

        leader = candidates[0]
        leader.role = "leader"
        self.leader_id = leader.node_id
        return leader


high_availability_core = AletheusHighAvailabilityEngine()
