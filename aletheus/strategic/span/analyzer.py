"""Default SPAN™ analyzer."""

from __future__ import annotations

from statistics import fmean
from typing import Iterable

from .models import AnalysisRequest, AnalysisResult, Evidence


class SpectrumPlatformAnalyzer:
    """Evidence-first analyzer for the present platform state.

    Drop 012A supplies a conservative baseline implementation. Future drops
    may compose architecture, runtime, topology, security, and standards
    analyzers through SPARTAN.
    """

    def analyze(
        self,
        request: AnalysisRequest,
        evidence: Iterable[Evidence] = (),
    ) -> AnalysisResult:
        evidence_tuple = tuple(evidence)
        confidence = (
            fmean(item.confidence for item in evidence_tuple)
            if evidence_tuple
            else 0.50
        )

        findings = (
            f"Subject identified: {request.subject}",
            "No specialized analyzer has been attached yet.",
            "Further SPARTAN domain evidence is required for a decisive result.",
        )

        return AnalysisResult(
            request_id=request.request_id,
            summary=f"Baseline analysis completed for {request.subject}.",
            findings=findings,
            evidence=evidence_tuple,
            confidence=confidence,
            risks=("Insufficient specialized evidence may limit precision.",),
        )
