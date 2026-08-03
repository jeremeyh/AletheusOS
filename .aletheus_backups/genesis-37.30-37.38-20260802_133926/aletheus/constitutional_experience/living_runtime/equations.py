from math import exp, pi, sin, sqrt, tanh

from .models import AmbientField, ResonanceProfile, SpatialBody


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(v)))


def critical_damping(stiffness: float, mass: float) -> float:
    if stiffness < 0 or mass <= 0:
        raise ValueError("invalid spring parameters")
    return 2.0 * sqrt(stiffness * mass)


def respiration_wave(t: float, hz: float = 0.15) -> float:
    return 0.5 + 0.5 * sin(2.0 * pi * hz * t)


def resonance_gain(driving_hz: float, profile: ResonanceProfile) -> float:
    natural = max(profile.natural_frequency_hz, 1e-9)
    r = driving_hz / natural
    d = sqrt((1.0 - r * r) ** 2 + (2.0 * profile.damping_ratio * r) ** 2)
    return profile.coupling_strength / max(d, 1e-9)


def elasticity_scalar(
    field: AmbientField, confidence: float, urgency: float, contradiction: float
) -> float:
    stress = 0.55 * clamp(urgency) + 0.45 * clamp(contradiction)
    return max(
        0.05,
        field.elasticity * (0.65 + 0.35 * clamp(confidence)) * (1.0 - 0.55 * stress),
    )


def semantic_gravity(body: SpatialBody, field: AmbientField) -> float:
    return field.gravity * max(0.0, body.mass) * (0.5 + 0.5 * clamp(body.confidence))


def ambient_drag(v: float, field: AmbientField) -> float:
    return -field.viscosity * v - field.turbulence * v * abs(v)


def temporal_coherence(dt: float, half_life: float) -> float:
    return exp(-max(0.0, dt) * 0.6931471805599453 / max(half_life, 1e-9))


def manifold_compression(distance: float, curvature: float) -> float:
    c = sqrt(abs(curvature)) if curvature else 1.0
    return tanh(c * max(0.0, distance))


def meantime_quotient(
    frame_ms: float, target_ms: float, stability: float, continuity: float
) -> float:
    frame = target_ms / max(target_ms, frame_ms)
    return clamp(frame * (0.5 * clamp(stability) + 0.5 * clamp(continuity)))


def practical_resonance(
    coherence: float, vitality: float, latency_ms: float, target_ms: float
) -> float:
    latency = target_ms / max(target_ms, latency_ms)
    return clamp((0.55 * clamp(coherence) + 0.45 * clamp(vitality)) * latency)
