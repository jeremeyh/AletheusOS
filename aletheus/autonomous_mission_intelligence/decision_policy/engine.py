from __future__ import annotations

from copy import deepcopy
from typing import Any, ClassVar

from .helpers import canonical_digest


class Engine:
    """Decision Policy Engine implementation for the Genesis 34 decision pipeline."""

    VERSION: ClassVar[str] = "34.x"
    CAPABILITY: ClassVar[str] = "Decision Policy Engine"

    def execute(self, payload: dict[str, Any]) -> dict[str, Any]:
        result = deepcopy(payload)
        stages = list(result.get("decisionStages", []))
        stages.append(self.CAPABILITY)
        result["decisionStages"] = stages
        result["humanAuthority"] = "PRESERVED"
        result["executionAuthorized"] = False
        result["requiresHumanAuthorization"] = True
        result["lastDecisionCapability"] = self.CAPABILITY
        result["decisionDigest"] = canonical_digest(result)
        return result
