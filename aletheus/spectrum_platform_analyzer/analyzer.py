"""
Spectrum Platform Analyzer

Genesis 54.0
"""

from __future__ import annotations

import os
from pathlib import Path

from .registry import SpectrumRegistry


class SpectrumPlatformAnalyzer:

    VERSION = "1.0.0"

    GENESIS = "54.0"

    def __init__(self):

        self.registry = SpectrumRegistry()

    # --------------------------------------------------
    # Platform Discovery
    # --------------------------------------------------

    def discover(self, root: str):

        root_path = Path(root)

        packages = []
        modules = []
        python_files = []

        for current, dirs, files in os.walk(root_path):

            dirs[:] = [
                d for d in dirs
                if d != "__pycache__"
                and not d.startswith(".")
            ]

            if "__init__.py" in files:
                packages.append(current)

            for file in files:

                if file.endswith(".py"):

                    python_files.append(
                        os.path.join(current, file)
                    )

                    if file != "__init__.py":

                        modules.append(file)

        return {
            "root": str(root_path),
            "packages": sorted(packages),
            "python_files": sorted(python_files),
            "modules": sorted(modules),
            "package_count": len(packages),
            "module_count": len(modules),
            "python_file_count": len(python_files),
        }

    # --------------------------------------------------
    # Census
    # --------------------------------------------------

    def census(self, root: str):

        discovery = self.discover(root)

        return {
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "packages": discovery["package_count"],
            "modules": discovery["module_count"],
            "python_files": discovery["python_file_count"],
        }

    # --------------------------------------------------
    # Health
    # --------------------------------------------------

    def health(self):

        return {
            "name": "Spectrum Platform Analyzer",
            "status": "healthy",
            "version": self.VERSION,
            "genesis": self.GENESIS,
            "registry": self.registry.statistics(),
        }
