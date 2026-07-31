"""Build the constitutional dependency graph."""

from __future__ import annotations

from typing import Any

from .models import (
    DependencyNode,
    DependencyRelationship,
    PolicyFinding,
)
from .policy import evaluate_dependency
from .taxonomy import capability_owner, infer_capability


def build_dependency_graph(
    repository: dict[str, Any],
    topology: dict[str, Any],
) -> tuple[
    list[DependencyNode],
    list[DependencyRelationship],
    list[PolicyFinding],
    list[str],
]:
    raw_modules = repository.get("modules", [])
    topology_modules = topology.get("modules", [])

    if not isinstance(raw_modules, list):
        raise TypeError("Repository modules must be a list.")
    if not isinstance(topology_modules, list):
        raise TypeError("Topology modules must be a list.")

    module_records: dict[str, dict[str, Any]] = {
        str(item.get("module")): item
        for item in raw_modules
        if isinstance(item, dict) and isinstance(item.get("module"), str)
    }

    nodes: dict[str, DependencyNode] = {}
    relationships: list[DependencyRelationship] = []
    findings: list[PolicyFinding] = []
    unresolved: list[str] = []

    root_nodes = (
        DependencyNode("constitutional:truth", "constitutional_root", "Truth"),
        DependencyNode(
            "constitutional:principle_x",
            "constitutional_root",
            "Principle X",
        ),
        DependencyNode(
            "constitutional:constitution",
            "constitutional_root",
            "Universal Constitution",
        ),
        DependencyNode(
            "constitutional:governance",
            "governance",
            "Constitutional Governance",
        ),
        DependencyNode(
            "runtime:crk",
            "runtime",
            "Constitutional Runtime Kernel",
        ),
    )
    for node in root_nodes:
        nodes[node.node_id] = node

    relationships.extend(
        [
            DependencyRelationship(
                "constitutional:principle_x",
                "constitutional:truth",
                "grounded_in",
                1.0,
            ),
            DependencyRelationship(
                "constitutional:constitution",
                "constitutional:principle_x",
                "grounded_in",
                1.0,
            ),
            DependencyRelationship(
                "constitutional:governance",
                "constitutional:constitution",
                "governed_by",
                1.0,
            ),
            DependencyRelationship(
                "runtime:crk",
                "constitutional:governance",
                "governed_by",
                1.0,
            ),
        ]
    )

    for module, record in sorted(module_records.items()):
        owner = record.get("owner")
        owner_value = owner if isinstance(owner, str) else None
        capability = infer_capability(module, owner_value)

        module_id = f"module:{module}"
        nodes[module_id] = DependencyNode(
            node_id=module_id,
            node_type="module",
            name=module,
            owner=owner_value,
            capability=capability,
            evidence=(str(record.get("path", "")),),
        )

        package = record.get("package")
        if isinstance(package, str):
            package_id = f"package:{package}"
            nodes.setdefault(
                package_id,
                DependencyNode(
                    node_id=package_id,
                    node_type="package",
                    name=package,
                ),
            )
            relationships.append(
                DependencyRelationship(
                    module_id,
                    package_id,
                    "belongs_to",
                    1.0,
                    evidence=(str(record.get("path", "")),),
                )
            )

        if capability is None:
            unresolved.append(module)
            continue

        capability_id = f"capability:{capability}"
        nodes.setdefault(
            capability_id,
            DependencyNode(
                node_id=capability_id,
                node_type="capability",
                name=capability,
                owner=capability_owner(capability),
            ),
        )
        relationships.append(
            DependencyRelationship(
                module_id,
                capability_id,
                "provides",
                0.85,
                evidence=(str(record.get("path", "")),),
            )
        )

        if capability == "Constitutional Runtime Kernel":
            relationships.append(
                DependencyRelationship(
                    capability_id,
                    "runtime:crk",
                    "depends_on",
                    1.0,
                )
            )
        else:
            relationships.append(
                DependencyRelationship(
                    capability_id,
                    "runtime:crk",
                    "depends_on",
                    0.75,
                    evidence=("inferred platform execution dependency",),
                )
            )

    for item in topology_modules:
        if not isinstance(item, dict):
            continue
        source_module = item.get("module")
        outgoing = item.get("outgoing", [])
        if not isinstance(source_module, str) or not isinstance(outgoing, list):
            continue

        source_record = module_records.get(source_module, {})
        source_owner = source_record.get("owner")
        source_capability = infer_capability(
            source_module,
            source_owner if isinstance(source_owner, str) else None,
        )

        for target_module in outgoing:
            if not isinstance(target_module, str):
                continue
            target_record = module_records.get(target_module, {})
            target_owner = target_record.get("owner")
            target_capability = infer_capability(
                target_module,
                target_owner if isinstance(target_owner, str) else None,
            )
            evidence = (
                str(source_record.get("path", "")),
                str(target_record.get("path", "")),
            )

            finding = evaluate_dependency(
                source_module,
                source_capability,
                target_module,
                target_capability,
                evidence,
            )
            policy_status = "violation" if finding else "allowed"
            relationships.append(
                DependencyRelationship(
                    source=f"module:{source_module}",
                    target=f"module:{target_module}",
                    relationship="imports",
                    confidence=1.0,
                    evidence=evidence,
                    policy_status=policy_status,
                )
            )
            if finding:
                findings.append(finding)

    return (
        sorted(nodes.values(), key=lambda item: (item.node_type, item.node_id)),
        relationships,
        sorted(findings, key=lambda item: (item.severity, item.code, item.source)),
        sorted(set(unresolved)),
    )
