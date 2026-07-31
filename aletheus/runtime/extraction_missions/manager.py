from .models import ExtractionMission


class RuntimeExtractionMissionManager:
    """
    Runtime Extraction Mission Manager™

    Tracks production extraction missions from runtime/core.py.
    """

    def __init__(self):
        self.missions = []

    def add(
        self,
        mission_id,
        responsibility,
        destination,
        estimated_lines,
        status="planned",
        notes="",
    ):

        self.missions.append(
            ExtractionMission(
                mission_id=mission_id,
                responsibility=responsibility,
                source="aletheus/runtime/core.py",
                destination=destination,
                estimated_lines=estimated_lines,
                status=status,
                notes=notes,
            )
        )

    def completion(self):

        if not self.missions:
            return 0.0

        complete = len([m for m in self.missions if m.status == "complete"])

        return round(
            complete / len(self.missions) * 100,
            1,
        )

    def health(self):

        return {
            "missions": len(self.missions),
            "completion": self.completion(),
        }
