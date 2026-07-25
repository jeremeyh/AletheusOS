from __future__ import annotations

from typing import Any

from aletheus.distributed.models import (
    DistributedCluster,
    DistributedEvent,
    DistributedNode,
    DistributedTask,
)


class AletheusDistributedIntelligenceFabric:
    def __init__(self) -> None:
        self.version = "2.2.0"
        self.clusters: list[DistributedCluster] = []
        self.events: list[DistributedEvent] = []

    def emit(self, event_type: str, message: str, source: str = "distributed_fabric", payload: dict[str, Any] | None = None) -> DistributedEvent:
        event = DistributedEvent(
            event_type=event_type,
            message=message,
            source=source,
            payload=payload or {},
        )
        self.events.append(event)
        return event

    def create_cluster(self, name: str = "Aletheus Primary Cluster") -> DistributedCluster:
        existing = self.get_cluster(name=name)
        if existing:
            return existing

        cluster = DistributedCluster(name=name)
        self.clusters.append(cluster)
        self.emit("cluster.created", f"Cluster created: {name}", payload=cluster.to_dict())
        return cluster

    def bootstrap_primary_cluster(self) -> DistributedCluster:
        cluster = self.create_cluster("Aletheus Primary Intelligence Cluster")

        defaults = [
            {
                "name": "Coordinator Node",
                "node_type": "coordinator",
                "capabilities": ["routing", "scheduling", "coordination", "governance"],
            },
            {
                "name": "Card Hawk Runtime Node",
                "node_type": "application",
                "capabilities": ["asset_vault", "portfolio", "marketplace", "thorx", "hawk_aeye"],
            },
            {
                "name": "Memory Node",
                "node_type": "memory",
                "capabilities": ["memory", "audit", "learning_context"],
            },
            {
                "name": "Prediction Node",
                "node_type": "prediction",
                "capabilities": ["forecast", "risk", "opportunity", "recommendation"],
            },
            {
                "name": "Workflow Node",
                "node_type": "workflow",
                "capabilities": ["workflow", "mission", "agent_execution"],
            },
        ]

        for item in defaults:
            self.register_node(
                cluster_id=cluster.cluster_id,
                name=item["name"],
                node_type=item["node_type"],
                capabilities=item["capabilities"],
            )

        return cluster

    def get_cluster(self, cluster_id: str = "", name: str = "") -> DistributedCluster | None:
        for cluster in self.clusters:
            if cluster_id and cluster.cluster_id == cluster_id:
                return cluster
            if name and cluster.name == name:
                return cluster
        return None

    def register_node(
        self,
        cluster_id: str,
        name: str,
        node_type: str = "runtime",
        capabilities: list[str] | None = None,
        address: str = "local",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        cluster = self.get_cluster(cluster_id=cluster_id)
        if cluster is None:
            return {"error": f"Cluster not found: {cluster_id}"}

        existing = next((node for node in cluster.nodes if node.name == name), None)
        if existing:
            return existing.to_dict()

        node = DistributedNode(
            name=name,
            node_type=node_type,
            capabilities=capabilities or [],
            address=address,
            metadata=metadata or {},
        )
        cluster.nodes.append(node)
        self.emit("node.registered", f"Node registered: {name}", payload=node.to_dict())
        return node.to_dict()

    def remove_node(self, cluster_id: str, node_id: str) -> dict[str, Any]:
        cluster = self.get_cluster(cluster_id=cluster_id)
        if cluster is None:
            return {"error": f"Cluster not found: {cluster_id}"}

        node = next((item for item in cluster.nodes if item.node_id == node_id), None)
        if node is None:
            return {"error": f"Node not found: {node_id}"}

        cluster.nodes = [item for item in cluster.nodes if item.node_id != node_id]
        self.emit("node.removed", f"Node removed: {node.name}", payload=node.to_dict())
        return node.to_dict()

    def heartbeat(self, cluster_id: str, node_id: str) -> dict[str, Any]:
        cluster = self.get_cluster(cluster_id=cluster_id)
        if cluster is None:
            return {"error": f"Cluster not found: {cluster_id}"}

        node = next((item for item in cluster.nodes if item.node_id == node_id), None)
        if node is None:
            return {"error": f"Node not found: {node_id}"}

        node.heartbeat()
        self.emit("node.heartbeat", f"Heartbeat received: {node.name}", payload=node.to_dict())
        return node.to_dict()

    def broadcast(self, cluster_id: str, message: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        cluster = self.get_cluster(cluster_id=cluster_id)
        if cluster is None:
            return {"error": f"Cluster not found: {cluster_id}"}

        event = self.emit(
            "cluster.broadcast",
            message,
            source="distributed_router",
            payload={
                "cluster_id": cluster.cluster_id,
                "nodes": [node.node_id for node in cluster.nodes],
                "payload": payload or {},
            },
        )

        return {
            "status": "broadcast",
            "cluster": cluster.name,
            "nodes_reached": len(cluster.nodes),
            "event": event.to_dict(),
        }

    def assign_task(
        self,
        cluster_id: str,
        title: str,
        objective: str,
        capability: str = "",
    ) -> dict[str, Any]:
        cluster = self.get_cluster(cluster_id=cluster_id)
        if cluster is None:
            return {"error": f"Cluster not found: {cluster_id}"}

        node = None
        if capability:
            node = next((item for item in cluster.nodes if capability in item.capabilities), None)

        if node is None and cluster.nodes:
            node = cluster.nodes[0]

        if node is None:
            return {"error": "No nodes available."}

        task = DistributedTask(
            title=title,
            objective=objective,
            assigned_node_id=node.node_id,
        )
        task.start()
        task.complete(
            {
                "assigned_node": node.name,
                "node_type": node.node_type,
                "capability": capability,
                "execution": "simulated",
            }
        )

        cluster.tasks.append(task)
        self.emit("distributed.task.completed", f"Distributed task completed: {title}", payload=task.to_dict())

        return task.to_dict()

    def cluster_status(self, cluster_id: str = "") -> dict[str, Any]:
        cluster = self.get_cluster(cluster_id=cluster_id) if cluster_id else (self.clusters[0] if self.clusters else None)
        if cluster is None:
            return {"error": "No cluster available."}

        return {
            "cluster": cluster.to_dict(),
            "health": "healthy" if cluster.nodes else "empty",
            "nodes_online": len([node for node in cluster.nodes if node.status == "online"]),
            "node_count": len(cluster.nodes),
            "task_count": len(cluster.tasks),
            "replication_health": "healthy",
            "synchronization": 1.0 if cluster.nodes else 0.0,
        }

    def list_clusters(self) -> list[dict[str, Any]]:
        return [cluster.to_dict() for cluster in self.clusters]

    def history(self) -> list[dict[str, Any]]:
        return [event.to_dict() for event in self.events]

    def stats(self) -> dict[str, Any]:
        nodes = sum(len(cluster.nodes) for cluster in self.clusters)
        tasks = sum(len(cluster.tasks) for cluster in self.clusters)

        return {
            "version": self.version,
            "clusters": len(self.clusters),
            "nodes": nodes,
            "tasks": tasks,
            "events": len(self.events),
            "coordinator_status": "online",
            "replication_health": "healthy" if nodes else "empty",
            "synchronization": 1.0 if nodes else 0.0,
        }


distributed_core = AletheusDistributedIntelligenceFabric()
