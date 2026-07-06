"""
AletheusOS
Genesis 47.5

Foundation Capability Base™

Base Class
"""

from __future__ import annotations

from abc import ABC

from .metadata import CapabilityMetadata


class FoundationCapability(ABC):
    """
    Base class for every Foundation capability.

    Every constitutional capability derives from this class
    to inherit a common engineering contract.
    """

    def __init__(self, metadata: CapabilityMetadata) -> None:

        self._metadata = metadata

    @property
    def metadata(self) -> CapabilityMetadata:

        return self._metadata

    @property
    def name(self) -> str:

        return self._metadata.name

    @property
    def genesis(self) -> str:

        return self._metadata.genesis

    @property
    def version(self) -> str:

        return self._metadata.version

    @property
    def status(self) -> str:

        return self._metadata.status

    @property
    def certification(self) -> str:

        return self._metadata.certification

    def health(self) -> dict:

        return {
            "name": self.name,
            "genesis": self.genesis,
            "version": self.version,
            "status": self.status,
            "certification": self.certification,
        }

    def statistics(self) -> dict:

        return {
            "name": self.name,
            "genesis": self.genesis,
            "version": self.version,
        }

    def capability_metadata(self) -> dict:

        return self.metadata.to_dict()

    def constitutional_articles(self) -> list[str]:

        return list(self.metadata.constitutional_articles)

    def dependencies(self) -> list[str]:

        return list(self.metadata.dependencies)

    def proofs(self) -> list[str]:

        return list(self.metadata.proofs)
