"""
AletheusOS
Genesis 51.0

Constitutional Library™

Knowledge Registry
"""

from __future__ import annotations

from .models import (
    KnowledgeObject,
    KnowledgeStatus,
    KnowledgeType,
)


class ConstitutionalLibraryRegistry:
    """
    Canonical registry for institutional knowledge.

    Knowledge is immutable in history,
    but evolvable through governed versions.
    """

    GENESIS = "51.0"
    VERSION = "1.0.0"

    def __init__(self) -> None:

        self._knowledge: dict[str, KnowledgeObject] = {}

    #
    # Registration
    #

    def register(
        self,
        knowledge: KnowledgeObject,
    ) -> KnowledgeObject:

        self._knowledge[
            knowledge.knowledge_id
        ] = knowledge

        return knowledge

    #
    # Retrieval
    #

    def get(
        self,
        knowledge_id: str,
    ) -> KnowledgeObject | None:

        return self._knowledge.get(
            knowledge_id
        )

    def all(self) -> list[KnowledgeObject]:

        return sorted(
            self._knowledge.values(),
            key=lambda k: (
                k.title.lower(),
                k.version,
            ),
        )

    #
    # Filtering
    #

    def by_status(
        self,
        status: KnowledgeStatus,
    ) -> list[KnowledgeObject]:

        return [

            knowledge

            for knowledge in self._knowledge.values()

            if knowledge.status == status

        ]

    def by_type(
        self,
        knowledge_type: KnowledgeType,
    ) -> list[KnowledgeObject]:

        return [

            knowledge

            for knowledge in self._knowledge.values()

            if knowledge.knowledge_type == knowledge_type

        ]

    #
    # Search
    #

    def search(
        self,
        text: str,
    ) -> list[KnowledgeObject]:

        query = text.lower()

        results = []

        for knowledge in self._knowledge.values():

            if (
                query in knowledge.title.lower()
                or
                query in knowledge.statement.lower()
            ):

                results.append(
                    knowledge
                )

        return sorted(
            results,
            key=lambda k: (
                k.title.lower(),
                k.version,
            ),
        )

    #
    # Statistics
    #

    def health(self) -> dict:

        return {

            "name": "Constitutional Library Registry",

            "genesis": self.GENESIS,

            "version": self.VERSION,

            "status": "healthy",

            "knowledge_objects": len(
                self._knowledge
            ),
        }

    def statistics(self) -> dict:

        statuses: dict[str, int] = {}

        types: dict[str, int] = {}

        for knowledge in self._knowledge.values():

            statuses.setdefault(
                knowledge.status.value,
                0,
            )

            statuses[
                knowledge.status.value
            ] += 1

            types.setdefault(
                knowledge.knowledge_type.value,
                0,
            )

            types[
                knowledge.knowledge_type.value
            ] += 1

        return {

            "name": "Constitutional Library Registry",

            "genesis": self.GENESIS,

            "version": self.VERSION,

            "knowledge_objects": len(
                self._knowledge
            ),

            "statuses": statuses,

            "knowledge_types": types,
        }


constitutional_library_registry = (
    ConstitutionalLibraryRegistry()
)
