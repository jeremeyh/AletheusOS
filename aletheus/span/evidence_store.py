"""Thread-safe normalized evidence store for SPAN™."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass, field
from hashlib import sha256
from pathlib import Path
from threading import RLock
from typing import Any


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    """Normalized fact collected by a SPAN provider."""

    kind: str
    provider: str
    source: str
    payload: Mapping[str, Any]
    confidence: float = 1.0
    location: str | None = None
    tags: tuple[str, ...] = ()
    record_id: str = ""

    def __post_init__(self) -> None:
        if not self.kind.strip():
            raise ValueError("kind cannot be empty")
        if not self.provider.strip():
            raise ValueError("provider cannot be empty")
        if not self.source.strip():
            raise ValueError("source cannot be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")

        object.__setattr__(self, "tags", tuple(dict.fromkeys(self.tags)))

        if not self.record_id:
            stable = {
                "kind": self.kind,
                "provider": self.provider,
                "source": self.source,
                "location": self.location,
                "payload": self.payload,
            }
            digest = sha256(
                json.dumps(stable, sort_keys=True, default=str).encode("utf-8")
            ).hexdigest()[:24]
            object.__setattr__(self, "record_id", f"evidence:{digest}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "kind": self.kind,
            "provider": self.provider,
            "source": self.source,
            "location": self.location,
            "confidence": self.confidence,
            "tags": list(self.tags),
            "payload": dict(self.payload),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> EvidenceRecord:
        return cls(
            record_id=str(payload.get("record_id", "")),
            kind=str(payload["kind"]),
            provider=str(payload["provider"]),
            source=str(payload["source"]),
            location=payload.get("location"),
            confidence=float(payload.get("confidence", 1.0)),
            tags=tuple(str(value) for value in payload.get("tags", ())),
            payload=dict(payload.get("payload", {})),
        )


@dataclass(slots=True)
class EvidenceStore:
    """Indexed in-memory evidence store with deterministic serialization."""

    _records: dict[str, EvidenceRecord] = field(default_factory=dict, init=False)
    _kind_index: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set), init=False
    )
    _provider_index: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set), init=False
    )
    _source_index: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set), init=False
    )
    _tag_index: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set), init=False
    )
    _lock: RLock = field(default_factory=RLock, init=False, repr=False)

    def __len__(self) -> int:
        with self._lock:
            return len(self._records)

    def __iter__(self) -> Iterator[EvidenceRecord]:
        return iter(self.all())

    def add(self, record: EvidenceRecord) -> str:
        with self._lock:
            existing = self._records.get(record.record_id)
            if existing is not None and existing != record:
                raise ValueError(f"evidence ID collision: {record.record_id}")
            if existing is not None:
                return record.record_id

            self._records[record.record_id] = record
            self._kind_index[record.kind].add(record.record_id)
            self._provider_index[record.provider].add(record.record_id)
            self._source_index[record.source].add(record.record_id)
            for tag in record.tags:
                self._tag_index[tag].add(record.record_id)
            return record.record_id

    def extend(self, records: Iterable[EvidenceRecord]) -> tuple[str, ...]:
        return tuple(self.add(record) for record in records)

    def get(self, record_id: str) -> EvidenceRecord | None:
        with self._lock:
            return self._records.get(record_id)

    def all(self) -> tuple[EvidenceRecord, ...]:
        with self._lock:
            return tuple(self._records[key] for key in sorted(self._records))

    def query(
        self,
        *,
        kind: str | None = None,
        provider: str | None = None,
        source: str | None = None,
        tags: Iterable[str] | None = None,
    ) -> tuple[EvidenceRecord, ...]:
        with self._lock:
            candidate_ids: set[str] | None = None

            def intersect(ids: set[str]) -> None:
                nonlocal candidate_ids
                candidate_ids = (
                    set(ids) if candidate_ids is None else candidate_ids & ids
                )

            if kind is not None:
                intersect(self._kind_index.get(kind, set()))
            if provider is not None:
                intersect(self._provider_index.get(provider, set()))
            if source is not None:
                intersect(self._source_index.get(source, set()))
            if tags is not None:
                for tag in tags:
                    intersect(self._tag_index.get(tag, set()))

            if candidate_ids is None:
                candidate_ids = set(self._records)

            return tuple(self._records[key] for key in sorted(candidate_ids))

    def summary(self) -> dict[str, Any]:
        with self._lock:
            kinds = Counter(record.kind for record in self._records.values())
            providers = Counter(record.provider for record in self._records.values())
            return {
                "total_records": len(self._records),
                "kinds": dict(sorted(kinds.items())),
                "providers": dict(sorted(providers.items())),
            }

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "records": [record.to_dict() for record in self.all()],
        }

    def write_json(self, path: str | Path) -> Path:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True, default=str) + "\n",
            encoding="utf-8",
        )
        return destination

    @classmethod
    def read_json(cls, path: str | Path) -> EvidenceStore:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        store = cls()
        store.extend(
            EvidenceRecord.from_dict(item) for item in payload.get("records", ())
        )
        return store
