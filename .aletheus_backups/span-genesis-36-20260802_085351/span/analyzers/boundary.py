"""SPAN Boundary Analyzer."""

from __future__ import annotations

from aletheus.span.analyzer import Analyzer
from aletheus.span.finding import Finding, Severity

DEFAULT_RULES = {
    "ui": {"forbidden": {"runtime", "providers"}},
    "applications": {"forbidden": {"providers"}},
}


class BoundaryAnalyzer(Analyzer):
    name = "boundary"
    version = "1.0.0"
    description = "Detect architectural boundary violations."

    required_evidence = ("import",)

    def analyze(self, evidence, context):
        imports = evidence.query(kind="import")
        for rec in imports:
            src = (rec.payload.get("source_module") or "").split(".")
            dst = (rec.payload.get("target_module") or "").split(".")
            if not src or not dst:
                continue
            src_root = src[0]
            dst_root = dst[0]
            rule = DEFAULT_RULES.get(src_root)
            if not rule:
                continue
            if dst_root in rule.get("forbidden", set()):
                yield Finding(
                    analyzer=self.name,
                    category="boundary",
                    title=f"Boundary violation: {src_root} -> {dst_root}",
                    summary=f"{src_root} should not directly depend on {dst_root}.",
                    severity=Severity.HIGH,
                    confidence=0.95,
                    recommendation="Introduce an interface or platform service boundary.",
                    tags=("boundary", "architecture"),
                    metadata={
                        "source_module": rec.payload.get("source_module"),
                        "target_module": rec.payload.get("target_module"),
                        "line": rec.payload.get("line"),
                    },
                )
