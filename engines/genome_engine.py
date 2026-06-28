from datetime import datetime


class GenomeEvent:
    """
    Asset Genome™ Event

    Represents one point in the lifecycle of an asset.
    """

    def __init__(
        self,
        event_type: str,
        description: str,
        value=None,
        metadata=None
    ):

        self.timestamp = datetime.utcnow()

        self.event_type = event_type

        self.description = description

        self.value = value

        self.metadata = metadata or {}

    def to_dict(self):

        return {

            "timestamp": self.timestamp.isoformat(),

            "event_type": self.event_type,

            "description": self.description,

            "value": self.value,

            "metadata": self.metadata

        }


class GenomeEngine:
    """
    Asset Genome™

    Living history of every collectible.

    DNA never changes.

    Genome evolves forever.
    """

    def __init__(self):

        self.events = []

    def add_event(
        self,
        event_type,
        description,
        value=None,
        metadata=None
    ):

        event = GenomeEvent(

            event_type,

            description,

            value,

            metadata

        )

        self.events.append(event)

        return event

    def purchase(self, asset):

        return self.add_event(

            "PURCHASE",

            "Asset acquired.",

            asset.purchase_price

        )

    def thorx_update(self, score):

        return self.add_event(

            "THORX",

            "THORᵡ score updated.",

            score

        )

    def valuation_update(self, value):

        return self.add_event(

            "VALUATION",

            "Market valuation changed.",

            value

        )

    def strike_zone(self):

        return self.add_event(

            "STRIKE_ZONE",

            "Entered Strike Zone™"

        )

    def grade_submission(self, company):

        return self.add_event(

            "GRADE_SUBMISSION",

            f"Submitted to {company}"

        )

    def grade_returned(
        self,
        company,
        grade
    ):

        return self.add_event(

            "GRADE_RETURN",

            f"{company} returned grade {grade}",

            grade

        )

    def sold(self, amount):

        return self.add_event(

            "SALE",

            "Asset sold.",

            amount

        )

    def founder_note(self, note):

        return self.add_event(

            "FOUNDER",

            note

        )

    def recommendation(self, action):

        return self.add_event(

            "DEX",

            f"Recommendation: {action}"

        )

    def history(self):

        return [

            event.to_dict()

            for event in self.events

        ]