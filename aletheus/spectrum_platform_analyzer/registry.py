"""
Spectrum Platform Analyzer Registry

Genesis 54.0
"""

from __future__ import annotations

from typing import Dict, List

from .models import PlatformFinding, PlatformReport


class SpectrumRegistry:

    VERSION = "1.0.0"

    GENESIS = "54.0"

    def __init__(self):

        self._findings: Dict[str, PlatformFinding] = {}

        self._reports: Dict[str, PlatformReport] = {}

    # --------------------------------------------------
    # Findings
    # --------------------------------------------------

    def add_finding(self, finding: PlatformFinding):

        self._findings[finding.finding_id] = finding

        return finding

    def get_finding(self, finding_id: str):

        return self._findings.get(finding_id)

    def findings(self):

        return list(self._findings.values())

    def clear_findings(self):

        self._findings.clear()

    # --------------------------------------------------
    # Reports
    # --------------------------------------------------

    def add_report(self, report: PlatformReport):

        self._reports[report.report_id] = report

        return report

    def get_report(self, report_id: str):

        return self._reports.get(report_id)

    def reports(self):

        return list(self._reports.values())

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    def statistics(self):

        severity = {}

        finding_types = {}

        for finding in self._findings.values():

            sev = finding.severity.value

            typ = finding.finding_type.value

            severity[sev] = severity.get(sev, 0) + 1

            finding_types[typ] = finding_types.get(typ, 0) + 1

        return {
            "version": self.VERSION,
            "genesis": self.GENESIS,
            "findings": len(self._findings),
            "reports": len(self._reports),
            "severity": severity,
            "finding_types": finding_types,
        }
