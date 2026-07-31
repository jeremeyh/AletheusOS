"""Package-level topology aggregation."""

from __future__ import annotations

from collections import defaultdict

from .graph import DirectedGraph
from .models import PackageTopology


def package_topology(
    graph: DirectedGraph,
    package_by_module: dict[str, str],
    cycles: list[list[str]],
) -> list[PackageTopology]:
    modules_by_package: dict[str, set[str]] = defaultdict(set)
    inbound: dict[str, set[str]] = defaultdict(set)
    outbound: dict[str, set[str]] = defaultdict(set)
    internal_edges: dict[str, int] = defaultdict(int)
    isolated: dict[str, int] = defaultdict(int)
    cycle_counts: dict[str, int] = defaultdict(int)

    for module, package in package_by_module.items():
        modules_by_package[package].add(module)
        if graph.fan_in(module) == 0 and graph.fan_out(module) == 0:
            isolated[package] += 1

    for source in graph.nodes:
        source_package = package_by_module.get(source, "unknown")
        for target in graph.outgoing.get(source, set()):
            target_package = package_by_module.get(target, "unknown")
            if source_package == target_package:
                internal_edges[source_package] += 1
            else:
                outbound[source_package].add(target_package)
                inbound[target_package].add(source_package)

    for cycle in cycles:
        touched = {package_by_module.get(module, "unknown") for module in cycle}
        for package in touched:
            cycle_counts[package] += 1

    return [
        PackageTopology(
            package=package,
            modules=len(modules),
            internal_edges=internal_edges[package],
            inbound_packages=tuple(sorted(inbound[package])),
            outbound_packages=tuple(sorted(outbound[package])),
            cycle_groups=cycle_counts[package],
            isolated_modules=isolated[package],
        )
        for package, modules in sorted(modules_by_package.items())
    ]
