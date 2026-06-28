class SmokeTests:
    """CI / QA smoke tests."""

    @staticmethod
    def run():
        results = {}
        checks = [
            ("asset_model", lambda: __import__("models.asset")),
            ("settings", lambda: __import__("config.settings")),
            ("migration_runner", lambda: __import__("migrations.migration_runner")),
            ("backup_manager", lambda: __import__("backup.backup_manager")),
        ]

        for name, fn in checks:
            try:
                fn()
                results[name] = "pass"
            except Exception as exc:
                results[name] = f"fail: {exc}"

        return results
