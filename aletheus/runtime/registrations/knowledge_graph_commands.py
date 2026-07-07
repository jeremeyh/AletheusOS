"""
Knowledge Graph Command Registration

Genesis 6
"""

def register_knowledge_graph_commands(runtime):

    commands = runtime.commands

    commands.register("knowledge.entity.create", runtime._cmd_kg_entity_create)
    commands.register("knowledge.entity.update", runtime._cmd_kg_entity_update)
    commands.register("knowledge.entity.delete", runtime._cmd_kg_entity_delete)
    commands.register("knowledge.relationship.create", runtime._cmd_kg_relationship_create)
    commands.register("knowledge.relationship.delete", runtime._cmd_kg_relationship_delete)
    commands.register("knowledge.search", runtime._cmd_kg_search)
    commands.register("knowledge.graph", runtime._cmd_kg_graph)
    commands.register("knowledge.neighbors", runtime._cmd_kg_neighbors)
    commands.register("knowledge.infer", runtime._cmd_kg_infer)
    commands.register("knowledge.bootstrap.cardhawk", runtime._cmd_kg_bootstrap_cardhawk)
    commands.register("knowledge.statistics", runtime._cmd_kg_statistics)
