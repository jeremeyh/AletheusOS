from pathlib import Path

path = Path("aletheus/persistence_v3/persistence_core.py")
text = path.read_text()

text = text.replace(
    """    def bootstrap(self):
        self.base_path.mkdir(parents=True, exist_ok=True)

        for name in [
            "runtime",
            "plugins",
            "applications",
            "agents",
            "workflows",
            "plans",
            "cluster",
            "metrics",
            "events",
        ]:
            path = self.base_path / f"{name}.json"
            if not path.exists():
                path.write_text(json.dumps({}, indent=2))

        return self.statistics()
""",
    """    def bootstrap(self):
        self.base_path.mkdir(parents=True, exist_ok=True)

        for name in [
            "runtime",
            "plugins",
            "applications",
            "agents",
            "workflows",
            "plans",
            "cluster",
            "metrics",
            "events",
        ]:
            path = self.base_path / f"{name}.json"
            if not path.exists():
                path.write_text(json.dumps({}, indent=2))

        return self._statistics_no_bootstrap()
""",
)

text = text.replace(
    """    def statistics(self):
        self.bootstrap()

        json_files = list(self.base_path.glob("*.json"))
        snapshot_dirs = list((self.base_path / "snapshots").glob("*")) if (self.base_path / "snapshots").exists() else []

        size = sum(file.stat().st_size for file in json_files if file.is_file())

        return {
            "version": self.VERSION,
            "path": str(self.base_path),
            "files": len(json_files),
            "snapshots": len(snapshot_dirs),
            "last_save": self.last_save,
            "last_load": self.last_load,
            "size_bytes": size,
            "health": "healthy",
        }
""",
    """    def statistics(self):
        self.base_path.mkdir(parents=True, exist_ok=True)
        return self._statistics_no_bootstrap()

    def _statistics_no_bootstrap(self):
        json_files = list(self.base_path.glob("*.json"))
        snapshot_dirs = list((self.base_path / "snapshots").glob("*")) if (self.base_path / "snapshots").exists() else []

        size = sum(file.stat().st_size for file in json_files if file.is_file())

        return {
            "version": self.VERSION,
            "path": str(self.base_path),
            "files": len(json_files),
            "snapshots": len(snapshot_dirs),
            "last_save": self.last_save,
            "last_load": self.last_load,
            "size_bytes": size,
            "health": "healthy",
        }
""",
)

path.write_text(text)
print("✔ Fixed v3.2 Persistence recursion.")
