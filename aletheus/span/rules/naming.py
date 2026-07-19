from ..finding import Severity
from ..rule_engine import Rule


SPAN_NAM_001 = Rule(
    id="SPAN-NAM-001",
    title='Canonical namespace ambiguity',
    category="naming.namespace",
    severity=Severity.MEDIUM,
    predicate=lambda context: bool(context.get("duplicate_namespace_candidates")),
    description='Similar namespaces coexist with singular/plural naming differences.',
    recommendation='Select the canonical term and retain aliases only through explicit compatibility boundaries.',
    confidence=0.95,
    tags=["genesis14", "naming"],
)

SPAN_NAM_002 = Rule(
    id="SPAN-NAM-002",
    title='Root artifact naming ambiguity',
    category="naming.ownership",
    severity=Severity.LOW,
    predicate=lambda context: bool(context.get("root_python_artifacts")),
    description='Root-level module placement obscures package ownership.',
    recommendation='Move the module to its canonical domain package and expose an intentional entry point if needed.',
    confidence=0.95,
    tags=["genesis14", "naming"],
)

RULES = (SPAN_NAM_001, SPAN_NAM_002,)
