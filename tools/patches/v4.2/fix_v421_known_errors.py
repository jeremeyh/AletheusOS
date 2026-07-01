from pathlib import Path
import re

# 1. Make VERSION match runtime
Path("VERSION").write_text("4.2.1\n")

core = Path("aletheus/runtime/core.py")
text = core.read_text()
text = re.sub(
    r'self\.version\s*=\s*"[^"]+"',
    'self.version = "4.2.1"',
    text,
    count=1,
)
core.write_text(text)

# 2. Fix stale foundation test message
foundation = Path("tests/test_aletheus_v411_foundation.py")
if foundation.exists():
    ft = foundation.read_text()
    ft = ft.replace(
        "✔ AletheusOS v4.1.1 Engineering Foundation tests passed.",
        "✔ AletheusOS Runtime Engineering Foundation tests passed.",
    )
    foundation.write_text(ft)

# 3. Ignore generated runtime reports
gitignore = Path(".gitignore")
existing = gitignore.read_text() if gitignore.exists() else ""
if "reports/" not in existing:
    gitignore.write_text(existing.rstrip() + "\n\n# Generated runtime health reports\nreports/\n")

# 4. Remove committed report artifacts from tracking if present
for report in [
    Path("reports/runtime-health.json"),
    Path("reports/runtime-health.md"),
]:
    if report.exists():
        # leave file locally; git rm --cached happens outside this script
        pass

print("✔ Known v4.2.1 cleanup issues repaired.")
