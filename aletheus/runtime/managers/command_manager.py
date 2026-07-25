"""
Command Manager

Genesis 7.4

Canonical command surface authority.
"""

from aletheus.runtime.command_bootstrap.bootstrapper import RuntimeCommandBootstrapper


class CommandManager:

    def __init__(self, runtime):

        self.runtime = runtime
        self.bootstrapper = RuntimeCommandBootstrapper()


    def bootstrap(self):

        self.bootstrapper.bootstrap(
            self.runtime
        )

        return self.status()


    def count(self):

        return self.runtime.commands.count()


    def list(self):

        return self.runtime.commands.list()


    def status(self):

        return {

            "registered":
                self.count(),

            "bootstrapper":
                type(self.bootstrapper).__name__,

            "healthy":
                self.count() > 0
        }
