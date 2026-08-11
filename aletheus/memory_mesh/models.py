from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


def now() -> str:
    return datetime.utcnow().isoformat()


def checksum(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class MemoryObject:
    key: str
    value: Any
    namespace: str = "global"
    object_type: str = "generic"
    owner: str = "aletheus"
    tags: list[str] = field(default_factory=list)
    permissions: list[str] = field(default_factory=lambda: ["read", "write"])
    version: int = 1
    replication_state: str = "local"
    object_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)
    updated_at: str = field(default_factory=now)
    metadata: dict[str, Any] = field(default_factory=dict)

    def update(
        self,
        value: Any,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.value = value
        self.version += 1
        self.updated_at = now()
        if tags is not None:
            self.tags = tags
        if metadata is not None:
            self.metadata.update(metadata)

    def to_dict(self) -> dict[str, Any]:
        data = self.__dict__.copy()
        data["checksum"] = checksum(
            {
                "key": self.key,
                "value": self.value,
                "namespace": self.namespace,
                "version": self.version,
            }
        )
        return data


@dataclass
class MemoryVersion:
    object_id: str
    version: int
    value: Any
    checksum_value: str
    version_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class MemorySnapshot:
    name: str
    objects: list[dict[str, Any]]
    snapshot_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class MemoryReplica:
    object_id: str
    target_node: str
    status: str = "replicated"
    replica_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__


@dataclass
class SemanticRecord:
    object_id: str
    terms: list[str]
    tags: list[str]
    semantic_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=now)

    def score(self, query: str) -> float:
        q = query.lower()
        haystack = " ".join(self.terms + self.tags).lower()
        if not q:
            return 0.0
        hits = sum(1 for token in q.split() if token in haystack)
        return round(hits / max(len(q.split()), 1), 2)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
