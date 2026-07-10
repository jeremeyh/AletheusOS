"""
Telemetry Command Registration
Genesis 6 Domain Migration
"""

from aletheus.runtime.domains import TelemetryDomain


def register_telemetry_commands(runtime):
    domain = TelemetryDomain(runtime)
    commands = runtime.commands

    commands.register("telemetry.bootstrap", domain.bootstrap)
    commands.register("telemetry.record", domain.record)
    commands.register("telemetry.metric", domain.metric)
    commands.register("telemetry.log", domain.log)
    commands.register("telemetry.trace", domain.trace)
    commands.register("telemetry.health", domain.health)
    commands.register("telemetry.timeline", domain.timeline)
    commands.register("telemetry.statistics", domain.statistics)
