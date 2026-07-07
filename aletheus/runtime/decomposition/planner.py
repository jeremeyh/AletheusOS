from .analyzer import RuntimeCoreAnalyzer
from .models import DecompositionPlan
from .responsibility import ResponsibilityExtractor


class RuntimeCoreDecompositionPlanner:
    """
    Produces a migration map for reducing runtime/core.py responsibility.
    """

    def __init__(self, path: str = "aletheus/runtime/core.py"):
        self.path = path

    def plan(self) -> DecompositionPlan:
        core = RuntimeCoreAnalyzer(self.path).analyze()
        findings = ResponsibilityExtractor(self.path).extract()

        estimated_remaining = len(findings)

        # Higher means more responsibility remains compressed inside core.py.
        runtime_compression_index = min(
            100.0,
            round((core.line_count / 4000.0) * 70 + estimated_remaining * 2.5, 2),
        )

        return DecompositionPlan(
            core=core,
            findings=findings,
            estimated_remaining_responsibilities=estimated_remaining,
            runtime_compression_index=runtime_compression_index,
        )
