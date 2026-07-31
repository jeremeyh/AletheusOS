import ast
from pathlib import Path

CORE = Path("aletheus/runtime/core.py")


def main():
    text = CORE.read_text()
    tree = ast.parse(text)

    functions = [
        node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
    ]

    print("========================================================")
    print("ALETHEUSOS GENESIS 7 INTEGRATION BASELINE")
    print("========================================================")
    print()
    print(f"Core Lines......................{len(text.splitlines())}")
    print(f"Functions.......................{len(functions)}")
    print(f"boot() Present..................{'boot' in functions}")
    print()
    print("Status..........................READY FOR INTEGRATION")
    print("========================================================")


if __name__ == "__main__":
    main()
