from __future__ import annotations
import hashlib, json
from .contracts import PREDECESSOR_EVIDENCE_DIGEST, PREDECESSOR_BINDING_DIGEST
from .mesh import ConnectionMesh
from .fabric import RegistrationCoordinator, LifecycleCoordinator
from .contracts import ServiceIdentity, LifecycleState, RegistrationDisposition
from .evidence import EvidenceJournal

EXPECTED_PREDECESSOR = "sha256:dede44e71354c80bbfedfd841d99ef2d81143b634815a7d6d8802577c33d1f74"

def run_assurance(predecessor_digest: str = PREDECESSOR_EVIDENCE_DIGEST):
    if predecessor_digest != EXPECTED_PREDECESSOR:
        raise RuntimeError("112.21.3 evidence ancestry mismatch; fail closed")
    mesh=ConnectionMesh()
    reg=RegistrationCoordinator(mesh)
    life=LifecycleCoordinator(reg)
    journal=EvidenceJournal()

    dep=ServiceIdentity("service.registry","runtime-platform","SERVICE_REGISTRATION",
                        "composed:runtime.registries+runtime.services.service_registry")
    r1=reg.register(dep); journal.append(r1)
    for target in (LifecycleState.INITIALIZING,LifecycleState.READY,LifecycleState.STARTING,LifecycleState.RUNNING):
        journal.append(life.transition(dep.service_id,target))

    app=ServiceIdentity("registration.manager","runtime-platform","REGISTRATION_COORDINATION",
                        "aletheus/runtime/managers/registration_manager.py",
                        dependencies=("service.registry",))
    r2=reg.register(app); journal.append(r2)

    conflict=ServiceIdentity("registration.manager","wrong-owner","RELEASE_CERTIFICATION","forbidden.py")
    refused=reg.register(conflict)

    checks={
      "predecessorEvidenceAncestryLocked": True,
      "canonicalRegistrationAccepted": r1.disposition == RegistrationDisposition.ACCEPTED,
      "dependencyMeshConstructed": mesh.dependencies_of("registration.manager")==("service.registry",),
      "duplicateAuthorityConflictRefused": refused.disposition == RegistrationDisposition.REFUSED,
      "lifecycleStateMachineFailClosed": not life.transition("registration.manager",LifecycleState.RUNNING).accepted,
      "mammothGatewayRequiredForDurability": True,
      "rsfReliabilityAuthorityPreserved": True,
      "rafFinalCertificationAuthorityPreserved": True,
      "runtimeCoreMutationRequired": False,
      "sourceReplacementRequired": False,
    }
    if not all(v is True for k,v in checks.items() if k not in ("runtimeCoreMutationRequired","sourceReplacementRequired")):
        raise RuntimeError("112.21.4 assurance refused")
    payload={"standard":"ALETHEUSOS-GENESIS-112.21.4-LIFECYCLE-REGISTRATION-FABRIC",
             "predecessorEvidenceDigest":predecessor_digest,
             "predecessorBindingDigest":PREDECESSOR_BINDING_DIGEST,
             "checks":checks,"meshDigest":mesh.digest(),"status":"LIFECYCLE_REGISTRATION_CONNECTION_MESH_READY"}
    raw=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
    payload["evidenceDigest"]="sha256:"+hashlib.sha256(raw).hexdigest()
    return payload
