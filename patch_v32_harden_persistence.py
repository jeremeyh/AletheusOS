from pathlib import Path

path = Path("aletheus/persistence_v3/persistence_core.py")
text = path.read_text()

# Ensure snapshots directory is created during bootstrap
old = '        self.base_path.mkdir(parents=True, exist_ok=True)\n'
new = '''        self.base_path.mkdir(parents=True, exist_ok=True)
        (self.base_path / "snapshots").mkdir(parents=True, exist_ok=True)
'''
text = text.replace(old, new, 1)

# Ensure snapshots directory exists before snapshot()
old = '''    def snapshot(self, name: str = "Runtime Snapshot", runtime=None):
        self.save(runtime)

        snapshot_id = str(uuid.uuid4())
'''
new = '''    def snapshot(self, name: str = "Runtime Snapshot", runtime=None):
        self.save(runtime)

        (self.base_path / "snapshots").mkdir(parents=True, exist_ok=True)

        snapshot_id = str(uuid.uuid4())
'''
text = text.replace(old, new, 1)

path.write_text(text)
print("✔ Hardened Persistence Engine.")
