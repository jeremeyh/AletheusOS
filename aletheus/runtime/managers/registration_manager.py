"""
Runtime Registration Manager

Version 6.0.0

Genesis 7:
Command composition ownership delegated to bootstrap providers.
"""

from aletheus.runtime.command_bootstrap.bootstrapper import (
    RuntimeCommandBootstrapper,
)


class RegistrationManager:

    def __init__(self, runtime):
        self.runtime = runtime
        self.bootstrapper = RuntimeCommandBootstrapper()

    def register_all(self):

        self.bootstrapper.bootstrap(
            self.runtime
        )

        return {
            "registered": True,
            "commands": self.runtime.commands.count(),
        }
