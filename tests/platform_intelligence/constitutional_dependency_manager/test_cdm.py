from __future__ import annotations

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalDependencyManager,
    ConstitutionalEventBus,
    DependencyNodeNotFoundError,
    PlatformServiceDefinition,
    PlatformServiceRegistry,
)


def definition(
    address: str,
    *,
    dependencies: tuple[str, ...] = (),
) -> PlatformServiceDefinition:
    return PlatformServiceDefinition.create(
        address=address,
        canonical_name=address,
        version="9.12.0",
        authority="AletheusOS Constitution",
        owner="Platform Intelligence",
        dependencies=dependencies,
    )


def build_manager() -> ConstitutionalDependencyManager:
    registry = PlatformServiceRegistry(event_bus=ConstitutionalEventBus())

    registry.register_many(
        [
            definition("service.runtime"),
            definition(
                "service.event-bus",
                dependencies=("service.runtime",),
            ),
            definition(
                "service.registry",
                dependencies=("service.event-bus",),
            ),
            definition(
                "service.graph",
                dependencies=("service.event-bus",),
            ),
            definition(
                "service.twin",
                dependencies=(
                    "service.registry",
                    "service.graph",
                ),
            ),
            definition(
                "service.explorer",
                dependencies=("service.twin",),
            ),
        ]
    )

    return ConstitutionalDependencyManager(service_registry=registry)


def test_validation_passes() -> None:
    manager = build_manager()

    validation = manager.validate()

    assert validation.valid is True
    assert validation.registered_services == 6
    assert validation.dependency_edges == 6
    assert validation.cycles == ()


def test_boot_plan_is_dependency_ordered() -> None:
    manager = build_manager()

    plan = manager.build_boot_plan()

    assert [level.services for level in plan.levels] == [
        ("service.runtime",),
        ("service.event-bus",),
        (
            "service.graph",
            "service.registry",
        ),
        ("service.twin",),
        ("service.explorer",),
    ]


def test_shutdown_plan_reverses_levels() -> None:
    manager = build_manager()

    plan = manager.build_shutdown_plan()

    assert [level.services for level in plan.levels] == [
        ("service.explorer",),
        ("service.twin",),
        (
            "service.graph",
            "service.registry",
        ),
        ("service.event-bus",),
        ("service.runtime",),
    ]


def test_boot_plan_contains_all_services() -> None:
    manager = build_manager()

    plan = manager.build_boot_plan()

    assert len(plan.ordered_services) == 6
    assert len(set(plan.ordered_services)) == 6


def test_direct_dependencies() -> None:
    manager = build_manager()

    assert manager.dependencies_of("service.twin") == (
        "service.graph",
        "service.registry",
    )


def test_transitive_dependencies() -> None:
    manager = build_manager()

    assert manager.dependencies_of(
        "service.explorer",
        transitive=True,
    ) == (
        "service.event-bus",
        "service.graph",
        "service.registry",
        "service.runtime",
        "service.twin",
    )


def test_direct_dependents() -> None:
    manager = build_manager()

    assert manager.dependents_of("service.event-bus") == (
        "service.graph",
        "service.registry",
    )


def test_transitive_dependents() -> None:
    manager = build_manager()

    assert manager.dependents_of(
        "service.runtime",
        transitive=True,
    ) == (
        "service.event-bus",
        "service.explorer",
        "service.graph",
        "service.registry",
        "service.twin",
    )


def test_restart_plan_includes_dependents() -> None:
    manager = build_manager()

    plan = manager.build_restart_plan("service.registry")

    assert plan.direction == "restart"
    assert plan.ordered_services == (
        "service.registry",
        "service.twin",
        "service.explorer",
    )


def test_restart_leaf_contains_only_leaf() -> None:
    manager = build_manager()

    plan = manager.build_restart_plan("service.explorer")

    assert plan.ordered_services == ("service.explorer",)


def test_unknown_service_is_rejected() -> None:
    manager = build_manager()

    with pytest.raises(DependencyNodeNotFoundError):
        manager.dependencies_of("service.missing")


def test_statistics_are_consistent() -> None:
    manager = build_manager()

    stats = manager.statistics()

    assert stats.services == 6
    assert stats.dependency_edges == 6
    assert stats.boot_levels == 5
    assert stats.maximum_depth == 4
    assert stats.parallel_groups == 1
    assert stats.root_services == 1
    assert stats.leaf_services == 1


def test_export_contains_plans() -> None:
    manager = build_manager()

    payload = manager.export()

    assert payload["validation"]["valid"] is True
    assert "boot_plan" in payload
    assert "shutdown_plan" in payload
    assert "statistics" in payload


def test_manager_is_read_only() -> None:
    manager = build_manager()

    forbidden = {
        "start",
        "stop",
        "boot",
        "execute",
        "transition",
        "report_health",
        "register",
        "publish",
        "connect",
    }

    assert forbidden.isdisjoint(set(dir(manager)))
