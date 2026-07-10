"""
Aletheus Autonomous Discovery

Post-Genesis 24

Canonical public discovery contract.
"""

from .engine import AutonomousDiscoveryEngine

# Backwards compatibility
DiscoveryEngine = AutonomousDiscoveryEngine

__all__ = [
    "AutonomousDiscoveryEngine",
    "DiscoveryEngine",
]
