"""
CardHawk OS™
Platform Exception Hierarchy
"""

class CardHawkError(Exception):
    """Base exception for all CardHawk OS errors."""


class ConfigurationError(CardHawkError):
    """Raised when configuration is invalid."""


class ServiceRegistrationError(CardHawkError):
    """Raised when a service cannot be registered."""


class ServiceNotFoundError(CardHawkError):
    """Raised when requesting an unknown service."""


class EngineRegistrationError(CardHawkError):
    """Raised when an engine cannot be registered."""


class EngineNotFoundError(CardHawkError):
    """Raised when requesting an unknown engine."""


class ProviderRegistrationError(CardHawkError):
    """Raised when a provider cannot be registered."""


class ProviderNotFoundError(CardHawkError):
    """Raised when requesting an unknown provider."""


class EventBusError(CardHawkError):
    """Raised for event bus failures."""


class SchedulerError(CardHawkError):
    """Raised for scheduler failures."""


class HealthCheckError(CardHawkError):
    """Raised for health check failures."""
