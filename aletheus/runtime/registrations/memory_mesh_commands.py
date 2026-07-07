"""
Memory Mesh Command Registration

Genesis 6
"""

def register_memory_mesh_commands(runtime):

    commands = runtime.commands

    commands.register(
        "memory.mesh.store",
        runtime._cmd_memory_mesh_store,
    )

    commands.register(
        "memory.mesh.retrieve",
        runtime._cmd_memory_mesh_retrieve,
    )

    commands.register(
        "memory.mesh.search",
        runtime._cmd_memory_mesh_search,
    )

    commands.register(
        "memory.mesh.snapshot",
        runtime._cmd_memory_mesh_snapshot,
    )

    commands.register(
        "memory.mesh.restore",
        runtime._cmd_memory_mesh_restore,
    )

    commands.register(
        "memory.mesh.replicate",
        runtime._cmd_memory_mesh_replicate,
    )

    commands.register(
        "memory.mesh.sync",
        runtime._cmd_memory_mesh_sync,
    )

    commands.register(
        "memory.mesh.history",
        runtime._cmd_memory_mesh_history,
    )

    commands.register(
        "memory.mesh.cache",
        runtime._cmd_memory_mesh_cache,
    )

    commands.register(
        "memory.mesh.stats",
        runtime._cmd_memory_mesh_stats,
    )
