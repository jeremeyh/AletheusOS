from aletheus import kernel
from engines.def_engine.engine import run as def_engine
from engines.falcon.engine import run as falcon
from engines.hawk_aeye.engine import run as hawk_aeye
from engines.nest.engine import run as nest
from engines.perch.engine import run as perch
from engines.roost.engine import run as roost
from engines.soar.engine import run as soar
from engines.strike.engine import run as strike
from engines.talon.engine import run as talon
from engines.thorx.engine import run as thorx

CARD_HAWK_ENGINES = [
    ("Hawk A•Eye™", hawk_aeye),
    ("THORᵡ", thorx),
    ("DEF", def_engine),
    ("NEST™", nest),
    ("FALCON™", falcon),
    ("PERCH™", perch),
    ("TALON™", talon),
    ("STRIKE™", strike),
    ("SOAR™", soar),
    ("ROOST™", roost),
]


def register_cardhawk_foundation():
    kernel.services.register(
        "Card Hawk Foundation™", {"status": "online", "type": "reference_application"}
    )
    kernel.services.register("Asset Vault", {"status": "online"})
    kernel.services.register("Portfolio Engine", {"status": "online"})
    kernel.services.register("Marketplace Intelligence", {"status": "online"})
    for name, handler in CARD_HAWK_ENGINES:
        kernel.engines.register(name, handler)
    kernel.commands.register("cardhawk.pipeline", run_cardhawk_pipeline)
    kernel.events.publish(
        "application.registered",
        {"application": "Card Hawk Foundation™"},
        "cardhawk_foundation",
    )


def run_cardhawk_pipeline(context):
    result = kernel.reasoning.run_chain(
        context, [name for name, _ in CARD_HAWK_ENGINES]
    )
    kernel.memory.remember(
        "last_cardhawk_pipeline", result.to_dict(), "cardhawk_foundation"
    )
    return result


def evaluate_asset(payload):
    return kernel.commands.dispatch(
        "cardhawk.pipeline", payload=payload, application="cardhawk_foundation"
    ).to_dict()


register_cardhawk_foundation()
