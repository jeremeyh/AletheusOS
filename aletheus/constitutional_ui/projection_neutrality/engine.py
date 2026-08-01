from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Request:
    modality: str
    audience: str
    detail: str
    provenance: bool = True
    minority_opinions: bool = True


class Engine:
    SUPPORTED = frozenset(
        {
            "axiomux_field",
            "dashboard",
            "executive_report",
            "technical_report",
            "chart_package",
            "statistical_appendix",
            "presentation",
            "spreadsheet",
            "voice",
            "api",
        }
    )

    def project(self, graph: dict[str, Any], request: Request) -> dict[str, Any]:
        if request.modality not in self.SUPPORTED:
            raise ValueError(f"Unsupported projection modality: {request.modality}")
        return {
            "modality": request.modality,
            "audience": request.audience,
            "detailLevel": request.detail,
            "sourceGraphValid": bool(graph.get("valid")),
            "nodes": graph.get("nodes", []),
            "edges": graph.get("edges", []),
            "provenanceIncluded": request.provenance,
            "minorityOpinionsIncluded": request.minority_opinions,
            "projectionNeutralityPreserved": True,
        }
