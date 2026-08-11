from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class MemoryRecord:
    key: str
    value: Any
    namespace: str = "system"
    memory_type: str = "working"
    tags: list[str] = field(default_factory=list)
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "namespace": self.namespace,
            "memory_type": self.memory_type,
            "key": self.key,
            "value": self.value,
            "tags": self.tags,
            "created_at": self.created_at,
        }


class AletheusMemoryCore:
    def __init__(self) -> None:
        self.version = "0.4.0-genesis"
        self.records: list[MemoryRecord] = []

    def remember(
        self,
        key: str,
        value: Any,
        namespace: str = "system",
        memory_type: str = "working",
        tags: list[str] | None = None,
    ) -> MemoryRecord:
        record = MemoryRecord(
            key=key,
            value=value,
            namespace=namespace,
            memory_type=memory_type,
            tags=tags or [],
        )
        self.records.append(record)
        return record

    def recall(
        self,
        key: str | None = None,
        namespace: str | None = None,
        memory_type: str | None = None,
        tag: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        results = self.records

        if key:
            results = [record for record in results if record.key == key]
        if namespace:
            results = [record for record in results if record.namespace == namespace]
        if memory_type:
            results = [
                record for record in results if record.memory_type == memory_type
            ]
        if tag:
            results = [record for record in results if tag in record.tags]

        return [record.to_dict() for record in results[-limit:]]

    def clear_working_memory(self) -> int:
        before = len(self.records)
        self.records = [
            record for record in self.records if record.memory_type != "working"
        ]
        return before - len(self.records)

    def stats(self) -> dict[str, Any]:
        by_type: dict[str, int] = {}

        for record in self.records:
            by_type[record.memory_type] = by_type.get(record.memory_type, 0) + 1

        return {
            "version": self.version,
            "total_records": len(self.records),
            "by_type": by_type,
        }


memory_core = AletheusMemoryCore()
