"""Registry for constitutional instrument definitions."""

from __future__ import annotations

from .models import InstrumentDefinition


class DuplicateInstrumentError(ValueError):
    pass


class ConstitutionalInstrumentRegistry:
    """Canonical registry of semantic instruments."""

    VERSION = "0.1.0"

    def __init__(self) -> None:
        self._definitions: dict[
            str,
            InstrumentDefinition,
        ] = {}

    def register(
        self,
        definition: InstrumentDefinition,
        *,
        replace: bool = False,
    ) -> InstrumentDefinition:
        instrument_id = (
            definition.instrument_id
        )

        if (
            instrument_id in self._definitions
            and not replace
        ):
            raise DuplicateInstrumentError(
                f"Instrument {instrument_id!r} "
                "is already registered."
            )

        self._definitions[
            instrument_id
        ] = definition

        return definition

    def get(
        self,
        instrument_id: str,
    ) -> InstrumentDefinition | None:
        return self._definitions.get(
            instrument_id
        )

    def require(
        self,
        instrument_id: str,
    ) -> InstrumentDefinition:
        definition = self.get(
            instrument_id
        )

        if definition is None:
            raise KeyError(
                f"Unknown instrument: "
                f"{instrument_id!r}."
            )

        return definition

    def list(
        self,
    ) -> tuple[InstrumentDefinition, ...]:
        return tuple(
            self._definitions.values()
        )

    def statistics(self) -> dict:
        return {
            "instruments": len(
                self._definitions
            ),
            "instrument_ids": sorted(
                self._definitions
            ),
        }

    def health(self) -> dict:
        return {
            "name": (
                "Constitutional Instrument Registry™"
            ),
            "version": self.VERSION,
            "status": "online",
            **self.statistics(),
        }
