from __future__ import annotations


class CommandSurfaceAuditor:
    """
    Genesis 6

    Validates runtime command registration integrity.
    """

    def __init__(self, runtime):
        self.runtime = runtime

    def audit(self):
        commands = getattr(
            self.runtime,
            "commands",
            None,
        )

        if commands is None:
            return {
                "healthy": False,
                "reason": "Command registry unavailable",
            }

        registry = getattr(
            commands,
            "commands",
            {},
        )

        results = []

        for name, handler in registry.items():
            valid = callable(handler)

            results.append(
                {
                    "command": name,
                    "handler": getattr(
                        handler,
                        "__name__",
                        str(handler),
                    ),
                    "valid": valid,
                }
            )

        failures = [item for item in results if not item["valid"]]

        return {
            "healthy": len(failures) == 0,
            "total_commands": len(results),
            "failed_commands": len(failures),
            "commands": results,
        }
