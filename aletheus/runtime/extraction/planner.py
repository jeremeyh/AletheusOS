from .models import (
    ExtractionCandidate,
    ExtractionPlan,
)


class RuntimeExtractionPlanner:
    """
    Runtime Extraction Planner™

    Plans the order that runtime/core.py
    responsibilities should be extracted.

    No code is modified here.
    """

    def build(self):

        candidates = [

            ExtractionCandidate(
                name="Lifecycle",
                source="runtime/core.py",
                destination="Runtime Lifecycle Manager",
                estimated_lines=180,
                priority=1,
                confidence=0.99,
                rationale="Already has a dedicated subsystem.",
            ),

            ExtractionCandidate(
                name="Registration",
                source="runtime/core.py",
                destination="Runtime Registration Manager",
                estimated_lines=240,
                priority=2,
                confidence=0.99,
                rationale="Large responsibility cluster.",
            ),

            ExtractionCandidate(
                name="Command Dispatch",
                source="runtime/core.py",
                destination="Runtime Command Registry",
                estimated_lines=260,
                priority=3,
                confidence=0.99,
                rationale="Natural registry ownership.",
            ),

            ExtractionCandidate(
                name="Compatibility",
                source="runtime/core.py",
                destination="Compatibility Manager",
                estimated_lines=120,
                priority=4,
                confidence=0.95,
                rationale="Low-risk extraction.",
            ),

            ExtractionCandidate(
                name="Diagnostics",
                source="runtime/core.py",
                destination="Platform Intelligence",
                estimated_lines=90,
                priority=5,
                confidence=0.95,
                rationale="Reporting belongs outside runtime.",
            ),

            ExtractionCandidate(
                name="Metrics",
                source="runtime/core.py",
                destination="Platform Intelligence",
                estimated_lines=80,
                priority=6,
                confidence=0.94,
                rationale="Observability concern.",
            ),

            ExtractionCandidate(
                name="Applications",
                source="runtime/core.py",
                destination="Application Runtime",
                estimated_lines=300,
                priority=7,
                confidence=0.98,
                rationale="Application ownership.",
            ),

            ExtractionCandidate(
                name="Workflow",
                source="runtime/core.py",
                destination="Workflow Runtime",
                estimated_lines=420,
                priority=8,
                confidence=0.97,
                rationale="Workflow execution belongs elsewhere.",
            ),
        ]

        candidates.sort(
            key=lambda item: item.priority
        )

        return ExtractionPlan(
            candidates=candidates
        )
