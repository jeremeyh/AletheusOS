from __future__ import annotations
import hashlib, json

class TopologyEvidenceBridge:
    @staticmethod
    def build(payload: dict) -> dict:
        raw=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
        return {
            "standard":"ALETHEUSOS-GENESIS-112.21.5-TOPOLOGY-EVIDENCE",
            "payload":payload,
            "evidenceDigest":"sha256:"+hashlib.sha256(raw).hexdigest(),
            "durablePersistenceAuthority":"MAMMOTH",
            "reliabilityAuthority":"RSF",
            "releaseCertificationAuthority":"RAF",
        }

    @staticmethod
    def persist(envelope: dict, mammoth_gateway):
        if mammoth_gateway is None or not callable(getattr(mammoth_gateway,"persist_assurance_evidence",None)):
            raise RuntimeError("Mammoth gateway required; direct topology persistence refused")
        return mammoth_gateway.persist_assurance_evidence(envelope)
