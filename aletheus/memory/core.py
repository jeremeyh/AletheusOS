from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class MemoryRecord:
    key: str
    value: Any
    namespace: str = "system"
    memory_type: str = "working"
    tags: List[str] = field(default_factory=list)
    record_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
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
        self.records: List[MemoryRecord] = []

    def remember(
        self,
        key: str,
        value: Any,
        namespace: str = "system",
        memory_type: str = "working",
        tags: Optional[List[str]] = None,
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
        key: Optional[str] = None,
        namespace: Optional[str] = None,
        memory_type: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        results = self.records

        if key:
            results = [record for record in results if record.key == key]
        if namespace:
            results = [record for record in results if record.namespace == namespace]
        if memory_type:
            results = [record for record in results if record.memory_type == memory_type]
        if tag:
            results = [record for record in results if tag in record.tags]

        return [record.to_dict() for record in results[-limit:]]

    def clear_working_memory(self) -> int:
        before = len(self.records)
        self.records = [record for record in self.records if record.memory_type != "working"]
        return before - len(self.records)

    def stats(self) -> Dict[str, Any]:
        by_type: Dict[str, int] = {}

        for record in self.records:
            by_type[record.memory_type] = by_type.get(record.memory_type, 0) + 1

        return {
            "version": self.version,
            "total_records": len(self.records),
            "by_type": by_type,
        }


memory_core = AletheusMemoryCore()
