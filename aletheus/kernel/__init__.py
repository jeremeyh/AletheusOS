"""
Aletheus Kernel™

Canonical public kernel namespace.

Implementation currently backed by kernel_v2.
"""

from aletheus.kernel_v2.kernel_core import AletheusAutonomousKernel, kernel_core
from aletheus.kernel_v2.models import KernelEvent, KernelRegistryItem, KernelState

kernel = kernel_core

__all__ = [
    "AletheusAutonomousKernel",
    "kernel_core",
    "kernel",
    "KernelEvent",
    "KernelRegistryItem",
    "KernelState",
]
