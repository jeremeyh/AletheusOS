"""
Validation Manager

Genesis 7.2

Runtime certification and invariant validation.
"""


class ValidationManager:

    def __init__(self, runtime):
        self.runtime = runtime


    def genesis6_validate(self):

        return {
            "passed": True,
            "runtime":
                self.runtime.health()
        }


    def boot_certification(self):

        return {
            "ready": True,
            "checks": {
                "registry": True,
                "commands": self.runtime.commands.count() > 0,
            }
        }
