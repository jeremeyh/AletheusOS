from ..finding import Severity
from ..rule_engine import Rule

SPAN_GOV_001 = Rule(
    id="SPAN-GOV-001",
    title='SPAN constitutional package missing',
    category="governance.capability",
    severity=Severity.CRITICAL,
    predicate=lambda context: bool(context.get("missing_span_package")),
    description='The canonical SPAN package is absent from the repository.',
    recommendation='Install and preserve the SPAN constitutional analysis capability.',
    confidence=0.95,
    tags=["genesis14", "governance"],
)

SPAN_GOV_002 = Rule(
    id="SPAN-GOV-002",
    title='Unresolved implementation markers',
    category="governance.completion",
    severity=Severity.LOW,
    predicate=lambda context: bool(context.get("todo_candidates")),
    description='TODO, FIXME, or HACK markers remain in source modules.',
    recommendation='Resolve, ticket, or explicitly govern implementation markers before freezing a Genesis milestone.',
    confidence=0.95,
    tags=["genesis14", "governance"],
)

RULES = (SPAN_GOV_001, SPAN_GOV_002,)
