"""
Federation Command Registration
Genesis 6 Domain Migration
"""

from aletheus.runtime.domains import FederationDomain


def register_federation_commands(runtime):
    domain = FederationDomain(runtime)
    commands = runtime.commands

    commands.register("federation.bootstrap", domain.bootstrap)
    commands.register("federation.join", domain.join)
    commands.register("federation.leave", domain.leave)
    commands.register("federation.discover", domain.discover)
    commands.register("federation.query", domain.query)
    commands.register("federation.broadcast", domain.broadcast)
    commands.register("federation.statistics", domain.statistics)
