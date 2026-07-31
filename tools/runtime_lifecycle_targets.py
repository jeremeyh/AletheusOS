import ast
from pathlib import Path

CORE = Path("aletheus/runtime/core.py")

LIFECYCLE_KEYWORDS = [
    "boot",
    "start",
    "stop",
    "shutdown",
    "pulse",
    "health",
    "initialize",
    "ready",
]


def main():
    text = CORE.read_text(errors="ignore")
    tree = ast.parse(text)

    targets = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name.lower()

            if any(keyword in name for keyword in LIFECYCLE_KEYWORDS):
                size = 0

                if hasattr(node, "lineno") and hasattr(node, "end_lineno"):
                    size = node.end_lineno - node.lineno + 1

                targets.append(
                    {
                        "name": node.name,
                        "line": node.lineno,
                        "size": size,
                    }
                )

    targets.sort(key=lambda item: item["line"])

    print("========================================================")
    print("ALETHEUSOS LIFECYCLE EXTRACTION TARGETS")
    print("========================================================")
    print()
    print(f"Core Path.......................{CORE}")
    print(f"Lifecycle Targets...............{len(targets)}")
    print()
    print("Targets")

    for target in targets:
        print(f"  - {target['name']} at line {target['line']} ({target['size']} lines)")

    print()
    print("========================================================")


if __name__ == "__main__":
    main()
