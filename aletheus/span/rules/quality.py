from ..finding import Severity
from ..rule_engine import Rule

SPAN_QUA_001 = Rule(
    id="SPAN-QUA-001",
    title='Oversized module pressure',
    category="quality.maintainability",
    severity=Severity.MEDIUM,
    predicate=lambda context: bool(context.get("oversized_modules")),
    description='A source module exceeds the Genesis 14 advisory size threshold.',
    recommendation='Review responsibility boundaries and extract cohesive components where evidence supports decomposition.',
    confidence=0.95,
    tags=["genesis14", "quality"],
)

SPAN_QUA_002 = Rule(
    id="SPAN-QUA-002",
    title='Direct print statement',
    category="quality.observability",
    severity=Severity.LOW,
    predicate=lambda context: bool(context.get("print_statement_candidates")),
    description='Direct print statements appear in implementation modules.',
    recommendation='Use the platform logging, telemetry, or reporting boundary for production observability.',
    confidence=0.95,
    tags=["genesis14", "quality"],
)

RULES = (SPAN_QUA_001, SPAN_QUA_002,)
