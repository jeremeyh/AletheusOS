from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib

class ReconstructionPlanner:
    """Produces a bounded implementation plan. It never mutates runtime/core.py."""
    @staticmethod
    def build(repository_root: str, reconciliation) -> dict:
        root=Path(repository_root).resolve()
        if reconciliation.reconciliationStatus != "RECONCILED_AND_READY":
            raise RuntimeError("reconstruction refused: reconciliation not ready")
        plan={
            "schemaVersion":"1.0.1",
            "standard":"ALETHEUSOS-GENESIS-112.21-RECONSTRUCTION-PLAN",
            "generatedAtIso":datetime.now(timezone.utc).isoformat(),
            "mode":"BOUNDED_EXTENSION",
            "target":"aletheus/platform_service_fabric/genesis_112_21",
            "runtimeCoreMutationAllowed":False,
            "mammothPersistenceRequired":True,
            "rsfReliabilityAuthorityPreserved":True,
            "externalRafFinalAuthorityPreserved":True,
            "collisionsRequireExplicitReconciliation":list(reconciliation.collisionSurfaces),
            "phases":[
                "112.21.1 repository reconnaissance",
                "112.21.2 authority and collision map",
                "112.21.3 canonical service contract",
                "112.21.4 binding and topology model",
                "112.21.5 runtime composition adapters",
                "112.21.6 Mammoth-backed durable fabric evidence",
                "112.21.7 RSF reliability integration",
                "112.21.8 adversarial and constitutional validation",
                "112.21.9 closure evidence pending external RAF certification",
            ],
        }
        raw=json.dumps(plan,sort_keys=True,separators=(",",":")).encode()
        plan["evidenceDigest"]="sha256:"+hashlib.sha256(raw).hexdigest()
        return plan
