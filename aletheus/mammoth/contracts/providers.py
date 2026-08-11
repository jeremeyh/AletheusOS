from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, runtime_checkable
from .objects import MammothObjectMetadata

@dataclass(frozen=True, slots=True)
class MammothProviderCapabilities:
    atomic_write: bool = False
    transactional_write: bool = False
    delete: bool = False
    versioning: bool = False
    replication: bool = False
    snapshots: bool = False
    range_read: bool = False
    streaming: bool = False
    immutable_write: bool = False
    durable_metadata: bool = False
    crash_recovery: bool = False

@dataclass(frozen=True, slots=True)
class MammothPutRequest:
    metadata: MammothObjectMetadata
    data: bytes

@dataclass(frozen=True, slots=True)
class MammothPutResult:
    provider_id: str
    committed: bool
    object_id: str
    version_id: str
    locator: str

@dataclass(frozen=True, slots=True)
class MammothGetRequest:
    object_id: str
    version_id: str | None = None

@dataclass(frozen=True, slots=True)
class MammothGetResult:
    provider_id: str
    metadata: MammothObjectMetadata
    data: bytes

@dataclass(frozen=True, slots=True)
class MammothDeleteRequest:
    object_id: str
    version_id: str | None = None

@dataclass(frozen=True, slots=True)
class MammothDeleteResult:
    provider_id: str
    removed: bool

@dataclass(frozen=True, slots=True)
class MammothProviderHealth:
    provider_id: str
    healthy: bool
    free_bytes: int | None = None
    detail: str = ""

@runtime_checkable
class MammothPersistenceProvider(Protocol):
    provider_id: str
    capabilities: MammothProviderCapabilities
    def put(self, request: MammothPutRequest) -> MammothPutResult: ...
    def get(self, request: MammothGetRequest) -> MammothGetResult | None: ...
    def remove(self, request: MammothDeleteRequest) -> MammothDeleteResult: ...
    def health(self) -> MammothProviderHealth: ...
