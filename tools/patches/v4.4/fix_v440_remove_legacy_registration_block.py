from pathlib import Path

core = Path("aletheus/runtime/core.py")

text = core.read_text()

start = text.find("        # v2.5 Cognitive Reasoning Engine")
end = text.find('        self.commands.register("workflow.create"', start)

if start == -1 or end == -1:
    raise SystemExit("Legacy registration block not found.")

end = text.find("\n", end)
text = text[:start] + text[end + 1 :]

core.write_text(text)

print("✔ Removed obsolete v2.5-v2.8 registration block.")
