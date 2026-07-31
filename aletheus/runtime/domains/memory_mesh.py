from __future__ import annotations


class MemoryMeshDomain:
    """
    Runtime Memory Mesh capability domain.
    Genesis 6 migration.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def store(self, context):
        payload = context.payload

        result = self.runtime.memory_mesh.store(
            key=payload.get("key", ""),
            value=payload.get("value"),
            namespace=payload.get("namespace", "global"),
            object_type=payload.get("object_type", "generic"),
            tags=payload.get("tags", []),
            owner=payload.get("owner", "aletheus"),
            metadata=payload.get("metadata", {}),
        )

        context.add_result("memory_object", result)
        context.add_result("memory", result)
        return context

    def retrieve(self, context):
        payload = context.payload

        result = self.runtime.memory_mesh.retrieve(
            object_id=payload.get("object_id", ""),
            key=payload.get("key", ""),
            namespace=payload.get("namespace", "global"),
        )

        context.add_result("memory_object", result)
        context.add_result("memory", result)
        return context

    def search(self, context):
        payload = context.payload

        result = self.runtime.memory_mesh.search(
            query=payload.get("query", ""),
            tags=payload.get("tags", []),
            namespace=payload.get("namespace", ""),
        )

        context.add_result("results", result)
        context.add_result("memory_search", result)
        return context

    def snapshot(self, context):
        result = self.runtime.memory_mesh.snapshot(
            context.payload.get(
                "name",
                "Memory Mesh Snapshot",
            )
        )

        context.add_result("snapshot", result)
        return context

    def restore(self, context):
        result = self.runtime.memory_mesh.restore(
            context.payload.get("snapshot_id", "")
        )

        context.add_result("restore", result)
        return context

    def replicate(self, context):
        payload = context.payload

        result = self.runtime.memory_mesh.replicate(
            object_id=payload.get("object_id", ""),
            target_node=payload.get("target_node", "primary"),
        )

        context.add_result("replication", result)
        return context

    def sync(self, context):
        result = self.runtime.memory_mesh.sync(
            context.payload.get(
                "node",
                "distributed_fabric",
            )
        )

        context.add_result("sync", result)
        return context

    def history(self, context):
        result = self.runtime.memory_mesh.history(context.payload.get("object_id", ""))

        context.add_result("history", result)
        return context

    def cache(self, context):
        result = self.runtime.memory_mesh.cache(context.payload.get("object_id", ""))

        context.add_result("cache", result)
        return context

    def stats(self, context):
        context.add_result(
            "memory_mesh_stats",
            self.runtime.memory_mesh.stats(),
        )
        return context
