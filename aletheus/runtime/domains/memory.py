from __future__ import annotations


class MemoryDomain:
    """
    Runtime Memory capability domain.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def remember(self, context):
        payload = context.payload

        record = self.runtime.memory.remember(
            key=payload.get("key", "untitled"),
            value=payload.get("value"),
            namespace=payload.get("namespace", context.application),
            memory_type=payload.get("memory_type", "working"),
            tags=payload.get("tags", []),
        )

        context.add_result(
            "memory_record",
            record.to_dict(),
        )

        return context

    def recall(self, context):
        payload = context.payload

        context.add_result(
            "memory",
            self.runtime.memory.recall(
                key=payload.get("key"),
                namespace=payload.get("namespace"),
                memory_type=payload.get("memory_type"),
                tag=payload.get("tag"),
                limit=payload.get("limit", 100),
            ),
        )

        return context

    def statistics(self, context):
        context.add_result(
            "memory_stats",
            (
                self.runtime.memory.stats()
                if hasattr(self.runtime.memory, "stats")
                else self.runtime.memory.statistics()
                if hasattr(self.runtime.memory, "statistics")
                else {
                    "status": getattr(
                        self.runtime.memory,
                        "status",
                        "unknown",
                    )
                }
            ),
        )

        return context

    def clear_working(self, context):
        removed = self.runtime.memory.clear_working_memory()

        context.add_result(
            "removed",
            removed,
        )

        return context
