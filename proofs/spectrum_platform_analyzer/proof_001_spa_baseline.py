"""
Spectrum Platform Analyzer

Proof 001

Baseline Platform Analysis

Genesis 54.4
"""

from __future__ import annotations

from pathlib import Path
from pprint import pprint

from aletheus.spectrum_platform_analyzer.analyzer import (
    SpectrumPlatformAnalyzer,
)
from aletheus.spectrum_platform_analyzer.assessment import (
    architectural_assessment,
)
from aletheus.spectrum_platform_analyzer.boundary_analysis import (
    boundary_analyzer,
)
from aletheus.spectrum_platform_analyzer.circular_dependencies import (
    circular_dependency_analyzer,
)
from aletheus.spectrum_platform_analyzer.dependency import (
    dependency_analyzer,
)
from aletheus.spectrum_platform_analyzer.duplicate_capability import (
    duplicate_capability_analyzer,
)
from aletheus.spectrum_platform_analyzer.hotspots import (
    hotspot_analyzer,
)
from aletheus.spectrum_platform_analyzer.report_writer import (
    report_writer,
)


def header(title: str) -> None:
    print()
    print(title)
    print("=" * len(title))


def main() -> None:
    root = Path("aletheus")

    spa = SpectrumPlatformAnalyzer()

    header("SPA HEALTH")
    pprint(spa.health())

    header("PLATFORM CENSUS")
    pprint(spa.census(str(root)))

    header("DEPENDENCY HEALTH")
    pprint(dependency_analyzer.health())

    header("TOP FAN OUT")
    pprint(dependency_analyzer.top_fan_out(str(root), limit=10))

    header("TOP FAN IN")
    pprint(dependency_analyzer.top_fan_in(str(root), limit=10))

    header("HOTSPOT HEALTH")
    pprint(hotspot_analyzer.health())

    header("GOD OBJECTS")
    pprint(hotspot_analyzer.god_objects(str(root))[:10])

    header("BOUNDARY HEALTH")
    pprint(boundary_analyzer.health())

    header("BOUNDARY SUMMARY")
    pprint(boundary_analyzer.summary(str(root)))

    header("DUPLICATE CAPABILITY HEALTH")
    pprint(duplicate_capability_analyzer.health())

    header("DUPLICATE CAPABILITY SUMMARY")
    pprint(duplicate_capability_analyzer.summary(str(root)))

    header("TOP DUPLICATE CAPABILITIES")
    pprint(duplicate_capability_analyzer.analyze(str(root))[:20])

    header("CIRCULAR DEPENDENCY HEALTH")
    pprint(circular_dependency_analyzer.health())

    header("CIRCULAR DEPENDENCY SUMMARY")
    pprint(circular_dependency_analyzer.summary(str(root)))

    header("CIRCULAR DEPENDENCIES")
    pprint(circular_dependency_analyzer.analyze(str(root))[:20])

    header("ARCHITECTURAL ASSESSMENT")
    report = architectural_assessment.assess(str(root))
    pprint(report.to_dict())

    json_file = report_writer.write_json(report)
    markdown_file = report_writer.write_markdown(report)

    header("REPORT FILES")
    print(json_file)
    print(markdown_file)

    assert report.score.overall() >= 0
    assert "genesis" in report.metadata
    assert json_file.exists()
    assert markdown_file.exists()

    header("SPA BASELINE PROOF PASSED")


if __name__ == "__main__":
    main()
