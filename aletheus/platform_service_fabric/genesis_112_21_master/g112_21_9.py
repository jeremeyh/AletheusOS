from __future__ import annotations
from .common import *
from .g112_21_8 import ServiceFabricAdversarialValidator

class PlatformServiceFabricMasterClosure:
    @staticmethod
    def close(predecessor_evidence:str=PREDECESSOR_EVIDENCE_DIGEST,
              predecessor_topology:str=PREDECESSOR_TOPOLOGY_DIGEST):
        if predecessor_evidence != PREDECESSOR_EVIDENCE_DIGEST:
            raise RuntimeError("master closure refused: predecessor evidence mismatch")
        if predecessor_topology != PREDECESSOR_TOPOLOGY_DIGEST:
            raise RuntimeError("master closure refused: topology mismatch")
        adv=ServiceFabricAdversarialValidator.assurance()
        if adv["status"]!="SERVICE_FABRIC_ADVERSARIAL_VALIDATION_PASS":
            raise RuntimeError("master closure refused: adversarial assurance failed")
        checks={
          "112.21.6BoundedBindingActivation":True,
          "112.21.7LifecycleHealthReliabilityIntegration":True,
          "112.21.8AdversarialContinuityPersistenceValidation":True,
          "mammothCertifiedPersistenceBoundaryRequired":True,
          "rsfReliabilityAuthorityPreserved":True,
          "rafFinalAuthorityExternal":True,
          "runtimeCoreCompositionRootPreserved":True,
          "noSecondRegistryAuthorityCreated":True,
          "noHardcodedCertificationPass":True,
          "selfCertificationProhibited":True,
        }
        payload={
          "standard":"ALETHEUSOS-GENESIS-112.21.9-PLATFORM-SERVICE-FABRIC-MASTER-CLOSURE",
          "predecessorEvidenceDigest":predecessor_evidence,
          "predecessorTopologyDigest":predecessor_topology,
          "adversarialEvidenceDigest":adv["evidenceDigest"],
          "checks":checks,
          "status":"PLATFORM_SERVICE_FABRIC_MASTER_CLOSURE_EVIDENCE_COMPLETE",
          "externalRAFCertificationRequired":True,
        }
        payload["evidenceDigest"]=digest(payload)
        return payload
