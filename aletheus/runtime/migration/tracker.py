from .models import MigrationItem, MigrationReport


class RuntimeMigrationTracker:
    """
    Runtime Migration Tracker™

    Tracks migration of responsibilities
    from runtime/core.py into bounded subsystems.
    """

    def __init__(self):
        self.items = []

    def add(
        self,
        name,
        destination,
        status="planned",
        notes=""
    ):
        self.items.append(
            MigrationItem(
                name=name,
                destination=destination,
                status=status,
                notes=notes,
            )
        )

    def report(self):
        return MigrationReport(
            items=self.items,
        )

    def completion(self):
        if not self.items:
            return 0.0

        complete = len(
            [
                item
                for item in self.items
                if item.status == "complete"
            ]
        )

        return round(
            complete / len(self.items) * 100,
            1,
        )
