"""
Health Manager

Genesis 7.2

Owns runtime health reporting.
"""


class HealthManager:

    def __init__(self, runtime):
        self.runtime = runtime


    def health(self):

        return {
            "status": "healthy",
            "booted": getattr(self.runtime, "booted", True),
            "version": getattr(self.runtime, "version", "unknown"),
            "commands":
                len(getattr(self.runtime.commands, "commands", {}))
                if hasattr(self.runtime, "commands")
                else 0,
            "state":
                str(getattr(self.runtime, "state", "unknown")),
        }
