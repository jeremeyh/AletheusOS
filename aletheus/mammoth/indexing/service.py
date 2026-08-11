from __future__ import annotations
import hashlib, json, os, tempfile
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping

class MammothIndexError(RuntimeError):
    pass

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def sha256_canonical(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode()).hexdigest()

def normalize_terms(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({v.strip().lower() for v in values if v and v.strip()}))

@dataclass(frozen=True)
class IndexDocument:
    object_id: str
    version_id: str
    namespace: str
    object_type: str
    content_type: str
    owner_capability: str
    producer_capability: str
    retention_class: str
    created_at_iso: str
    updated_at_iso: str
    tags: tuple[str, ...] = ()
    semantic_terms: tuple[str, ...] = ()
    attributes: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))

    @staticmethod
    def create(**kw: Any) -> "IndexDocument":
        attrs = MappingProxyType(dict(sorted(dict(kw.pop("attributes", {})).items())))
        return IndexDocument(
            tags=normalize_terms(kw.pop("tags", ())),
            semantic_terms=normalize_terms(kw.pop("semantic_terms", ())),
            attributes=attrs,
            **kw,
        )

    def record(self) -> dict[str, Any]:
        return {
            "object_id": self.object_id,
            "version_id": self.version_id,
            "namespace": self.namespace,
            "object_type": self.object_type,
            "content_type": self.content_type,
            "owner_capability": self.owner_capability,
            "producer_capability": self.producer_capability,
            "retention_class": self.retention_class,
            "created_at_iso": self.created_at_iso,
            "updated_at_iso": self.updated_at_iso,
            "tags": list(self.tags),
            "semantic_terms": list(self.semantic_terms),
            "attributes": dict(self.attributes),
        }

@dataclass(frozen=True)
class DiscoveryQuery:
    namespace: str | None = None
    object_type: str | None = None
    content_type: str | None = None
    owner_capability: str | None = None
    producer_capability: str | None = None
    retention_class: str | None = None
    tags_all: tuple[str, ...] = ()
    semantic_terms_all: tuple[str, ...] = ()
    attributes_all: tuple[tuple[str, str], ...] = ()
    limit: int = 100
    def __post_init__(self):
        if not 1 <= self.limit <= 10000:
            raise MammothIndexError("limit must be 1..10000")

@dataclass(frozen=True)
class IndexHealth:
    healthy: bool
    document_count: int
    journal_entries: int
    issues: tuple[str, ...]

class PersistentIndexingDiscoveryService:
    SCHEMA_VERSION = "1.0.0"
    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.catalog_path = self.root/"mammoth-index-catalog.json"
        self.journal_path = self.root/"mammoth-index-journal.jsonl"
        self._catalog: dict[tuple[str,str], IndexDocument] = {}
        self._load_or_rebuild()

    def _key(self, d: IndexDocument):
        return (d.object_id, d.version_id)

    def _sorted(self):
        return sorted(self._catalog.values(), key=lambda d:(d.namespace,d.object_type,d.object_id,d.version_id))

    def _catalog_envelope(self):
        docs=[d.record() for d in self._sorted()]
        body={"schemaVersion":self.SCHEMA_VERSION,"documents":docs}
        return {**body,"catalogDigest":sha256_canonical(body)}

    def _atomic_write(self, value):
        fd,tmp=tempfile.mkstemp(prefix="catalog.",suffix=".tmp",dir=str(self.root))
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as f:
                json.dump(value,f,sort_keys=True,separators=(",",":"))
                f.write("\n"); f.flush(); os.fsync(f.fileno())
            os.replace(tmp,self.catalog_path)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)

    def _append_event(self, body):
        event={**body,"eventDigest":sha256_canonical(body)}
        with self.journal_path.open("a",encoding="utf-8") as f:
            f.write(canonical_json(event)+"\n"); f.flush(); os.fsync(f.fileno())

    def index(self,d: IndexDocument):
        key=self._key(d)
        e=self._catalog.get(key)
        if e is not None:
            if e.record()!=d.record(): raise MammothIndexError("identity collision")
            return
        self._append_event({"schemaVersion":self.SCHEMA_VERSION,"operation":"UPSERT","document":d.record()})
        self._catalog[key]=d
        self._atomic_write(self._catalog_envelope())

    def get(self,object_id,version_id):
        return self._catalog.get((object_id,version_id))

    def remove_reference(self,object_id,version_id):
        key=(object_id,version_id)
        if key not in self._catalog: return False
        self._append_event({"schemaVersion":self.SCHEMA_VERSION,"operation":"REMOVE_REFERENCE","objectId":object_id,"versionId":version_id})
        del self._catalog[key]
        self._atomic_write(self._catalog_envelope())
        return True

    def discover(self,q: DiscoveryQuery):
        tags=set(normalize_terms(q.tags_all)); terms=set(normalize_terms(q.semantic_terms_all)); attrs=dict(q.attributes_all)
        out=[]
        for d in self._sorted():
            if q.namespace is not None and d.namespace!=q.namespace: continue
            if q.object_type is not None and d.object_type!=q.object_type: continue
            if q.content_type is not None and d.content_type!=q.content_type: continue
            if q.owner_capability is not None and d.owner_capability!=q.owner_capability: continue
            if q.producer_capability is not None and d.producer_capability!=q.producer_capability: continue
            if q.retention_class is not None and d.retention_class!=q.retention_class: continue
            if not tags.issubset(set(d.tags)): continue
            if not terms.issubset(set(d.semantic_terms)): continue
            if any(d.attributes.get(k)!=v for k,v in attrs.items()): continue
            out.append(d)
            if len(out)>=q.limit: break
        return tuple(out)

    def _replay_journal(self):
        rebuilt={}
        if not self.journal_path.exists(): return rebuilt
        for n,line in enumerate(self.journal_path.read_text(encoding="utf-8").splitlines(),1):
            if not line.strip(): continue
            try: event=json.loads(line)
            except json.JSONDecodeError as e: raise MammothIndexError(f"journal corruption line {n}") from e
            digest=event.pop("eventDigest",None)
            if digest!=sha256_canonical(event): raise MammothIndexError(f"journal digest mismatch line {n}")
            op=event.get("operation")
            if op=="UPSERT":
                d=IndexDocument.create(**event["document"]); key=self._key(d)
                if key in rebuilt and rebuilt[key].record()!=d.record(): raise MammothIndexError("journal collision")
                rebuilt[key]=d
            elif op=="REMOVE_REFERENCE":
                rebuilt.pop((event["objectId"],event["versionId"]),None)
            else:
                raise MammothIndexError(f"unknown journal op line {n}")
        return rebuilt

    def rebuild_from_journal(self):
        self._catalog=self._replay_journal()
        self._atomic_write(self._catalog_envelope())

    def _load_or_rebuild(self):
        if self.catalog_path.exists():
            try:
                env=json.loads(self.catalog_path.read_text(encoding="utf-8"))
                body={"schemaVersion":env.get("schemaVersion"),"documents":env.get("documents",[])}
                if body["schemaVersion"]!=self.SCHEMA_VERSION or env.get("catalogDigest")!=sha256_canonical(body):
                    raise MammothIndexError("catalog digest mismatch")
                docs=[IndexDocument.create(**x) for x in body["documents"]]
                self._catalog={self._key(d):d for d in docs}
                return
            except Exception:
                if not self.journal_path.exists(): raise MammothIndexError("catalog corrupt; no verified journal")
        if self.journal_path.exists(): self.rebuild_from_journal()

    def health(self):
        issues=[]
        try:
            if self._replay_journal()!=self._catalog: issues.append("CATALOG_JOURNAL_DIVERGENCE")
        except MammothIndexError as e:
            issues.append(str(e))
        lines=len(self.journal_path.read_text(encoding="utf-8").splitlines()) if self.journal_path.exists() else 0
        return IndexHealth(not issues,len(self._catalog),lines,tuple(issues))
