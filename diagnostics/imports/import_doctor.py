import ast
from pathlib import Path

ROOT = Path(".")

missing = {}

for py in ROOT.rglob("*.py"):

    try:
        tree = ast.parse(py.read_text())

    except Exception:
        continue

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for n in node.names:

                module = n.name.split(".")[0]

                missing.setdefault(module, []).append(py)

        elif isinstance(node, ast.ImportFrom):

            if node.module:

                module = node.module.split(".")[0]

                missing.setdefault(module, []).append(py)

print()

print("Imported Packages")

print("="*50)

for mod in sorted(missing):

    print(mod)
