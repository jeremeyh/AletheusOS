import ast
import importlib.util
from pathlib import Path

ROOT = Path(".")

failures = []

for py in ROOT.rglob("*.py"):
    try:
        source = py.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(py))
    except Exception:
        continue

    for node in ast.walk(tree):
        module = None

        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name
                if importlib.util.find_spec(module) is None:
                    failures.append((str(py), module))

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module = node.module
                if importlib.util.find_spec(module) is None:
                    failures.append((str(py), module))

print("=" * 80)
print("UNRESOLVED IMPORTS")
print("=" * 80)

if not failures:
    print("None")
else:
    for file, module in sorted(set(failures)):
        print(f"{file}")
        print(f"  -> {module}")
