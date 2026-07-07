from .models import RegistrationRecord


class RuntimeRegistrationManager:
    """
    Runtime Registration Manager™

    Owns runtime registrations.

    It does not create services.
    It maintains authoritative runtime registrations.
    """

    def __init__(self):
        self.records = {}

    def register(
        self,
        category: str,
        name: str,
        metadata=None,
    ):
        record = RegistrationRecord(
            name=name,
            category=category,
            metadata=metadata or {},
        )

        self.records.setdefault(category, {})
        self.records[category][name] = record

        return record

    def categories(self):
        return sorted(self.records.keys())

    def registrations(self):
        total = 0

        for category in self.records.values():
            total += len(category)

        return total

    def health(self):
        return {
            "categories": self.categories(),
            "registration_count": self.registrations(),
        }
