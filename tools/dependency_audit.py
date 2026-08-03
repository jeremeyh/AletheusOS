import ast
import importlib.util
from pathlib import Path

ROOT = Path(".")

failures = []


def check_module(pyfile, module):
    try:
        spec = importlib.util.find_spec(module)
        if spec is None:
            failures.append((str(pyfile), module))
    except Exception:
        failures.append((str(pyfile), module))


for py in ROOT.rglob("*.py"):
    try:
        source = py.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(py))
    except Exception:
        continue

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                check_module(py, alias.name)

        elif isinstance(node, ast.ImportFrom) and node.module:
            check_module(py, node.module)

print("=" * 80)
print("MISSING IMPORTS")
print("=" * 80)

for path, module in sorted(set(failures)):
    print(f"{path}: {module}")

print()
print(f"Total: {len(set(failures))}")
