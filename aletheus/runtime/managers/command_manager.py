"""
Command Manager

Genesis 7.4
Genesis 11.5

Canonical runtime command surface authority.

Command registration is owned by the runtime boot pipeline and
RuntimeCommandBootstrapper. This manager exposes command-state operations
after composition and does not initiate runtime bootstrap.
"""


class CommandManager:
    def __init__(self, runtime):
        self.runtime = runtime

    def count(self):
        return self.runtime.commands.count()

    def list(self):
        return self.runtime.commands.list()

    def status(self):
        return {
            "registered": self.count(),
            "healthy": self.count() > 0,
        }
