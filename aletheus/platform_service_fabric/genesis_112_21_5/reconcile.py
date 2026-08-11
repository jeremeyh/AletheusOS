from __future__ import annotations
from collections import defaultdict
from .models import TopologyNode, TopologyEdge, TopologyFinding, TopologyClassification

class TopologyReconciler:
    @staticmethod
    def reconcile(nodes: tuple[TopologyNode,...], edges: tuple[TopologyEdge,...], evidence: dict):
        findings = []
        node_ids = {n.node_id for n in nodes}

        for missing in evidence.get("missingCanonicalNodes", []):
            findings.append(TopologyFinding(
                subject=missing,
                classification=TopologyClassification.ORPHANED,
                reason="Canonical node has no installed implementation surface."
            ))

        authority_by_edge = {}
        for e in edges:
            if e.source not in node_ids or e.target not in node_ids:
                findings.append(TopologyFinding(
                    subject=f"{e.source}->{e.target}",
                    classification=TopologyClassification.ORPHANED,
                    reason="Topology edge references an unavailable node."
                ))
                continue
            key=(e.source,e.target,e.relation)
            prior=authority_by_edge.get(key)
            if prior and prior != e.authority:
                findings.append(TopologyFinding(
                    subject=f"{e.source}->{e.target}:{e.relation}",
                    classification=TopologyClassification.CONFLICTING,
                    reason="Conflicting authority detected for identical topology edge."
                ))
            else:
                authority_by_edge[key]=e.authority

        for n in nodes:
            findings.append(TopologyFinding(
                subject=n.node_id,
                classification=TopologyClassification.BOUNDED_EXTERNAL if n.owner_domain=="RSF" else TopologyClassification.CANONICAL,
                reason="Installed surface reconciled to canonical 112.21.3 binding."
            ))

        for rel in evidence.get("dormantKnownSurfaces", []):
            findings.append(TopologyFinding(
                subject=rel,
                classification=TopologyClassification.DORMANT,
                reason="Known dormant/non-canonical surface preserved without authority."
            ))

        blockers=[f for f in findings if f.classification in {TopologyClassification.ORPHANED,TopologyClassification.CONFLICTING}]
        return tuple(findings), tuple(blockers)
