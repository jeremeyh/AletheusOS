from __future__ import annotations
from dataclasses import dataclass, fields
from threading import RLock
from aletheus.mammoth.contracts.providers import MammothPersistenceProvider

class MammothProviderRegistrationError(ValueError): pass
class MammothProviderSelectionError(LookupError): pass

@dataclass(frozen=True, slots=True)
class MammothProviderRequirements:
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

class MammothProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, MammothPersistenceProvider] = {}
        self._lock = RLock()

    def register(self, provider: MammothPersistenceProvider) -> None:
        provider_id = getattr(provider, "provider_id", "")
        if not isinstance(provider_id, str) or not provider_id.strip():
            raise MammothProviderRegistrationError("provider_id must be nonblank")
        if not isinstance(provider, MammothPersistenceProvider):
            raise MammothProviderRegistrationError("provider does not satisfy MammothPersistenceProvider")
        with self._lock:
            if provider_id in self._providers:
                raise MammothProviderRegistrationError(f"provider already registered: {provider_id}")
            self._providers[provider_id] = provider

    def get(self, provider_id: str) -> MammothPersistenceProvider:
        with self._lock:
            try: return self._providers[provider_id]
            except KeyError as exc: raise MammothProviderSelectionError(provider_id) from exc

    def select(self, requirements: MammothProviderRequirements) -> MammothPersistenceProvider:
        with self._lock:
            candidates = sorted(self._providers.values(), key=lambda p: p.provider_id)
        for provider in candidates:
            caps = provider.capabilities
            if all(not required or bool(getattr(caps, field))
                   for field, required in ((f.name, getattr(requirements, f.name)) for f in fields(requirements))):
                return provider
        raise MammothProviderSelectionError("no provider satisfies required capabilities")

    def provider_ids(self) -> tuple[str, ...]:
        with self._lock: return tuple(sorted(self._providers))
