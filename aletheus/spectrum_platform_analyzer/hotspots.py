"""
Spectrum Platform Analyzer
Hotspot Analysis

Genesis 54.0
"""

from __future__ import annotations

import os
from pathlib import Path


class HotspotAnalyzer:

    VERSION = "1.0.0"

    GENESIS = "54.0"

    #
    # These are intentionally conservative.
    # SPA will eventually make these configurable.
    #

    GOD_OBJECT_LINE_THRESHOLD = 1000

    LARGE_FILE_THRESHOLD = 600

    MEDIUM_FILE_THRESHOLD = 300

    def python_files(self, root: str):

        root = Path(root)

        results = []

        for current, dirs, files in os.walk(root):

            dirs[:] = [
                d
                for d in dirs
                if d != "__pycache__"
                and not d.startswith(".")
                and d not in {
                    "venv",
                    "node_modules",
                }
            ]

            for file in files:

                if file.endswith(".py"):

                    results.append(
                        Path(current) / file
                    )

        return sorted(results)

    def line_count(self, path: Path):

        try:

            return len(
                path.read_text(
                    encoding="utf-8"
                ).splitlines()
            )

        except Exception:

            return 0

    def classify(self, lines: int):

        if lines >= self.GOD_OBJECT_LINE_THRESHOLD:

            return "GOD_OBJECT"

        if lines >= self.LARGE_FILE_THRESHOLD:

            return "LARGE"

        if lines >= self.MEDIUM_FILE_THRESHOLD:

            return "MEDIUM"

        return "NORMAL"

    def analyze(self, root: str):

        findings = []

        for file in self.python_files(root):

            lines = self.line_count(file)

            findings.append({

                "file": str(file),

                "lines": lines,

                "classification": self.classify(lines),

            })

        findings.sort(

            key=lambda x: x["lines"],

            reverse=True,

        )

        return findings

    def god_objects(self, root: str):

        return [

            item

            for item in self.analyze(root)

            if item["classification"] == "GOD_OBJECT"

        ]

    def large_components(self, root: str):

        return [

            item

            for item in self.analyze(root)

            if item["classification"] in {

                "LARGE",

                "GOD_OBJECT",

            }

        ]

    def health(self):

        return {

            "name": "Spectrum Hotspot Analyzer",

            "version": self.VERSION,

            "genesis": self.GENESIS,

            "status": "healthy",

        }


hotspot_analyzer = HotspotAnalyzer()
