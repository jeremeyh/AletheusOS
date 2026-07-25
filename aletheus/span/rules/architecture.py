from ..finding import Severity
from ..rule_engine import Rule

SPAN_ARC_001 = Rule(
    id="SPAN-ARC-001",
    title='Parallel namespace ownership',
    category="architecture.boundary",
    severity=Severity.HIGH,
    predicate=lambda context: bool(context.get("duplicate_namespace_candidates")),
    description='Parallel singular and plural namespaces can indicate duplicate authority or unresolved migration lineage.',
    recommendation='Choose one canonical namespace and document or remove the historical alias.',
    confidence=0.95,
    tags=["genesis14", "architecture"],
)

SPAN_ARC_002 = Rule(
    id="SPAN-ARC-002",
    title='Unclassified root Python artifacts',
    category="architecture.organization",
    severity=Severity.MEDIUM,
    predicate=lambda context: bool(context.get("root_python_artifacts")),
    description='Python modules remain in the repository root outside approved entry-point conventions.',
    recommendation='Move each artifact into its owning package or explicitly approve it as a root entry point.',
    confidence=0.95,
    tags=["genesis14", "architecture"],
)

RULES = (SPAN_ARC_001, SPAN_ARC_002,)
