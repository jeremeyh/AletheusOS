"""
Intelligence Kernel Command Registration
Genesis 6 Domain Migration
"""

from aletheus.runtime.domains import KernelDomain


def register_kernel_commands(runtime):
    domain = KernelDomain(runtime)
    commands = runtime.commands

    commands.register("kernel.bootstrap", domain.bootstrap)
    commands.register("kernel.execute", domain.execute)
    commands.register("kernel.tasks", domain.tasks)
    commands.register("kernel.scheduler", domain.scheduler)
    commands.register("kernel.dispatcher", domain.dispatcher)
    commands.register("kernel.supervisor", domain.supervisor)
    commands.register("kernel.statistics", domain.statistics)
