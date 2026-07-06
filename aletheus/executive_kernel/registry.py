from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass(slots=True)
class KernelDescriptor:
    kernel_id: str
    name: str
    version: str = "1.0"
    description: str = ""
    status: str = "registered"


class ExecutiveKernelRegistry:
    """
    Registry of executive-visible kernels.

    Tracks kernels only. It does not track services, engines,
    applications, commands, or runtime components.
    """

    def __init__(self) -> None:
        self._kernels: Dict[str, KernelDescriptor] = {}

    def register(self, kernel: KernelDescriptor) -> None:
        self._kernels[kernel.kernel_id] = kernel

    def unregister(self, kernel_id: str) -> None:
        self._kernels.pop(kernel_id, None)

    def get(self, kernel_id: str) -> KernelDescriptor | None:
        return self._kernels.get(kernel_id)

    def exists(self, kernel_id: str) -> bool:
        return kernel_id in self._kernels

    def all(self) -> Iterable[KernelDescriptor]:
        return self._kernels.values()

    def count(self) -> int:
        return len(self._kernels)

    def summary(self) -> dict:
        return {
            "registered_kernels": self.count(),
            "kernels": [
                {
                    "id": kernel.kernel_id,
                    "name": kernel.name,
                    "version": kernel.version,
                    "description": kernel.description,
                    "status": kernel.status,
                }
                for kernel in self._kernels.values()
            ],
        }
