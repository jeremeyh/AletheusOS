from ..finding import Severity
from ..rule_engine import Rule


SPAN_DEP_001 = Rule(
    id="SPAN-DEP-001",
    title='Two-way import cycle candidate',
    category="dependency.cycle",
    severity=Severity.HIGH,
    predicate=lambda context: bool(context.get("circular_import_candidates")),
    description='A pair of modules import one another directly.',
    recommendation='Introduce an interface, event, shared contract, or dependency inversion boundary.',
    confidence=0.95,
    tags=["genesis14", "dependency"],
)

SPAN_DEP_002 = Rule(
    id="SPAN-DEP-002",
    title='Wildcard import usage',
    category="dependency.api",
    severity=Severity.MEDIUM,
    predicate=lambda context: bool(context.get("wildcard_imports")),
    description='Wildcard imports obscure ownership and public API boundaries.',
    recommendation='Replace wildcard imports with explicit symbols or a documented package export.',
    confidence=0.95,
    tags=["genesis14", "dependency"],
)

RULES = (SPAN_DEP_001, SPAN_DEP_002,)
