from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Constitution:
    name: str = "AletheusOS Constitution"
    version: str = "Genesis"
    principle_x: str = "Continuously reduce the gap between reality and understanding through truthful observation, evidence-based reasoning, governed intelligence, responsible action, continuous learning, and stewardship."

    def validate(self):
        if not all((self.name.strip(), self.version.strip(), self.principle_x.strip())):
            raise ValueError("Constitution is incomplete.")
