"""
AletheusOS
Genesis 51.0

Constitutional Library™

Knowledge Retrieval
"""

from __future__ import annotations

from .indexing import constitutional_knowledge_index
from .models import KnowledgeObject, KnowledgeStatus, KnowledgeType
from .registry import constitutional_library_registry


class ConstitutionalLibraryRetrieval:
    """
    Retrieval services for governed institutional knowledge.

    Retrieval does not determine truth.
    Retrieval returns knowledge candidates.
    """

    GENESIS = "51.0"
    VERSION = "1.0.0"

    def search(
        self,
        text: str,
        *,
        canonical_only: bool = False,
    ) -> list[KnowledgeObject]:

        results = constitutional_library_registry.search(text)

        if canonical_only:
            results = [
                knowledge
                for knowledge in results
                if knowledge.status == KnowledgeStatus.CANONICAL
            ]

        return results

    def by_title(
        self,
        title: str,
    ) -> list[KnowledgeObject]:

        return constitutional_knowledge_index.by_title(title)

    def by_article(
        self,
        article: str,
    ) -> list[KnowledgeObject]:

        return constitutional_knowledge_index.by_article(article)

    def by_identity(
        self,
        identity: str,
    ) -> list[KnowledgeObject]:

        return constitutional_knowledge_index.by_identity(identity)

    def by_memory(
        self,
        memory: str,
    ) -> list[KnowledgeObject]:

        return constitutional_knowledge_index.by_memory(memory)

    def by_reason(
        self,
        reason: str,
    ) -> list[KnowledgeObject]:

        return constitutional_knowledge_index.by_reason(reason)

    def by_type(
        self,
        knowledge_type: KnowledgeType,
    ) -> list[KnowledgeObject]:

        return constitutional_library_registry.by_type(knowledge_type)

    def canonical(self) -> list[KnowledgeObject]:

        return constitutional_library_registry.by_status(KnowledgeStatus.CANONICAL)

    def health(self) -> dict:

        return {
            "name": "Constitutional Library Retrieval",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


constitutional_library_retrieval = ConstitutionalLibraryRetrieval()
