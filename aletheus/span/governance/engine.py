from .decision import Decision
from .policy_registry import PolicyRegistry


class GovernanceEngine:
    def __init__(self, registry=None):
        self.registry=registry or PolicyRegistry.default()

    def evaluate_metric(self,name,value):
        decisions=[]
        for p in self.registry.policies():
            if p.name.endswith(name.replace("_","-").title()) or \
               (name=="fan_out" and p.name=="Maximum Fan-Out") or \
               (name=="fan_in" and p.name=="Maximum Fan-In"):
                passed=value<=p.threshold
                decisions.append(
                    Decision(
                        policy=p.name,
                        passed=passed,
                        observed=value,
                        threshold=p.threshold,
                        message=("PASS" if passed else p.recommendation),
                    )
                )
        return decisions
