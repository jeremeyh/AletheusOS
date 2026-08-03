from __future__ import annotations

from math import acosh, exp, sqrt

from .models import EvidenceNode


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def informational_mass(node: EvidenceNode) -> float:
    """M_E = w_provenance * w_consensus * Value(E)."""
    return max(0.0, node.utility) * clamp(node.provenance) * clamp(node.consensus)


def consensus_pressure(nodes: list[EvidenceNode]) -> float:
    """Bounded H0-style agreement proxy for runtime clustering."""
    if not nodes:
        return 0.0
    weighted = sum(clamp(node.consensus) * max(0.0, node.utility) for node in nodes)
    normalizer = sum(max(0.0, node.utility) for node in nodes)
    return 0.0 if normalizer == 0 else clamp(weighted / normalizer)


def contradiction_shear(node: EvidenceNode) -> float:
    """Shear = contradiction * (1 + |temporal delta|)."""
    return clamp(node.contradiction) * (1.0 + min(1.0, abs(node.temporal_delta)))


def temporal_momentum(node: EvidenceNode, age_seconds: float) -> float:
    """Momentum decays exponentially while preserving recent change."""
    return node.temporal_delta * exp(-max(0.0, age_seconds) / 86400.0)


def spring_damping(stiffness: float, mass: float, damping_ratio: float) -> float:
    if stiffness < 0 or mass <= 0 or damping_ratio < 0:
        raise ValueError("invalid spring parameters")
    return 2.0 * damping_ratio * sqrt(stiffness * mass)


def poincare_distance(p: tuple[float, ...], q: tuple[float, ...]) -> float:
    if len(p) != len(q) or not p:
        raise ValueError("points must have equal non-zero dimensions")
    p2 = sum(value * value for value in p)
    q2 = sum(value * value for value in q)
    if p2 >= 1.0 or q2 >= 1.0:
        raise ValueError("points must lie inside the unit ball")
    delta2 = sum((a - b) ** 2 for a, b in zip(p, q, strict=True))
    return acosh(1.0 + 2.0 * delta2 / ((1.0 - p2) * (1.0 - q2)))
