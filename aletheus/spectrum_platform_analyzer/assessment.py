"""
Spectrum Platform Analyzer
Architectural Assessment

Genesis 54.0
"""

from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso

from datetime import datetime
import uuid

from .models import (
    PlatformFinding,
    PlatformReport,
    PlatformScore,
    FindingType,
    Severity,
)
from .registry import SpectrumRegistry
from .hotspots import hotspot_analyzer
from .boundary_analysis import boundary_analyzer


class ArchitecturalAssessment:

    VERSION = "1.0.0"

    GENESIS = "54.0"

    def __init__(self):

        self.registry = SpectrumRegistry()

    # --------------------------------------------------

    def assess(self, root: str):

        score = PlatformScore()

        #
        # Hotspots
        #

        for hotspot in hotspot_analyzer.large_components(root):

            finding = PlatformFinding(

                finding_id=f"SPA-{uuid.uuid4().hex[:8].upper()}",

                finding_type=FindingType.GOD_OBJECT,

                severity=(
                    Severity.HIGH
                    if hotspot["classification"] == "GOD_OBJECT"
                    else Severity.MEDIUM
                ),

                title="Oversized Component",

                description=(
                    f'{hotspot["file"]} contains '
                    f'{hotspot["lines"]} lines.'
                ),

                component=hotspot["file"],

                recommendation=(
                    "Reduce responsibility by extracting "
                    "focused managers/components."
                ),

            )

            self.registry.add_finding(finding)

            score.maintainability -= 2

        #
        # Boundary Violations
        #

        for violation in boundary_analyzer.analyze(root):

            finding = PlatformFinding(

                finding_id=f"SPA-{uuid.uuid4().hex[:8].upper()}",

                finding_type=FindingType.BOUNDARY,

                severity=Severity.MEDIUM,

                title="Boundary Violation",

                description=(
                    f'{violation["module"]} imports '
                    f'{violation["import"]}'
                ),

                component=violation["module"],

                recommendation=(
                    "Respect subsystem boundaries "
                    "or introduce shared contracts."
                ),

            )

            self.registry.add_finding(finding)

            score.boundaries -= 5

        #
        # Clamp scores
        #

        score.architecture = max(score.architecture, 0)

        score.boundaries = max(score.boundaries, 0)

        score.maintainability = max(
            score.maintainability,
            0,
        )

        report = PlatformReport(

            report_id=f"REPORT-{uuid.uuid4().hex[:8].upper()}",

            generated_at=utc_now_iso(),

            score=score,

            findings=self.registry.findings(),

            metadata={

                "genesis": self.GENESIS,

                "version": self.VERSION,

            },

        )

        self.registry.add_report(report)

        return report

    # --------------------------------------------------

    def statistics(self):

        return self.registry.statistics()

    # --------------------------------------------------

    def health(self):

        return {

            "name": "Architectural Assessment",

            "status": "healthy",

            "version": self.VERSION,

            "genesis": self.GENESIS,

        }


architectural_assessment = ArchitecturalAssessment()
