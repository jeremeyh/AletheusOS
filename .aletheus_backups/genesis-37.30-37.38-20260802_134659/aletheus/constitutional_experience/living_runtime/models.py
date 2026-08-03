from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SpatialBody:
    body_id: str
    mass: float
    x: float
    y: float
    z: float
    vx: float = 0.0
    vy: float = 0.0
    vz: float = 0.0
    confidence: float = 0.5
    urgency: float = 0.0
    contradiction: float = 0.0


@dataclass(frozen=True, slots=True)
class AmbientField:
    gravity: float = 1.0
    elasticity: float = 0.6
    viscosity: float = 0.25
    turbulence: float = 0.08
    respiration_hz: float = 0.15
    curvature: float = -1.0


@dataclass(frozen=True, slots=True)
class ResonanceProfile:
    natural_frequency_hz: float
    damping_ratio: float
    coupling_strength: float
    harmonic_order: int = 3


@dataclass(frozen=True, slots=True)
class VitalityState:
    vitality: float
    coherence: float
    resonance: float
    elasticity: float
    meantime_quotient: float
    phase: str
