from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any
import uuid


def utc_now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class RuntimeNode:
    node_name: str
    version: str = "3.0.0"
    status: str = "online"
    health: str = "healthy"

    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    capabilities: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)
    agents: List[str] = field(default_factory=list)
    workflows: List[str] = field(default_factory=list)
    plans: List[str] = field(default_factory=list)

    created_at: str = field(default_factory=utc_now)
    last_seen: str = field(default_factory=utc_now)
    heartbeat_count: int = 0

    def heartbeat(self):
        self.heartbeat_count += 1
        self.last_seen = utc_now()
        self.status = "online"
        self.health = "healthy"

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "node_name": self.node_name,
            "version": self.version,
            "status": self.status,
            "health": self.health,
            "capabilities": self.capabilities,
            "services": self.services,
            "agents": self.agents,
            "workflows": self.workflows,
            "plans": self.plans,
            "created_at": self.created_at,
            "last_seen": self.last_seen,
            "heartbeat_count": self.heartbeat_count,
        }


@dataclass
class RuntimeCluster:
    name: str
    cluster_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    leader_node_id: str = ""
    nodes: Dict[str, RuntimeNode] = field(default_factory=dict)
    jobs: List[Dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    health: str = "healthy"

    def to_dict(self):
        return {
            "cluster_id": self.cluster_id,
            "name": self.name,
            "leader_node_id": self.leader_node_id,
            "health": self.health,
            "created_at": self.created_at,
            "node_count": len(self.nodes),
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "jobs": self.jobs,
        }


class AletheusDistributedRuntimeFabric:

    VERSION = "3.0.0"

    def __init__(self):
        self.cluster: RuntimeCluster | None = None

    def bootstrap(self):
        if self.cluster is None:
            self.cluster = RuntimeCluster(
                name="AletheusOS Primary Cluster"
            )

            founder = RuntimeNode(
                node_name="Founder Runtime",
                capabilities=[
                    "kernel",
                    "memory",
                    "knowledge",
                    "reasoning",
                    "decision",
                    "agents",
                    "workflow",
                    "planning",
                ],
                services=[
                    "Runtime Core",
                    "Memory Mesh",
                    "Knowledge Graph",
                    "Reasoning Engine",
                    "Decision Engine",
                    "Agent Runtime",
                    "Workflow Engine",
                    "Planning Engine",
                ],
                agents=[
                    "Founder Agent",
                    "Research Agent",
                    "Marketplace Agent",
                    "Portfolio Agent",
                ],
            )

            self.cluster.nodes[founder.node_id] = founder
            self.cluster.leader_node_id = founder.node_id

        return self.statistics()

    def join(self, node_name: str, capabilities=None, services=None):
        if self.cluster is None:
            self.bootstrap()

        node = RuntimeNode(
            node_name=node_name,
            capabilities=capabilities or [],
            services=services or [],
        )

        self.cluster.nodes[node.node_id] = node
        return node.to_dict()

    def leave(self, node_id: str):
        if self.cluster is None:
            return {"error": "Cluster not initialized"}

        node = self.cluster.nodes.pop(node_id, None)

        if node is None:
            return {"error": "Node not found"}

        if self.cluster.leader_node_id == node_id:
            self.elect_leader()

        return node.to_dict()

    def nodes(self):
        if self.cluster is None:
            self.bootstrap()

        return {
            "nodes": [n.to_dict() for n in self.cluster.nodes.values()]
        }

    def services(self):
        if self.cluster is None:
            self.bootstrap()

        services = []

        for node in self.cluster.nodes.values():
            for svc in node.services:
                services.append(
                    {
                        "node": node.node_name,
                        "service": svc,
                    }
                )

        return {"services": services}

    def heartbeat(self):
        if self.cluster is None:
            self.bootstrap()

        for node in self.cluster.nodes.values():
            node.heartbeat()

        return self.statistics()

    def elect_leader(self):
        if self.cluster is None:
            self.bootstrap()

        leader = next(iter(self.cluster.nodes.values()))
        self.cluster.leader_node_id = leader.node_id

        return {
            "leader": leader.to_dict()
        }

    def status(self):
        if self.cluster is None:
            self.bootstrap()

        return self.cluster.to_dict()

    def statistics(self):
        if self.cluster is None:
            return {
                "version": self.VERSION,
                "clusters": 0,
                "nodes": 0,
                "leader": None,
                "health": "offline",
                "heartbeats": 0,
                "services": 0,
            }

        nodes = list(self.cluster.nodes.values())

        return {
            "version": self.VERSION,
            "clusters": 1,
            "nodes": len(nodes),
            "leader": self.cluster.leader_node_id,
            "health": self.cluster.health,
            "heartbeats": sum(n.heartbeat_count for n in nodes),
            "services": sum(len(n.services) for n in nodes),
            "capabilities": sum(len(n.capabilities) for n in nodes),
            "jobs": len(self.cluster.jobs),
        }



    # ============================================================
    # Legacy Runtime Compatibility Layer
    # ============================================================

    @property
    def version(self):
        return self.VERSION

    def bootstrap_primary_cluster(self):
        self.bootstrap()
        return self.cluster

    def create_cluster(self, name="Aletheus Cluster"):
        self.cluster = RuntimeCluster(name=name)
        self.bootstrap()
        return self.cluster

    def list_clusters(self):
        if self.cluster is None:
            self.bootstrap()
        return [self.cluster.to_dict()]

    def cluster_status(self, cluster_id=""):
        if self.cluster is None:
            self.bootstrap()
        return self.cluster.to_dict()

    def stats(self):
        return self.statistics()

    def history(self):
        return []

    def register_node(self, **kwargs):
        return self.join(
            node_name=kwargs.get("node_name", "Runtime Node"),
            capabilities=kwargs.get("capabilities", []),
            services=kwargs.get("services", []),
        )

    def remove_node(self, node_id):
        return self.leave(node_id)

    def assign_task(self, *args, **kwargs):
        return {"status": "accepted"}

    def broadcast(self, *args, **kwargs):
        return {"status": "broadcast"}


distributed_v3_core = AletheusDistributedRuntimeFabric()
