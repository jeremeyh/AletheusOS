"""
Spectrum Platform Analyzer
Boundary Analysis

Genesis 54.0
"""

from __future__ import annotations

from .dependency import dependency_analyzer


class BoundaryAnalyzer:

    VERSION = "1.0.0"

    GENESIS = "54.0"

    #
    # Canonical architectural boundaries.
    #
    # This list will grow as Aletheus grows.
    #

    ALLOWED = {

        #
        # Runtime
        #

        "aletheus.runtime": [

            "aletheus.runtime",

            "aletheus.foundation",

            "aletheus.kernel",

            "aletheus.memory",

            "aletheus.reasoning",

            "aletheus.knowledge",

        ],

        #
        # Memory
        #

        "aletheus.memory": [

            "aletheus.foundation",

            "aletheus.memory",

        ],

        #
        # Knowledge
        #

        "aletheus.knowledge": [

            "aletheus.foundation",

            "aletheus.memory",

            "aletheus.knowledge",

        ],

        #
        # Applications
        #

        "aletheus.applications": [

            "aletheus.foundation",

            "aletheus.runtime",

            "aletheus.applications",

        ],
    }

    def subsystem(self, module: str):

        parts = module.split(".")

        if len(parts) < 2:

            return module

        return ".".join(parts[:2])

    def analyze(self, root: str):

        graph = dependency_analyzer.internal_import_graph(root)

        violations = []

        for module, imports in graph.items():

            source = self.subsystem(module)

            allowed = self.ALLOWED.get(source)

            #
            # Unknown subsystem.
            #

            if allowed is None:

                continue

            for imported in imports:

                target = self.subsystem(imported)

                if target not in allowed:

                    violations.append({

                        "source": source,

                        "module": module,

                        "target": target,

                        "import": imported,

                        "type": "BOUNDARY",

                        "severity": "MEDIUM",

                    })

        return violations

    def summary(self, root: str):

        violations = self.analyze(root)

        return {

            "boundary_violations": len(violations),

            "status": (

                "PASS"

                if len(violations) == 0

                else "FAIL"

            ),

        }

    def health(self):

        return {

            "name": "Boundary Analyzer",

            "version": self.VERSION,

            "genesis": self.GENESIS,

            "status": "healthy",

        }


boundary_analyzer = BoundaryAnalyzer()
