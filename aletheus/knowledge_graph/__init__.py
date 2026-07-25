"""
Aletheus Knowledge Graph package.

The canonical runtime graph is the v2.4 AletheusKnowledgeGraph implementation.
The Post-Genesis 31 graph remains available only through its explicit legacy
type name.
"""

# Import legacy compatibility symbols first. Importing this submodule causes
# Python to temporarily bind the package attribute `knowledge_graph_core` to
# the module itself, so the canonical singleton must be assigned afterward.
from aletheus.knowledge_graph.engine import (
    KnowledgeGraphExpansionEngine,
)
from aletheus.knowledge_graph.graph_core import (
    AletheusKnowledgeGraph,
    GraphNode,
    GraphRelationship,
    InferenceRule,
)
from aletheus.knowledge_graph.graph_core import (
    knowledge_graph_core as _canonical_knowledge_graph_core,
)
from aletheus.knowledge_graph.knowledge_graph_core import (
    KnowledgeGraphCore as LegacyKnowledgeGraphCore,
)

KnowledgeGraphCore = AletheusKnowledgeGraph

# Explicitly restore the canonical runtime singleton after all submodule
# imports have completed.
knowledge_graph_core = _canonical_knowledge_graph_core

__all__ = [
    "AletheusKnowledgeGraph",
    "GraphNode",
    "GraphRelationship",
    "InferenceRule",
    "KnowledgeGraphCore",
    "KnowledgeGraphExpansionEngine",
    "LegacyKnowledgeGraphCore",
    "knowledge_graph_core",
]
