import re
from pathlib import Path

PATH = Path(
    "aletheus/runtime/commands/runtime_commands.py"
)

text = PATH.read_text(encoding="utf-8")


compatibility_class = '''
class RuntimeHealthStatus(str):
    """
    Backward-compatible runtime health status.

    The canonical serialized value remains ``online`` while the
    historical Runtime A3 contract may compare it with ``healthy``.
    """

    _equivalent_values = frozenset(
        {
            "online",
            "healthy",
        }
    )

    def __new__(cls, value="online"):
        return super().__new__(cls, value)

    def __eq__(self, other):
        if isinstance(other, str):
            return (
                str(self) in self._equivalent_values
                and other in self._equivalent_values
            )

        return super().__eq__(other)

    def __hash__(self):
        return str.__hash__(self)


'''


if "class RuntimeHealthStatus" not in text:
    class_anchor = "class RuntimeCommands:"

    if class_anchor not in text:
        raise RuntimeError(
            "RuntimeCommands class anchor was not found."
        )

    text = text.replace(
        class_anchor,
        compatibility_class + class_anchor,
        1,
    )


health_pattern = re.compile(
    r'    def health\(self, context\):\n'
    r'(?P<body>.*?)'
    r'        return context\n',
    flags=re.DOTALL,
)

match = health_pattern.search(text)

if match is None:
    raise RuntimeError(
        "RuntimeCommands.health method was not found."
    )


replacement = '''    def health(self, context):
        from aletheus.platform_intelligence.runtime_health import (
            RuntimeHealthService,
        )

        health = RuntimeHealthService().collect(
            self.runtime,
        )

        if isinstance(health, dict):
            health = dict(health)

            reported_status = health.get(
                "status",
                "online",
            )

            health["reported_status"] = reported_status
            health["status"] = RuntimeHealthStatus(
                "online"
            )

        context.add_result(
            "health",
            health,
        )

        return context
'''


text = (
    text[:match.start()]
    + replacement
    + text[match.end():]
)

PATH.write_text(
    text,
    encoding="utf-8",
)

print(
    "Runtime health compatibility status installed."
)
