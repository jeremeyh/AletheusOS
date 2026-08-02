from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar

from ..architectural_anatomy.engine import Engine as Anatomy
from ..architectural_digital_twin.engine import Engine as DigitalTwin
from ..architectural_fitness.engine import Engine as Fitness
from ..architectural_governance.engine import Engine as Governance
from ..architectural_pathology.engine import Engine as Pathology
from ..architectural_physiology.engine import Engine as Physiology
from ..architectural_recommendations.engine import Engine as Recommendations
from ..dependency_intelligence.engine import Engine as Dependencies
from ..evolution_intelligence.engine import Engine as Evolution
from ..expansion_intelligence.engine import Engine as Expansion
from ..repository_intelligence.engine import Engine as Repository
from ..runtime_cartography.engine import Engine as Cartography
from ..spartan_architectural_defense.engine import Engine as Spartan
from .helpers import stable_digest


class Engine:
    VERSION: ClassVar[str] = "36.18.0"
    CAPABILITY: ClassVar[str] = "SPAN Director"

    def __init__(self) -> None:
        self._engines = (
            Repository(),
            Dependencies(),
            Anatomy(),
            Physiology(),
            Fitness(),
            Pathology(),
            Evolution(),
            Cartography(),
            DigitalTwin(),
            Expansion(),
            Recommendations(),
            Governance(),
            Spartan(),
        )

    def analyze(
        self,
        repository_root: str | Path,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        analyses = [
            engine.analyze(repository_root, context=context) for engine in self._engines
        ]
        result = {
            "system": "SPAN",
            "version": self.VERSION,
            "genesis": "36.0-36.18",
            "analysisCount": len(analyses),
            "analyses": analyses,
            "constitutionalStatus": "VERIFIED",
            "spartanStatus": "ACTIVE",
            "humanAuthority": "PRESERVED",
            "executionAuthorized": False,
        }
        result["digest"] = stable_digest(result)
        return result
