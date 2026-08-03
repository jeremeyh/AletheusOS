from dataclasses import replace

from .equations import (
    ambient_drag,
    elasticity_scalar,
    meantime_quotient,
    practical_resonance,
    respiration_wave,
    semantic_gravity,
)
from .models import AmbientField, ResonanceProfile, SpatialBody, VitalityState


class LivingExperienceEngine:
    def step_body(
        self,
        body: SpatialBody,
        target: tuple[float, float, float],
        field: AmbientField,
        dt: float,
    ) -> SpatialBody:
        h = max(0.0, min(0.032, dt)) / 4.0
        x, y, z, vx, vy, vz = body.x, body.y, body.z, body.vx, body.vy, body.vz
        e = elasticity_scalar(field, body.confidence, body.urgency, body.contradiction)
        g = semantic_gravity(body, field)
        for _ in range(4):
            ax = e * (target[0] - x) + ambient_drag(vx, field)
            ay = e * (target[1] - y) + ambient_drag(vy, field)
            az = e * (target[2] - z) + ambient_drag(vz, field) - g * 0.0005
            vx += ax * h
            vy += ay * h
            vz += az * h
            x += vx * h
            y += vy * h
            z += vz * h
        return replace(body, x=x, y=y, z=z, vx=vx, vy=vy, vz=vz)

    def vitality(
        self,
        *,
        coherence: float,
        stability: float,
        continuity: float,
        frame_ms: float,
        target_ms: float,
        latency_ms: float,
        field: AmbientField,
        profile: ResonanceProfile,
        t: float,
    ) -> VitalityState:
        breath = respiration_wave(t, field.respiration_hz)
        vitality = max(0.0, min(1.0, 0.65 * coherence + 0.35 * breath))
        mtq = meantime_quotient(frame_ms, target_ms, stability, continuity)
        resonance = practical_resonance(coherence, vitality, latency_ms, target_ms)
        phase = (
            "crystalline"
            if coherence >= 0.98
            else "quasi-crystalline"
            if coherence >= 0.85
            else "fluid"
            if coherence >= 0.60
            else "nebular"
        )
        return VitalityState(
            round(vitality, 6),
            round(coherence, 6),
            round(resonance, 6),
            round(field.elasticity, 6),
            round(mtq, 6),
            phase,
        )
