from ..finding import Severity
from ..rule_engine import Rule

SPAN_API_001 = Rule(
    id="SPAN-API-001",
    title="Mutable default argument",
    category="api.contract",
    severity=Severity.HIGH,
    predicate=lambda context: bool(context.get("mutable_default_candidates")),
    description="A public callable uses a mutable list, dict, or set as a default argument.",
    recommendation="Use None as the default and create the mutable value inside the callable.",
    confidence=0.95,
    tags=["genesis14", "api"],
)

SPAN_API_002 = Rule(
    id="SPAN-API-002",
    title="Python syntax failure",
    category="api.integrity",
    severity=Severity.CRITICAL,
    predicate=lambda context: bool(context.get("parse_errors")),
    description="A Python module could not be parsed and cannot participate reliably in analysis or runtime execution.",
    recommendation="Correct the syntax error and rerun compilation and SPAN validation.",
    confidence=0.95,
    tags=["genesis14", "api"],
)

RULES = (
    SPAN_API_001,
    SPAN_API_002,
)
