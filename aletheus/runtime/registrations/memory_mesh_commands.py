"""
Memory Mesh Command Registration

Genesis 6 Domain Migration
"""

from aletheus.runtime.domains import MemoryMeshDomain


def register_memory_mesh_commands(runtime):

    domain = MemoryMeshDomain(runtime)
    commands = runtime.commands

    commands.register("memory.mesh.store", domain.store)
    commands.register("memory.mesh.retrieve", domain.retrieve)
    commands.register("memory.mesh.search", domain.search)
    commands.register("memory.mesh.snapshot", domain.snapshot)
    commands.register("memory.mesh.restore", domain.restore)
    commands.register("memory.mesh.replicate", domain.replicate)
    commands.register("memory.mesh.sync", domain.sync)
    commands.register("memory.mesh.history", domain.history)
    commands.register("memory.mesh.cache", domain.cache)
    commands.register("memory.mesh.stats", domain.stats)
