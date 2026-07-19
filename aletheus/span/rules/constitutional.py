from ..finding import Severity
from ..rule_engine import Rule


SPAN_CON_001 = Rule(
    id="SPAN-CON-001",
    title='Constitution document missing',
    category="constitutional.foundation",
    severity=Severity.HIGH,
    predicate=lambda context: bool(context.get("missing_constitution")),
    description='The repository does not expose a canonical constitution document.',
    recommendation='Add a canonical CONSTITUTION.md or docs/CONSTITUTION.md and keep it aligned with platform governance.',
    confidence=0.95,
    tags=["genesis14", "constitutional"],
)

SPAN_CON_002 = Rule(
    id="SPAN-CON-002",
    title='Governance document missing',
    category="constitutional.governance",
    severity=Severity.MEDIUM,
    predicate=lambda context: bool(context.get("missing_governance_docs")),
    description='The repository does not expose a canonical governance document.',
    recommendation='Add GOVERNANCE.md or docs/GOVERNANCE.md defining authority, change control, and exception handling.',
    confidence=0.95,
    tags=["genesis14", "constitutional"],
)

RULES = (SPAN_CON_001, SPAN_CON_002,)
