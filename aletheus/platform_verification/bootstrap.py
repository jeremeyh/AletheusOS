from __future__ import annotations

from .checks.capability_check import capability_check
from .checks.compile_check import compile_check
from .checks.repository_dna_check import repository_dna_check
from .checks.runtime_boot_check import runtime_boot_check
from .checks.unit_test_check import unit_test_check
from .registry import VerificationRegistry


def bootstrap_verification_registry() -> VerificationRegistry:
    registry = VerificationRegistry()

    registry.register(compile_check)
    registry.register(unit_test_check)
    registry.register(repository_dna_check)
    registry.register(runtime_boot_check)
    registry.register(capability_check)

    return registry
