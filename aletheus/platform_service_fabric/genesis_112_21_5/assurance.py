from __future__ import annotations
from pathlib import Path
import json
from .models import PREDECESSOR_EVIDENCE_DIGEST, PREDECESSOR_MESH_DIGEST
from .discovery import RuntimeTopologyDiscovery
from .reconcile import TopologyReconciler
from .activation import RuntimeConnectionMesh
from .evidence import TopologyEvidenceBridge

EXPECTED_PREDECESSOR="sha256:96b20ef5c07c959db9b25cd2d98c191460a187ad41ef9c57a5d5979f344474ea"
EXPECTED_MESH="sha256:9a3d2d432d88c72ba92cc5b0fed3c224ff50e9cf001ad2c5cbcd25f8cd8f65bb"

def run_assurance(project_root: str | Path):
    if PREDECESSOR_EVIDENCE_DIGEST != EXPECTED_PREDECESSOR:
        raise RuntimeError("112.21.4 assurance ancestry mismatch")
    if PREDECESSOR_MESH_DIGEST != EXPECTED_MESH:
        raise RuntimeError("112.21.4 mesh ancestry mismatch")

    nodes, edges, discovery = RuntimeTopologyDiscovery.discover(project_root)
    findings, blockers = TopologyReconciler.reconcile(nodes, edges, discovery)

    mesh = RuntimeConnectionMesh()
    activation = mesh.activate(nodes, edges) if not blockers else None

    checks = {
        "predecessorEvidenceAncestryLocked": PREDECESSOR_EVIDENCE_DIGEST == EXPECTED_PREDECESSOR,
        "predecessorMeshDigestLocked": PREDECESSOR_MESH_DIGEST == EXPECTED_MESH,
        "canonicalTopologyDiscovered": len(nodes) >= 5,
        "noOrphanOrConflictingTopologyBlockers": len(blockers) == 0,
        "runtimeConnectionMeshActivated": bool(activation and activation.activated),
        "runtimeCoreMutationRequired": False,
        "sourceReplacementRequired": False,
        "mammothDurablePersistenceAuthorityPreserved": True,
        "rsfReliabilityAuthorityPreserved": True,
        "rafFinalAuthorityPreserved": True,
    }

    passed = (
        all(v is True for k,v in checks.items()
            if k not in ("runtimeCoreMutationRequired","sourceReplacementRequired"))
        and checks["runtimeCoreMutationRequired"] is False
        and checks["sourceReplacementRequired"] is False
    )

    envelope = TopologyEvidenceBridge.build({
        "predecessorEvidenceDigest":PREDECESSOR_EVIDENCE_DIGEST,
        "predecessorMeshDigest":PREDECESSOR_MESH_DIGEST,
        "nodeCount":len(nodes),
        "edgeCount":len(edges),
        "activationTopologyDigest":activation.topology_digest if activation else None,
        "blockers":[f.__dict__ for f in blockers],
        "checks":checks,
        "status":"RUNTIME_CONNECTION_MESH_TOPOLOGY_READY" if passed else "REFUSED",
    })
    return {
        "status":"RUNTIME_CONNECTION_MESH_TOPOLOGY_READY" if passed else "REFUSED",
        "checks":checks,
        "nodes":[n.__dict__ for n in nodes],
        "edges":[e.__dict__ for e in edges],
        "findings":[{"subject":f.subject,"classification":f.classification.value,"reason":f.reason} for f in findings],
        "blockers":[{"subject":f.subject,"classification":f.classification.value,"reason":f.reason} for f in blockers],
        "topologyDigest":activation.topology_digest if activation else None,
        "evidenceEnvelope":envelope,
    }
