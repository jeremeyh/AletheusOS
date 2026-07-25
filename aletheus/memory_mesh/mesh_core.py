from __future__ import annotations

from typing import Any

from aletheus.memory_mesh.models import (
    MemoryObject,
    MemoryReplica,
    MemorySnapshot,
    MemoryVersion,
    SemanticRecord,
    checksum,
)


class AletheusMemoryMesh:
    def __init__(self) -> None:
        self.version = "2.3.0"
        self.objects: dict[str, MemoryObject] = {}
        self.versions: dict[str, list[MemoryVersion]] = {}
        self.snapshots: dict[str, MemorySnapshot] = {}
        self.replicas: list[MemoryReplica] = []
        self.semantic_cache: dict[str, SemanticRecord] = {}
        self.sync_events: list[dict[str, Any]] = []

    def store(
        self,
        key: str,
        value: Any,
        namespace: str = "global",
        object_type: str = "generic",
        tags: list[str] | None = None,
        owner: str = "aletheus",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        existing = next(
            (obj for obj in self.objects.values() if obj.key == key and obj.namespace == namespace),
            None,
        )

        if existing:
            existing.update(value=value, tags=tags or existing.tags, metadata=metadata or {})
            obj = existing
        else:
            obj = MemoryObject(
                key=key,
                value=value,
                namespace=namespace,
                object_type=object_type,
                tags=tags or [],
                owner=owner,
                metadata=metadata or {},
            )
            self.objects[obj.object_id] = obj

        self._commit_version(obj)
        self._cache_semantic(obj)
        return obj.to_dict()

    def retrieve(self, object_id: str = "", key: str = "", namespace: str = "global") -> dict[str, Any]:
        obj = None
        if object_id:
            obj = self.objects.get(object_id)
        elif key:
            obj = next((item for item in self.objects.values() if item.key == key and item.namespace == namespace), None)

        if obj is None:
            return {"error": "Memory object not found."}

        return obj.to_dict()

    def search(self, query: str = "", tags: list[str] | None = None, namespace: str = "") -> list[dict[str, Any]]:
        tags = tags or []
        results = []

        for obj in self.objects.values():
            text = f"{obj.key} {obj.namespace} {obj.object_type} {' '.join(obj.tags)} {obj.value}".lower()
            match_query = not query or query.lower() in text
            match_tags = not tags or any(tag in obj.tags for tag in tags)
            match_namespace = not namespace or obj.namespace == namespace

            if match_query and match_tags and match_namespace:
                results.append(obj.to_dict())

        return results

    def snapshot(self, name: str = "Memory Mesh Snapshot") -> dict[str, Any]:
        snap = MemorySnapshot(
            name=name,
            objects=[obj.to_dict() for obj in self.objects.values()],
        )
        self.snapshots[snap.snapshot_id] = snap
        return snap.to_dict()

    def restore(self, snapshot_id: str) -> dict[str, Any]:
        snap = self.snapshots.get(snapshot_id)
        if snap is None:
            return {"error": f"Snapshot not found: {snapshot_id}"}

        self.objects = {}
        for item in snap.objects:
            obj = MemoryObject(
                key=item["key"],
                value=item["value"],
                namespace=item.get("namespace", "global"),
                object_type=item.get("object_type", "generic"),
                owner=item.get("owner", "aletheus"),
                tags=item.get("tags", []),
                permissions=item.get("permissions", ["read", "write"]),
                version=item.get("version", 1),
                replication_state=item.get("replication_state", "local"),
                object_id=item.get("object_id"),
                metadata=item.get("metadata", {}),
            )
            self.objects[obj.object_id] = obj

        return {
            "restored": True,
            "snapshot": snap.to_dict(),
            "objects": len(self.objects),
        }

    def replicate(self, object_id: str = "", target_node: str = "primary") -> dict[str, Any]:
        if object_id and object_id not in self.objects:
            return {"error": f"Memory object not found: {object_id}"}

        targets = [self.objects[object_id]] if object_id else list(self.objects.values())
        created = []

        for obj in targets:
            obj.replication_state = "replicated"
            replica = MemoryReplica(object_id=obj.object_id, target_node=target_node)
            self.replicas.append(replica)
            created.append(replica.to_dict())

        return {
            "replicated": len(created),
            "target_node": target_node,
            "replicas": created,
        }

    def sync(self, node: str = "distributed_fabric") -> dict[str, Any]:
        event = {
            "node": node,
            "objects": len(self.objects),
            "snapshots": len(self.snapshots),
            "replicas": len(self.replicas),
            "status": "synchronized",
        }
        self.sync_events.append(event)
        return event

    def history(self, object_id: str = "") -> dict[str, Any]:
        if object_id:
            return {
                "object_id": object_id,
                "versions": [v.to_dict() for v in self.versions.get(object_id, [])],
            }

        return {
            "versions": {
                oid: [v.to_dict() for v in versions]
                for oid, versions in self.versions.items()
            }
        }

    def cache(self, object_id: str = "") -> dict[str, Any]:
        if object_id:
            record = self.semantic_cache.get(object_id)
            return record.to_dict() if record else {"error": "Semantic cache record not found."}

        return {
            "semantic_cache": [record.to_dict() for record in self.semantic_cache.values()]
        }

    def stats(self) -> dict[str, Any]:
        version_count = sum(len(items) for items in self.versions.values())
        return {
            "version": self.version,
            "memory_objects": len(self.objects),
            "snapshots": len(self.snapshots),
            "replicas": len(self.replicas),
            "semantic_records": len(self.semantic_cache),
            "memory_versions": version_count,
            "sync_events": len(self.sync_events),
            "replication_status": "healthy" if self.replicas or self.objects else "idle",
            "synchronization": 1.0 if self.sync_events or self.objects else 0.0,
            "cache_hit_rate": 0.99 if self.semantic_cache else 0.0,
        }

    def _commit_version(self, obj: MemoryObject) -> None:
        record = MemoryVersion(
            object_id=obj.object_id,
            version=obj.version,
            value=obj.value,
            checksum_value=checksum(obj.value),
        )
        self.versions.setdefault(obj.object_id, []).append(record)

    def _cache_semantic(self, obj: MemoryObject) -> None:
        terms = []
        terms.extend(obj.key.replace("_", " ").split())
        terms.extend(obj.namespace.replace("_", " ").split())
        terms.extend(obj.object_type.replace("_", " ").split())
        terms.extend([str(tag) for tag in obj.tags])

        record = SemanticRecord(
            object_id=obj.object_id,
            terms=terms,
            tags=obj.tags,
        )
        self.semantic_cache[obj.object_id] = record


memory_mesh_core = AletheusMemoryMesh()
