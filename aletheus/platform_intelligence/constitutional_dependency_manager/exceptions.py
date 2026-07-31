"""Exceptions for the Constitutional Dependency Manager."""

from __future__ import annotations


class ConstitutionalDependencyManagerError(Exception):
    """Base exception for CDM failures."""


class DependencyPlanError(ConstitutionalDependencyManagerError):
    """Raised when a dependency plan cannot be created."""


class MissingDependencyError(DependencyPlanError):
    """Raised when a declared dependency is not registered."""


class DependencyCycleError(DependencyPlanError):
    """Raised when the service dependency graph contains a cycle."""


class DependencyNodeNotFoundError(ConstitutionalDependencyManagerError):
    """Raised when a requested service is not registered."""
