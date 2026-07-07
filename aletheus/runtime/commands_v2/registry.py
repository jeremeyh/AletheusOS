from .models import CommandRecord, CommandResult


class RuntimeCommandRegistry:
    """
    Runtime Command Registry™

    Owns command registration and dispatch.

    Runtime/core.py should eventually delegate command ownership here.
    """

    def __init__(self):
        self.commands = {}

    def register(
        self,
        name: str,
        handler,
        category: str = "general",
        description: str = "",
        metadata=None,
    ):
        record = CommandRecord(
            name=name,
            handler=handler,
            category=category,
            description=description,
            metadata=metadata or {},
        )

        self.commands[name] = record
        return record

    def has(self, name: str) -> bool:
        return name in self.commands

    def dispatch(self, name: str, payload=None):
        payload = payload or {}
        record = self.commands.get(name)

        if record is None:
            return CommandResult(
                command=name,
                status="missing",
                response={"error": f"Command '{name}' is not registered."},
            )

        try:
            response = record.handler(payload)

            return CommandResult(
                command=name,
                status="completed",
                response=response if isinstance(response, dict) else {"result": response},
            )

        except Exception as exc:
            return CommandResult(
                command=name,
                status="failed",
                response={"error": str(exc)},
            )

    def categories(self):
        return sorted({record.category for record in self.commands.values()})

    def health(self):
        return {
            "status": "online",
            "commands": len(self.commands),
            "categories": self.categories(),
            "command_names": sorted(self.commands.keys()),
        }
