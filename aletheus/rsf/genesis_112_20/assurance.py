from __future__ import annotations
from .contracts import *
from .invariants import *
from .adversarial import WholeSystemReliabilityAdversarialValidation

def run_package_assurance() -> dict:
    contract = RSFContractEngine.evaluate_contract("assurance-probe", ReliabilityAssuranceState.HEALTHY)
    adv = WholeSystemReliabilityAdversarialValidation.run()
    checks = {
        "contract_standard": contract.standard == "ALETHEUSOS-RSF-CANONICAL-CONTRACT",
        "healthy_continue": contract.disposition is ReliabilityDisposition.CONTINUE,
        "authority_boundary": contract.authority_boundary.rsf_may_issue_release_certificate is False,
        "adversarial": all(x.passed for x in adv),
    }
    return {"status":"PASS" if all(checks.values()) else "FAIL", "checks":checks}
