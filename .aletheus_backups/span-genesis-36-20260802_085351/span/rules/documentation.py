from ..finding import Severity
from ..rule_engine import Rule

SPAN_DOC_001 = Rule(
    id="SPAN-DOC-001",
    title="Module documentation missing",
    category="documentation.module",
    severity=Severity.LOW,
    predicate=lambda context: bool(context.get("missing_module_docstrings")),
    description="One or more implementation modules do not define a module-level docstring.",
    recommendation="Add concise purpose, ownership, and boundary documentation to public modules.",
    confidence=0.95,
    tags=["genesis14", "documentation"],
)

SPAN_DOC_002 = Rule(
    id="SPAN-DOC-002",
    title="Public symbol documentation missing",
    category="documentation.api",
    severity=Severity.LOW,
    predicate=lambda context: bool(context.get("missing_public_docstrings")),
    description="One or more public classes or functions do not define docstrings.",
    recommendation="Document the contract, parameters, return behavior, and important invariants.",
    confidence=0.95,
    tags=["genesis14", "documentation"],
)

RULES = (
    SPAN_DOC_001,
    SPAN_DOC_002,
)
