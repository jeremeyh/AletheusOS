from pathlib import Path
import shutil

FILE = Path("aletheus/span/constitutional_context.py")

if not FILE.exists():
    raise SystemExit(f"Missing {FILE}")

backup = FILE.with_suffix(".py.bak_mutable_defaults")
if not backup.exists():
    shutil.copy2(FILE, backup)
    print(f"✓ Backup created: {backup}")

lines = FILE.read_text(encoding="utf-8").splitlines()

start = None
end = None

# Locate the unreachable mutable-default block
for i, line in enumerate(lines):
    if 'elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):' in line:
        start = i
        break

if start is None:
    raise SystemExit("Could not locate unreachable mutable-default block.")

for i in range(start + 1, len(lines)):
    if lines[i].startswith("        for class_name"):
        end = i
        break

if end is None:
    raise SystemExit("Could not locate end of unreachable block.")

# Remove unreachable block
del lines[start:end]

# Locate the first Function/Class handler
insert_after = None
for i, line in enumerate(lines):
    if "elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):" in line:
        insert_after = i
        break

if insert_after is None:
    raise SystemExit("Could not locate Function/Class handler.")

# Find insertion point immediately after missing_public_docstrings.append(...)
append_line = None
for i in range(insert_after, len(lines)):
    if "missing_public_docstrings.append" in lines[i]:
        append_line = i
        break

if append_line is None:
    raise SystemExit("Could not locate docstring append.")

# If append spans multiple lines, move to closing parenthesis
j = append_line
while j < len(lines) and ")" not in lines[j]:
    j += 1

insertion = [
"                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):",
"                    for default in (*node.args.defaults, *node.args.kw_defaults):",
"                        if default is not None and isinstance(default, (ast.List, ast.Dict, ast.Set)):",
"                            context.mutable_default_candidates.append(",
"                                f\"{rel}:{node.lineno}:{node.name}\"",
"                            )",
"",
]

lines[j + 1:j + 1] = insertion

FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("✓ constitutional_context.py updated")
print("✓ Removed unreachable mutable-default block")
print("✓ Added mutable-default detection into reachable FunctionDef branch")
