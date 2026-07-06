"""
AletheusOS
Genesis 51.0

Constitutional Library™

Knowledge Index
"""

from __future__ import annotations

from collections import defaultdict

from .models import (
    KnowledgeObject,
)
from .registry import constitutional_library_registry


class ConstitutionalKnowledgeIndex:
    """
    Canonical indexing services.

    The index accelerates retrieval.

    It never owns knowledge.
    """

    GENESIS = "51.0"
    VERSION = "1.0.0"

    def __init__(self) -> None:

        self.rebuild()

    #
    # Index Construction
    #

    def rebuild(self) -> None:

        self._title: dict[str, list[str]] = defaultdict(list)

        self._article: dict[str, list[str]] = defaultdict(list)

        self._identity: dict[str, list[str]] = defaultdict(list)

        self._reason: dict[str, list[str]] = defaultdict(list)

        self._memory: dict[str, list[str]] = defaultdict(list)

        self._type: dict[str, list[str]] = defaultdict(list)

        for knowledge in constitutional_library_registry.all():

            kid = knowledge.knowledge_id

            #
            # Title
            #

            self._title[
                knowledge.title.lower()
            ].append(kid)

            #
            # Type
            #

            self._type[
                knowledge.knowledge_type.value
            ].append(kid)

            #
            # Constitutional Articles
            #

            for article in knowledge.constitutional_articles:

                self._article[
                    article
                ].append(kid)

            #
            # Related identities
            #

            for identity in knowledge.related_identities:

                self._identity[
                    identity
                ].append(kid)

            #
            # Related memories
            #

            for memory in knowledge.related_memories:

                self._memory[
                    memory
                ].append(kid)

            #
            # Related reasons
            #

            for reason in knowledge.related_reasons:

                self._reason[
                    reason
                ].append(kid)

    #
    # Lookup Helpers
    #

    def by_title(
        self,
        title: str,
    ) -> list[KnowledgeObject]:

        ids = self._title.get(
            title.lower(),
            [],
        )

        return [
            constitutional_library_registry.get(i)
            for i in ids
            if constitutional_library_registry.get(i)
        ]

    def by_article(
        self,
        article: str,
    ) -> list[KnowledgeObject]:

        ids = self._article.get(
            article,
            [],
        )

        return [
            constitutional_library_registry.get(i)
            for i in ids
            if constitutional_library_registry.get(i)
        ]

    def by_identity(
        self,
        identity: str,
    ) -> list[KnowledgeObject]:

        ids = self._identity.get(
            identity,
            [],
        )

        return [
            constitutional_library_registry.get(i)
            for i in ids
            if constitutional_library_registry.get(i)
        ]

    def by_reason(
        self,
        reason: str,
    ) -> list[KnowledgeObject]:

        ids = self._reason.get(
            reason,
            [],
        )

        return [
            constitutional_library_registry.get(i)
            for i in ids
            if constitutional_library_registry.get(i)
        ]

    def by_memory(
        self,
        memory: str,
    ) -> list[KnowledgeObject]:

        ids = self._memory.get(
            memory,
            [],
        )

        return [
            constitutional_library_registry.get(i)
            for i in ids
            if constitutional_library_registry.get(i)
        ]

    def by_type(
        self,
        knowledge_type: str,
    ) -> list[KnowledgeObject]:

        ids = self._type.get(
            knowledge_type,
            [],
        )

        return [
            constitutional_library_registry.get(i)
            for i in ids
            if constitutional_library_registry.get(i)
        ]

    #
    # Diagnostics
    #

    def health(self) -> dict:

        return {

            "name": "Constitutional Knowledge Index",

            "genesis": self.GENESIS,

            "version": self.VERSION,

            "status": "healthy",

            "title_index": len(self._title),

            "article_index": len(self._article),

            "identity_index": len(self._identity),

            "memory_index": len(self._memory),

            "reason_index": len(self._reason),

            "type_index": len(self._type),
        }


constitutional_knowledge_index = (
    ConstitutionalKnowledgeIndex()
)
