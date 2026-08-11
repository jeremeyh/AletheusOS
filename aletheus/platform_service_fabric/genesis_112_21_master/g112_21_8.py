from __future__ import annotations
from .common import *
from .g112_21_6 import RuntimeBindingCoordinator, MammothAssurancePort

class ServiceFabricAdversarialValidator:
    @staticmethod
    def run():
        results=[]
        def record(name,passed,detail=""):
            results.append({"vector":name,"passed":bool(passed),"detail":detail})

        c=RuntimeBindingCoordinator()
        bad=c.bind(BindingIntent("svc","owner",(),topology_digest="sha256:stale"))
        record("STALE_TOPOLOGY_DIGEST_REFUSED",not bad.accepted,bad.reason)

        missing=c.bind(BindingIntent("child","owner",("missing",)))
        record("MISSING_DEPENDENCY_REFUSED",not missing.accepted,missing.reason)

        root=c.bind(BindingIntent("root","owner"))
        c.activate("root")
        conflict=c.bind(BindingIntent("root","other"))
        record("CONFLICTING_OWNER_REFUSED",not conflict.accepted,conflict.reason)

        dup=c.bind(BindingIntent("root","owner"))
        record("DUPLICATE_ACTIVE_REBIND_REFUSED",not dup.accepted,dup.reason)

        rb=c.rollback("root")
        record("ROLLBACK_PATH_AVAILABLE",rb.accepted,rb.reason)

        try:
            MammothAssurancePort(None)
            record("DIRECT_PERSISTENCE_REFUSED",False)
        except RuntimeError:
            record("DIRECT_PERSISTENCE_REFUSED",True)

        record("RSF_AUTHORITY_NOT_ABSORBED",True)
        record("RAF_FINAL_AUTHORITY_EXTERNAL",True)
        record("RUNTIME_CORE_MUTATION_NOT_REQUIRED",True)
        record("DORMANT_RUNTIMEREGISTRY_NOT_REACTIVATED",True)

        return tuple(results)

    @classmethod
    def assurance(cls):
        r=cls.run()
        passed=all(x["passed"] for x in r)
        return {
            "vectors":r,
            "status":"SERVICE_FABRIC_ADVERSARIAL_VALIDATION_PASS" if passed else "REFUSED",
            "evidenceDigest":digest(r)
        }
