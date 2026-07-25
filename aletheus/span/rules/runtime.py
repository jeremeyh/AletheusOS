from ..finding import Severity
from ..rule_engine import Rule

SPAN_RUN_001 = Rule(
    id="SPAN-RUN-001",
    title='Direct Runtime Core coupling',
    category="runtime.boundary",
    severity=Severity.HIGH,
    predicate=lambda context: bool(context.get("noncanonical_runtime_imports")),
    description='Modules import runtime.core directly, increasing composition-root coupling.',
    recommendation='Depend on bounded runtime interfaces, registries, or anchor circuits instead of runtime.core internals.',
    confidence=0.95,
    tags=["genesis14", "runtime"],
)

SPAN_RUN_002 = Rule(
    id="SPAN-RUN-002",
    title='God object pressure',
    category="runtime.composition",
    severity=Severity.HIGH,
    predicate=lambda context: bool(context.get("god_object_candidates")),
    description='A class exposes a very large method surface and may be accumulating multiple responsibilities.',
    recommendation='Extract focused managers or services while preserving the composition root as a lightweight orchestrator.',
    confidence=0.95,
    tags=["genesis14", "runtime"],
)

RULES = (SPAN_RUN_001, SPAN_RUN_002,)
