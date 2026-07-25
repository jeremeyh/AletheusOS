"""
AletheusOS
Genesis 51.0

Constitutional Library™

Core Services
"""

from __future__ import annotations

from .governance import constitutional_library_governance
from .models import (
    KnowledgeObject,
    KnowledgeType,
    new_knowledge_id,
)
from .registry import constitutional_library_registry
from .retrieval import constitutional_library_retrieval


class ConstitutionalLibrary:
    """
    Constitutional institutional knowledge.

    The Constitutional Library stores,
    governs, retrieves and evolves
    institutional knowledge.

    It never determines truth.

    It preserves governed knowledge.
    """

    GENESIS = "51.0"
    VERSION = "1.0.0"

    def create(
        self,
        *,
        title: str,
        statement: str,
        knowledge_type: KnowledgeType,
        confidence: float = 0.0,
        constitutional_articles: list[str] | None = None,
        supporting_evidence: list[str] | None = None,
        related_identities: list[str] | None = None,
        related_memories: list[str] | None = None,
        related_reasons: list[str] | None = None,
        execution_graph_nodes: list[str] | None = None,
        provenance: dict | None = None,
        metadata: dict | None = None,
    ) -> KnowledgeObject:

        knowledge = KnowledgeObject(

            knowledge_id=new_knowledge_id(),

            title=title,

            statement=statement,

            knowledge_type=knowledge_type,

            confidence=confidence,

            constitutional_articles=constitutional_articles or [],

            supporting_evidence=supporting_evidence or [],

            related_identities=related_identities or [],

            related_memories=related_memories or [],

            related_reasons=related_reasons or [],

            execution_graph_nodes=execution_graph_nodes or [],

            provenance=provenance or {},

            metadata=metadata or {},
        )

        constitutional_library_registry.register(
            knowledge
        )

        return knowledge

    #
    # Governance
    #

    def validate(
        self,
        knowledge: KnowledgeObject,
    ) -> KnowledgeObject:

        return constitutional_library_governance.validate_only(
            knowledge
        )

    def promote(
        self,
        knowledge: KnowledgeObject,
    ) -> KnowledgeObject:

        return constitutional_library_governance.promote(
            knowledge
        )

    def archive(
        self,
        knowledge: KnowledgeObject,
    ) -> KnowledgeObject:

        return constitutional_library_governance.archive(
            knowledge
        )

    def supersede(
        self,
        knowledge: KnowledgeObject,
    ) -> KnowledgeObject:

        return constitutional_library_governance.supersede(
            knowledge
        )

    #
    # Retrieval
    #

    def search(
        self,
        text: str,
        *,
        canonical_only: bool = False,
    ):

        return constitutional_library_retrieval.search(
            text,
            canonical_only=canonical_only,
        )

    def canonical(self):

        return constitutional_library_retrieval.canonical()

    #
    # Diagnostics
    #

    def health(self) -> dict:

        return {

            "name": "Constitutional Library",

            "genesis": self.GENESIS,

            "version": self.VERSION,

            "status": "healthy",

            "registry":
                constitutional_library_registry.health(),

            "retrieval":
                constitutional_library_retrieval.health(),

            "governance":
                constitutional_library_governance.health(),
        }

    def statistics(self) -> dict:

        return constitutional_library_registry.statistics()


constitutional_library = ConstitutionalLibrary()
