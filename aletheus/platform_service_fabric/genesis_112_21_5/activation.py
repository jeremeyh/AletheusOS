from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple
import hashlib, json
from .models import TopologyNode, TopologyEdge

@dataclass(frozen=True)
class ActivationReceipt:
    activated: bool
    node_count: int
    edge_count: int
    topology_digest: str
    reason: str

class RuntimeConnectionMesh:
    """
    Activates an in-memory topology view only.
    It does not patch runtime/core.py and does not create a second service authority.
    """
    def __init__(self):
        self._nodes: Dict[str,TopologyNode] = {}
        self._edges: Dict[tuple[str,str,str],TopologyEdge] = {}

    def activate(self, nodes: tuple[TopologyNode,...], edges: tuple[TopologyEdge,...]) -> ActivationReceipt:
        if not nodes:
            return ActivationReceipt(False,0,0,self.digest(),"no canonical topology nodes available")
        node_ids={n.node_id for n in nodes}
        for e in edges:
            if e.source not in node_ids or e.target not in node_ids:
                return ActivationReceipt(False,len(nodes),0,self.digest(),"edge references unresolved node")
        self._nodes={n.node_id:n for n in nodes}
        self._edges={(e.source,e.target,e.relation):e for e in edges}
        return ActivationReceipt(True,len(self._nodes),len(self._edges),self.digest(),"bounded runtime connection mesh activated")

    def digest(self) -> str:
        payload={
          "nodes":[n.__dict__ for n in sorted(self._nodes.values(),key=lambda x:x.node_id)],
          "edges":[e.__dict__ for e in sorted(self._edges.values(),key=lambda x:(x.source,x.target,x.relation))]
        }
        raw=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
        return "sha256:"+hashlib.sha256(raw).hexdigest()

    def topology(self):
        return tuple(self._nodes.values()), tuple(self._edges.values())
