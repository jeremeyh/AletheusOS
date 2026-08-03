from __future__ import annotations

from copy import deepcopy
from typing import Any, ClassVar

from ..alternative_generation.engine import Engine as AlternativeGeneration
from ..constitutional_decision.engine import Engine as ConstitutionalDecision
from ..decision_audit.engine import Engine as DecisionAudit
from ..decision_confidence.engine import Engine as DecisionConfidence
from ..decision_context.engine import Engine as DecisionContext
from ..decision_learning.engine import Engine as DecisionLearning
from ..decision_optimization.engine import Engine as DecisionOptimization
from ..decision_policy.engine import Engine as DecisionPolicy
from ..evidence_fusion.engine import Engine as EvidenceFusion
from ..executive_decision_runtime.engine import Engine as ExecutiveDecisionRuntime
from ..explainability.engine import Engine as Explainability
from ..predictive_validation.engine import Engine as PredictiveValidation


class DecisionPipeline:
    """Bounded Genesis 34 strategic decision composition pipeline."""

    VERSION: ClassVar[str] = "34.30.0"

    def __init__(self) -> None:
        self._stages = (
            ExecutiveDecisionRuntime(),
            EvidenceFusion(),
            DecisionContext(),
            AlternativeGeneration(),
            DecisionOptimization(),
            ConstitutionalDecision(),
            PredictiveValidation(),
            DecisionConfidence(),
            Explainability(),
            DecisionPolicy(),
            DecisionAudit(),
            DecisionLearning(),
        )

    def run(self, base_result: Any) -> dict[str, Any]:
        if isinstance(base_result, dict):
            payload = deepcopy(base_result)
        else:
            payload = {"strategicResult": base_result}

        for stage in self._stages:
            payload = stage.execute(payload)

        payload["genesis34DecisionExpansion"] = True
        payload["decisionPipelineVersion"] = self.VERSION
        payload["runtimeHandoff"] = "GENESIS_33"
        payload["operationsHandoff"] = "GENESIS_35"
        payload["humanAuthority"] = "PRESERVED"
        payload["executionAuthorized"] = False
        payload["requiresHumanAuthorization"] = True
        return payload
