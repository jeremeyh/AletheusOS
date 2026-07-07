import ast
from pathlib import Path


CORE = Path("aletheus/runtime/core.py")


def main():
    text = CORE.read_text()
    tree = ast.parse(text)

    boot_function = None

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "boot":
            boot_function = node
            break

    if boot_function is None:
        raise SystemExit("boot() not found")

    boot_lines = boot_function.end_lineno - boot_function.lineno + 1

    print("========================================================")
    print("ALETHEUSOS RUNTIME COMPOSITION ROOT CHECKPOINT")
    print("========================================================")
    print()
    print(f"Core Path.......................{CORE}")
    print(f"Core Lines......................{len(text.splitlines())}")
    print(f"boot() Line.....................{boot_function.lineno}")
    print(f"boot() Lines....................{boot_lines}")
    print()
    print("Status..........................READY FOR COMPOSITION ROOT")
    print("========================================================")


if __name__ == "__main__":
    main()
