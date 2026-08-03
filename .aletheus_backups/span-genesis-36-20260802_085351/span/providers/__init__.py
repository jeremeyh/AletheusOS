"""Built-in SPAN™ evidence providers."""

from .ast import ASTProvider
from .base import Provider, ProviderContext, ProviderResult
from .configuration import ConfigurationProvider
from .filesystem import FilesystemProvider
from .git import GitProvider
from .imports import ImportProvider
from .registry import RegistryProvider
from .runtime import RuntimeProvider

__all__ = [
    "ASTProvider",
    "ConfigurationProvider",
    "FilesystemProvider",
    "GitProvider",
    "ImportProvider",
    "Provider",
    "ProviderContext",
    "ProviderResult",
    "RegistryProvider",
    "RuntimeProvider",
]
