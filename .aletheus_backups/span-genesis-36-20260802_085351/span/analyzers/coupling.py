"""SPAN Coupling Intelligence Analyzer."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from aletheus.span.analyzer import Analyzer
from aletheus.span.finding import Finding, Severity


@dataclass(frozen=True)
class CouplingMetric:
    module: str
    fan_in: int
    fan_out: int

    @property
    def instability(self) -> float:
        total = self.fan_in + self.fan_out
        return 0.0 if total == 0 else round(self.fan_out / total, 4)

    def to_dict(self):
        return {
            "module": self.module,
            "fan_in": self.fan_in,
            "fan_out": self.fan_out,
            "instability": self.instability,
        }


class CouplingAnalyzer(Analyzer):
    name = "coupling"
    version = "1.0.0"
    description = "Computes architectural coupling metrics."
    required_evidence = ("import",)

    def analyze(self, evidence, context):
        imports = evidence.query(kind="import")

        outgoing = defaultdict(set)
        incoming = defaultdict(set)

        for rec in imports:
            src = rec.payload.get("source_module")
            dst = rec.payload.get("target_module")
            if not src or not dst:
                continue
            outgoing[src].add(dst)
            incoming[dst].add(src)

        self.metrics = {}

        modules = sorted(set(outgoing) | set(incoming))

        for module in modules:
            metric = CouplingMetric(
                module=module,
                fan_in=len(incoming[module]),
                fan_out=len(outgoing[module]),
            )

            self.metrics[module] = metric

            if metric.fan_out >= 25:
                yield Finding(
                    analyzer=self.name,
                    category="coupling",
                    title=f"High fan-out: {module}",
                    summary=f"{module} depends on {metric.fan_out} modules.",
                    severity=Severity.MEDIUM,
                    confidence=0.95,
                    recommendation="Reduce outgoing dependencies.",
                    metadata=metric.to_dict(),
                    tags=("coupling", "fan-out"),
                )

            if metric.fan_in >= 40:
                yield Finding(
                    analyzer=self.name,
                    category="coupling",
                    title=f"High fan-in: {module}",
                    summary=f"{metric.fan_in} modules depend on {module}.",
                    severity=Severity.MEDIUM,
                    confidence=0.95,
                    recommendation="Review API stability and ownership.",
                    metadata=metric.to_dict(),
                    tags=("coupling", "fan-in"),
                )

            if metric.instability > 0.9 and metric.fan_out >= 10:
                yield Finding(
                    analyzer=self.name,
                    category="coupling",
                    title=f"Highly unstable module: {module}",
                    summary=f"Instability={metric.instability}",
                    severity=Severity.HIGH,
                    confidence=0.97,
                    recommendation="Split responsibilities or introduce abstraction.",
                    metadata=metric.to_dict(),
                    tags=("instability",),
                )
