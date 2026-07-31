"""
Spectrum Platform Analyzer
Duplicate Capability Analyzer

Genesis 54.3
"""

from __future__ import annotations

import ast
import os
from collections import defaultdict
from pathlib import Path


class DuplicateCapabilityAnalyzer:
    VERSION = "1.0.0"

    GENESIS = "54.3"

    def python_files(self, root):

        files = []

        for current, dirs, filenames in os.walk(root):
            dirs[:] = [d for d in dirs if d != "__pycache__" and not d.startswith(".")]

            for filename in filenames:
                if filename.endswith(".py"):
                    files.append(Path(current) / filename)

        return sorted(files)

    def exported_functions(self, path):

        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))

        except Exception:
            return []

        results = []

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                results.append(node.name)

            elif isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, ast.FunctionDef):
                        if not child.name.startswith("_"):
                            results.append(child.name)

        return results

    def analyze(self, root):

        capability_index = defaultdict(list)

        for file in self.python_files(root):
            for function in self.exported_functions(file):
                capability_index[function].append(str(file))

        duplicates = []

        for capability, locations in capability_index.items():
            if len(locations) > 1:
                duplicates.append(
                    {
                        "capability": capability,
                        "count": len(locations),
                        "locations": sorted(locations),
                    }
                )

        duplicates.sort(
            key=lambda x: (
                -x["count"],
                x["capability"],
            )
        )

        return duplicates

    def summary(self, root):

        duplicates = self.analyze(root)

        return {
            "duplicate_capabilities": len(duplicates),
            "status": ("PASS" if len(duplicates) == 0 else "REVIEW"),
        }

    def health(self):

        return {
            "name": "Duplicate Capability Analyzer",
            "version": self.VERSION,
            "genesis": self.GENESIS,
            "status": "healthy",
        }


duplicate_capability_analyzer = DuplicateCapabilityAnalyzer()
