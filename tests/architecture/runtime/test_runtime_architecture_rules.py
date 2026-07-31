from __future__ import annotations

from tools.repository.runtime_architecture_audit.boundaries import (
    find_boundary_violations,
)
from tools.repository.runtime_architecture_audit.coupling import (
    calculate_coupling_metrics,
)
from tools.repository.runtime_architecture_audit.models import (
    ImportEdge,
)
from tools.repository.runtime_architecture_audit.rules import (
    DEFAULT_ARCHITECTURE_RULES,
)


def edge(
    source: str,
    target: str,
    line: int = 1,
) -> ImportEdge:
    return ImportEdge(
        source=source,
        target=target,
        line=line,
        imported_name=target.rsplit(".", maxsplit=1)[-1],
        internal=True,
    )


def test_kernel_may_not_import_composition() -> None:
    violations = find_boundary_violations(
        [
            edge(
                "aletheus.runtime.kernel.kernel",
                "aletheus.runtime.composition.root",
            )
        ]
    )

    assert len(violations) == 1
    assert violations[0].rule == "forbidden_dependency"


def test_domains_may_not_import_runtime_core() -> None:
    violations = find_boundary_violations(
        [
            edge(
                "aletheus.runtime.domains.memory",
                "aletheus.runtime.core",
            )
        ]
    )

    assert len(violations) == 1
    assert violations[0].rule == "forbidden_dependency"


def test_composition_may_import_kernel() -> None:
    violations = find_boundary_violations(
        [
            edge(
                "aletheus.runtime.composition.root",
                "aletheus.runtime.kernel.kernel",
            )
        ]
    )

    assert violations == []


def test_same_layer_dependencies_are_allowed() -> None:
    violations = find_boundary_violations(
        [
            edge(
                "aletheus.runtime.kernel.executor",
                "aletheus.runtime.kernel.scheduler",
            )
        ]
    )

    assert violations == []


def test_unknown_packages_are_not_assumed_invalid() -> None:
    violations = find_boundary_violations(
        [
            edge(
                "aletheus.runtime.anchors.memory",
                "aletheus.runtime.anchors.base",
            )
        ],
        DEFAULT_ARCHITECTURE_RULES,
    )

    assert violations == []


def test_coupling_metrics_are_calculated() -> None:
    modules = {
        "aletheus.runtime.composition.root",
        "aletheus.runtime.kernel.kernel",
        "aletheus.runtime.lifecycle.manager",
    }

    metrics = calculate_coupling_metrics(
        module_names=modules,
        imports=[
            edge(
                "aletheus.runtime.composition.root",
                "aletheus.runtime.kernel.kernel",
            ),
            edge(
                "aletheus.runtime.kernel.kernel",
                "aletheus.runtime.lifecycle.manager",
            ),
        ],
    )

    by_module = {metric.module: metric for metric in metrics}

    root = by_module["aletheus.runtime.composition.root"]
    kernel = by_module["aletheus.runtime.kernel.kernel"]
    lifecycle = by_module["aletheus.runtime.lifecycle.manager"]

    assert root.fan_in == 0
    assert root.fan_out == 1
    assert root.instability == 1.0

    assert kernel.fan_in == 1
    assert kernel.fan_out == 1
    assert kernel.instability == 0.5

    assert lifecycle.fan_in == 1
    assert lifecycle.fan_out == 0
    assert lifecycle.instability == 0.0
