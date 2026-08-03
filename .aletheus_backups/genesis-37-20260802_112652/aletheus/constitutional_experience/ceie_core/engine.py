from ..biophilic_respiration.engine import Engine as Respiration
from ..cognitive_ergonomics.engine import Engine as Ergonomics
from ..information_physics.engine import Engine as Physics
from ..models import ExperienceProjection


class Engine:
    def project(self, signal, context):
        p = Physics()
        mass = p.informational_mass(signal)
        phase = p.phase(signal.veracity)
        density = Ergonomics().density(
            min(1, mass), context.intent_velocity, context.cognitive_load
        )
        breathing = Respiration().cadence_hz(
            max(context.intent_velocity, signal.contradiction), context.reduced_motion
        )
        return ExperienceProjection(
            phase,
            mass,
            density,
            breathing,
            p.tension(signal.contradiction),
            0.0 if context.reduced_motion else max(0.1, 1 - context.cognitive_load),
            True,
            (f"phase:{phase.value}", f"mass:{mass:.4f}", f"density:{density:.4f}"),
        )
