"""Bootstrap Living Constitutional Instrumentation™."""

from __future__ import annotations

from .bus import ConstitutionalInstrumentBus
from .catalog import (
    register_canonical_cognition_instruments,
)
from .cognition_bridge import (
    CognitionInstrumentBridge,
)
from .registry import (
    ConstitutionalInstrumentRegistry,
)


def build_cognition_instrumentation(
    *,
    history_limit: int = 100,
) -> tuple[
    ConstitutionalInstrumentBus,
    CognitionInstrumentBridge,
]:
    registry = ConstitutionalInstrumentRegistry()

    register_canonical_cognition_instruments(registry)

    bus = ConstitutionalInstrumentBus(
        registry=registry,
        history_limit=history_limit,
    )

    bridge = CognitionInstrumentBridge(bus=bus)

    return bus, bridge
