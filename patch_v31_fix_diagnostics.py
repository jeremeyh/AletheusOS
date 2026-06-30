from pathlib import Path

p = Path("aletheus/runtime/diagnostics.py")
text = p.read_text()

entry = '("plugins_v3", "Aletheus Plugin Manager"),'

if entry in text:
    print("Plugin diagnostics already present.")
    raise SystemExit(0)

anchor = '("distributed_v3", "Aletheus Distributed Runtime Fabric"),'

if anchor not in text:
    raise SystemExit("Distributed Runtime entry not found.")

text = text.replace(
    anchor,
    anchor + "\n            " + entry,
    1,
)

p.write_text(text)

print("✔ Plugin Manager added to diagnostics.")
