"""
Genesis 11
RUF012 Safe Constant Transformer

Phase 1:
    - transforms ONLY safe uppercase constants
    - no shared mutable state
    - no manual-review candidates
"""

from .runner import Runner


def main() -> int:
    Runner().run()
    return 0
