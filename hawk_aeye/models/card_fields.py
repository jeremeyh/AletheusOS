from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CardFields:
    """
    Canonical CardHawk Asset DNA™

    Every engine in CardHawk OS should consume this model.
    """

    #
    # Identity
    #

    player: str = ""
    year: int = 0
    sport: str = ""
    team: str = ""

    #
    # Card Information
    #

    brand: str = ""
    manufacturer: str = ""
    set: str = ""
    subset: str = ""
    card_number: str = ""
    parallel: str = ""

    #
    # Collectibility
    #

    serial: str = ""
    autograph: bool = False
    patch: bool = False
    rookie: bool = False
    first_bowman: bool = False
    one_of_one: bool = False
    case_hit: bool = False
    ssp: bool = False

    #
    # Grading
    #

    grade_company: str = ""
    grade: str = ""
    condition: str = "Raw"

    #
    # Marketplace

    purchase_price: float = 0.0
    market_value: float = 0.0

    #
    # Intelligence

    thorx_score: float = 0.0
    founder_rating: str = ""

    #
    # Metadata

    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self):

        return self.__dict__
