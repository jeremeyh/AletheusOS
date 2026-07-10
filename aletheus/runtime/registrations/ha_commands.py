"""
High Availability Command Registration
Genesis 6 Domain Migration
"""

from aletheus.runtime.domains import HighAvailabilityDomain


def register_ha_commands(runtime):
    domain = HighAvailabilityDomain(runtime)
    commands = runtime.commands

    commands.register("ha.bootstrap", domain.bootstrap)
    commands.register("ha.join", domain.join)
    commands.register("ha.leave", domain.leave)
    commands.register("ha.promote", domain.promote)
    commands.register("ha.demote", domain.demote)
    commands.register("ha.failover", domain.failover)
    commands.register("ha.recover", domain.recover)
    commands.register("ha.replicate", domain.replicate)
    commands.register("ha.status", domain.status)
    commands.register("ha.statistics", domain.statistics)
