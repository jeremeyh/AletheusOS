from __future__ import annotations


class RuntimeErrorBase(Exception):
    """Base class for runtime-specific exceptions."""


class ComponentAlreadyRegisteredError(RuntimeErrorBase):
    """Raised when a duplicate component is registered."""


class ComponentNotFoundError(RuntimeErrorBase):
    """Raised when a component cannot be found."""


class ComponentDependencyError(RuntimeErrorBase):
    """Raised when component dependencies cannot be satisfied."""


class ComponentLifecycleError(RuntimeErrorBase):
    """Raised when a lifecycle transition fails."""
