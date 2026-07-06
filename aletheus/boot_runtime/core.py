from __future__ import annotations

from .executor import BootExecutor


class BootRuntime:

    GENESIS = "13.9"
    VERSION = "0.1.0"

    def __init__(self):

        self.executor = BootExecutor()

    def execute(self, plan):

        return self.executor.execute(plan)

    def health(self):

        return {
            "name": "Boot Runtime",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
        }

    def statistics(self):

        return self.health()


boot_runtime = BootRuntime()
