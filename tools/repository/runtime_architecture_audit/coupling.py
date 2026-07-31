from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .models import ImportEdge


@dataclass(frozen=True, slots=True)
class CouplingMetric:
    """Dependency coupling measurements for one runtime module."""

    module: str
    fan_in: int
    fan_out: int
    afferent_coupling: int
    efferent_coupling: int
    instability: float
    inbound_modules: tuple[str, ...]
    outbound_modules: tuple[str, ...]


def calculate_coupling_metrics(
    module_names: set[str],
    imports: list[ImportEdge],
) -> list[CouplingMetric]:
    """Calculate fan-in, fan-out, and instability for every module."""

    inbound: dict[str, set[str]] = defaultdict(set)
    outbound: dict[str, set[str]] = defaultdict(set)

    for edge in imports:
        if not edge.internal:
            continue

        if edge.source not in module_names:
            continue

        target = edge.target

        while target and target not in module_names:
            if "." not in target:
                target = ""
                break

            target = target.rpartition(".")[0]

        if not target:
            continue

        if target == edge.source:
            continue

        outbound[edge.source].add(target)
        inbound[target].add(edge.source)

    metrics: list[CouplingMetric] = []

    for module_name in sorted(module_names):
        inbound_modules = tuple(sorted(inbound[module_name]))
        outbound_modules = tuple(sorted(outbound[module_name]))

        afferent = len(inbound_modules)
        efferent = len(outbound_modules)
        total = afferent + efferent

        instability = round(efferent / total, 4) if total else 0.0

        metrics.append(
            CouplingMetric(
                module=module_name,
                fan_in=afferent,
                fan_out=efferent,
                afferent_coupling=afferent,
                efferent_coupling=efferent,
                instability=instability,
                inbound_modules=inbound_modules,
                outbound_modules=outbound_modules,
            )
        )

    return metrics


def top_coupling_hotspots(
    metrics: list[CouplingMetric],
    limit: int = 20,
) -> list[CouplingMetric]:
    """Return modules with the greatest total dependency coupling."""

    return sorted(
        metrics,
        key=lambda metric: (
            -(metric.afferent_coupling + metric.efferent_coupling),
            -metric.fan_in,
            -metric.fan_out,
            metric.module,
        ),
    )[:limit]
