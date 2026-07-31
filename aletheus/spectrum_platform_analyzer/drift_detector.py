"""
Spectrum Platform Analyzer
Architectural Drift Detector

Genesis 54.2
"""

from __future__ import annotations

import json
from pathlib import Path


class DriftDetector:
    VERSION = "1.0.0"

    GENESIS = "54.2"

    def load_report(self, report_path):

        report_path = Path(report_path)

        if not report_path.exists():
            return None

        with report_path.open(
            "r",
            encoding="utf-8",
        ) as f:
            return json.load(f)

    def compare(self, previous, current):

        if previous is None:
            return {
                "status": "BASELINE",
                "summary": "No previous report exists.",
                "changes": [],
            }

        previous_score = previous["score"]

        current_score = current["score"]

        changes = []

        for key in sorted(current_score):
            if key == "overall":
                continue

            old = previous_score[key]

            new = current_score[key]

            if old != new:
                changes.append(
                    {
                        "metric": key,
                        "previous": old,
                        "current": new,
                        "delta": round(new - old, 2),
                    }
                )

        return {
            "status": ("UNCHANGED" if not changes else "CHANGED"),
            "summary": (
                "Architecture unchanged."
                if not changes
                else f"{len(changes)} architectural metrics changed."
            ),
            "changes": changes,
        }

    def health(self):

        return {
            "name": "Architectural Drift Detector",
            "version": self.VERSION,
            "genesis": self.GENESIS,
            "status": "healthy",
        }


drift_detector = DriftDetector()
