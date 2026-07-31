"""Kinekt™ Runtime Topology engine."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .chains import longest_chains
from .graph import build_graph
from .loader import load_repository_report
from .models import ModuleTopology, TopologyReport
from .packages import package_topology
from .reporting import write_reports
from .scc import cycle_groups, strongly_connected_components


class TopologyEngine:
    def __init__(self, source: Path, output: Path) -> None:
        self.source = source.resolve()
        self.output = output.resolve()

    def analyze(self) -> TopologyReport:
        payload = load_repository_report(self.source)
        raw_modules = payload["modules"]
        graph, package_by_module = build_graph(raw_modules)

        components = strongly_connected_components(graph)
        cycles = cycle_groups(graph, components)

        modules = [
            ModuleTopology(
                module=module,
                package=package_by_module.get(module, "unknown"),
                incoming=tuple(sorted(graph.incoming.get(module, set()))),
                outgoing=tuple(sorted(graph.outgoing.get(module, set()))),
                fan_in=graph.fan_in(module),
                fan_out=graph.fan_out(module),
            )
            for module in sorted(graph.nodes)
        ]

        entry_points = [
            module.module
            for module in modules
            if module.fan_in == 0 and module.fan_out > 0
        ]
        sinks = [
            module.module
            for module in modules
            if module.fan_in > 0 and module.fan_out == 0
        ]
        isolated = [
            module.module
            for module in modules
            if module.fan_in == 0 and module.fan_out == 0
        ]

        report = TopologyReport(
            generated_at=datetime.now(UTC).isoformat(),
            source_report=str(self.source),
            modules=modules,
            packages=package_topology(graph, package_by_module, cycles),
            entry_points=entry_points,
            sinks=sinks,
            isolated=isolated,
            strongly_connected_components=components,
            cycles=cycles,
            longest_chains=longest_chains(graph, components),
        )
        write_reports(report, self.output)
        return report
