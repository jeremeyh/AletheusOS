from dataclasses import dataclass


@dataclass
class AssetDNA:
    """
    Asset DNA™

    Immutable or slow-changing identity facts that define what an asset is.
    """

    player: str = ""
    team: str = ""
    sport: str = ""
    league: str = ""
    year: int = 0
    brand: str = ""
    set_name: str = ""
    subset: str = ""
    card_number: str = ""
    parallel: str = ""
    variation: str = ""
    serial_number: str = ""
    print_run: int | None = None
    rookie: bool = False
    first_bowman: bool = False
    autograph: bool = False
    auto_type: str = ""
    patch: bool = False
    memorabilia: bool = False
    one_of_one: bool = False
    case_hit: bool = False
    ssp: bool = False

    def summary(self) -> str:
        parts = [
            str(self.year) if self.year else "",
            self.brand,
            self.set_name,
            self.parallel,
            self.serial_number,
        ]
        return " • ".join([p for p in parts if p])
