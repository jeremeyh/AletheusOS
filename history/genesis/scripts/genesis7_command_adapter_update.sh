#!/bin/bash

set -e

echo "=== Genesis 7 Command Adapter Extraction ==="


echo "Creating adapters package..."

mkdir -p aletheus/runtime/adapters


cat > aletheus/runtime/adapters/__init__.py <<'PY'
"""
AletheusOS Runtime Command Adapter Layer

Genesis 7

Compatibility boundary between
CommandBus and runtime capabilities.
"""
PY


echo "Creating Graph Command Adapter..."

cat > aletheus/runtime/adapters/graph_adapter.py <<'PY'
"""
Graph Command Adapter

Genesis 7

Extracted from runtime/core.py
"""

from __future__ import annotations


class GraphCommandAdapter:

    def __init__(self, runtime):
        self.runtime = runtime


    def entity_create(self, context):

        payload = context.payload

        entity = self.runtime.knowledge.create_entity(
            label=payload.get(
                "label",
                "Untitled Entity",
            ),
            entity_type=payload.get(
                "entity_type",
                "generic",
            ),
            properties=payload.get(
                "properties",
                {},
            ),
        )

        self.runtime.memory.remember(
            key="entity_created",
            value=entity.to_dict(),
            namespace="aletheus.knowledge",
            memory_type="semantic",
            tags=[
                "entity",
                "knowledge",
            ],
        )

        context.add_result(
            "entity",
            entity.to_dict(),
        )

        return context


    def entity_search(self, context):

        payload = context.payload

        context.add_result(
            "entities",
            self.runtime.knowledge.search_entities(
                label=payload.get(
                    "label"
                ),
                entity_type=payload.get(
                    "entity_type"
                ),
            ),
        )

        return context


    def relationship_create(self, context):

        payload = context.payload

        relationship = self.runtime.knowledge.create_relationship(
            source_id=payload.get(
                "source_id",
                "",
            ),
            target_id=payload.get(
                "target_id",
                "",
            ),
            relationship_type=payload.get(
                "relationship_type",
                "related_to",
            ),
            properties=payload.get(
                "properties",
                {},
            ),
        )

        self.runtime.memory.remember(
            key="relationship_created",
            value=relationship.to_dict(),
            namespace="aletheus.knowledge",
            memory_type="semantic",
            tags=[
                "relationship",
                "knowledge",
            ],
        )

        context.add_result(
            "relationship",
            relationship.to_dict(),
        )

        return context


    def relationship_search(self, context):

        payload = context.payload

        context.add_result(
            "relationships",
            self.runtime.knowledge.search_relationships(
                source_id=payload.get(
                    "source_id"
                ),
                target_id=payload.get(
                    "target_id"
                ),
                relationship_type=payload.get(
                    "relationship_type"
                ),
            ),
        )

        return context


    def graph_export(self, context):

        context.add_result(
            "graph",
            self.runtime.knowledge.graph_export(),
        )

        return context


    def graph_query(self, context):

        context.add_result(
            "graph_query",
            self.runtime.knowledge.graph_query(
                context.payload.get(
                    "entity_id",
                    "",
                )
            ),
        )

        return context


    def graph_stats(self, context):

        knowledge = self.runtime.knowledge

        if hasattr(
            knowledge,
            "stats",
        ):
            result = knowledge.stats()

        elif hasattr(
            knowledge,
            "statistics",
        ):
            result = knowledge.statistics()

        else:
            result = {
                "status": "unknown"
            }

        context.add_result(
            "graph_stats",
            result,
        )

        return context
PY



echo "Patching runtime core imports..."

python - <<'PY'
from pathlib import Path

path = Path(
    "aletheus/runtime/core.py"
)

text = path.read_text()


line = (
    "from aletheus.runtime.adapters.graph_adapter "
    "import GraphCommandAdapter"
)


if line not in text:

    marker = (
        "from aletheus.runtime.managers.runtime_facade "
        "import RuntimeFacade"
    )

    text = text.replace(
        marker,
        marker + "\n" + line
    )


if "self.graph_adapter = GraphCommandAdapter(self)" not in text:

    marker = (
        "self.commands = CommandBus(self)"
    )

    text = text.replace(
        marker,
        marker + "\n        self.graph_adapter = GraphCommandAdapter(self)"
    )


path.write_text(text)

PY



echo "Updating graph command registration..."

cat > aletheus/runtime/registrations/graph_commands.py <<'PY'
"""
Graph Command Registration

Genesis 7

Uses GraphCommandAdapter boundary.
"""


def register_graph_commands(runtime):

    commands = runtime.commands

    commands.register(
        "entity.create",
        runtime.graph_adapter.entity_create,
    )

    commands.register(
        "entity.search",
        runtime.graph_adapter.entity_search,
    )

    commands.register(
        "relationship.create",
        runtime.graph_adapter.relationship_create,
    )

    commands.register(
        "relationship.search",
        runtime.graph_adapter.relationship_search,
    )

    commands.register(
        "graph.export",
        runtime.graph_adapter.graph_export,
    )

    commands.register(
        "graph.query",
        runtime.graph_adapter.graph_query,
    )

    commands.register(
        "graph.stats",
        runtime.graph_adapter.graph_stats,
    )
PY



echo "Validation..."

python -m compileall aletheus/runtime


python - <<'PY'
from aletheus.runtime import runtime_core


print(
    {
        "commands":
            runtime_core.commands.count(),

        "graph_adapter":
            type(
                runtime_core.graph_adapter
            ).__name__,

        "genesis6":
            runtime_core.genesis6_validate()["passed"],

        "freeze":
            runtime_core.genesis6_freeze_review()["approved"]
    }
)

PY


echo "=== Genesis 7 Command Adapter Extraction Complete ==="

