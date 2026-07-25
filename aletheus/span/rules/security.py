from ..finding import Severity
from ..rule_engine import Rule

SPAN_SEC_001 = Rule(
    id="SPAN-SEC-001",
    title='Hardcoded secret candidate',
    category="security.secret",
    severity=Severity.CRITICAL,
    predicate=lambda context: bool(context.get("hardcoded_secret_candidates")),
    description='Source text contains a pattern consistent with embedded credentials or private keys.',
    recommendation='Remove the value, rotate the credential, and use an approved secret-management mechanism.',
    confidence=0.95,
    tags=["genesis14", "security"],
)

SPAN_SEC_002 = Rule(
    id="SPAN-SEC-002",
    title='Broad exception handling',
    category="security.resilience",
    severity=Severity.MEDIUM,
    predicate=lambda context: bool(context.get("broad_exception_candidates")),
    description='Broad exception handlers may conceal failures and weaken evidence preservation.',
    recommendation='Catch specific exceptions, preserve causal context, and report failures explicitly.',
    confidence=0.95,
    tags=["genesis14", "security"],
)

RULES = (SPAN_SEC_001, SPAN_SEC_002,)
