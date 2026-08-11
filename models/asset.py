from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Asset:
    """
    CardHawk OS™
    Canonical Asset Record™

    Every collectible inside CardHawk OS™ is represented
    by one Asset object.
    """

    # -------------------------
    # Identity
    # -------------------------

    asset_id: int | None = None

    category: str = ""
    sport: str = ""

    player: str = ""
    team: str = ""

    year: int = 0

    brand: str = ""
    set_name: str = ""
    subset: str = ""

    card_number: str = ""

    # -------------------------
    # Physical
    # -------------------------

    parallel: str = ""

    serial_number: str = ""

    print_run: int | None = None

    autograph: bool = False

    memorabilia: bool = False

    grade_company: str = ""

    grade: str = ""

    condition: str = "Raw"

    # -------------------------
    # Acquisition
    # -------------------------

    purchase_price: float = 0.00

    shipping_cost: float = 0.00

    tax: float = 0.00

    fees: float = 0.00

    purchase_date: str = field(
        default_factory=lambda: datetime.now().strftime("%Y-%m-%d")
    )

    marketplace: str = ""

    seller: str = ""

    # -------------------------
    # Valuation
    # -------------------------

    current_value: float = 0.00

    floor_value: float = 0.00

    ceiling_value: float = 0.00

    nuclear_value: float = 0.00

    # -------------------------
    # Intelligence
    # -------------------------

    thorx_score: float = 0.0

    ni_score: float = 0.0

    q_def: float = 0.0

    d_def: float = 0.0

    strike_zone: bool = False

    opportunity_rank: int = 0

    confidence: float = 0.0

    # -------------------------
    # Media
    # -------------------------

    front_image: str = ""

    back_image: str = ""

    # -------------------------
    # Notes
    # -------------------------

    notes: str = ""

    tags: str = ""

    @property
    def total_cost(self) -> float:
        return self.purchase_price + self.shipping_cost + self.tax + self.fees

    @property
    def gain_loss(self) -> float:
        return self.current_value - self.total_cost

    @property
    def roi_percent(self) -> float:
        if self.total_cost == 0:
            return 0

        return ((self.current_value - self.total_cost) / self.total_cost) * 100
