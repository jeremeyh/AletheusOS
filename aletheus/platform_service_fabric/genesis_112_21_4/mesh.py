from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Iterable, Tuple
import hashlib, json

@dataclass(frozen=True)
class ConnectionEdge:
    source: str
    target: str
    relation: str
    authority: str

class ConnectionMesh:
    """Declarative connection topology. It routes relationships; it does not absorb authority."""
    def __init__(self):
        self._edges: Dict[Tuple[str,str,str], ConnectionEdge] = {}

    def connect(self, source: str, target: str, relation: str, authority: str) -> ConnectionEdge:
        if not all((source, target, relation, authority)):
            raise ValueError("connection mesh refuses incomplete edge")
        key=(source,target,relation)
        candidate=ConnectionEdge(source,target,relation,authority)
        prior=self._edges.get(key)
        if prior and prior != candidate:
            raise ValueError("conflicting connection authority refused")
        self._edges[key]=candidate
        return candidate

    def dependencies_of(self, service_id: str) -> Tuple[str,...]:
        return tuple(sorted(e.target for e in self._edges.values()
                            if e.source == service_id and e.relation == "DEPENDS_ON"))

    def edges(self) -> Tuple[ConnectionEdge,...]:
        return tuple(sorted(self._edges.values(), key=lambda e:(e.source,e.target,e.relation,e.authority)))

    def digest(self) -> str:
        raw=json.dumps([e.__dict__ for e in self.edges()], sort_keys=True, separators=(",",":")).encode()
        return "sha256:"+hashlib.sha256(raw).hexdigest()
