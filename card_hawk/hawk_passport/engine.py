"""In-memory Hawk Passport trust foundation for the CardHawk prototype."""

from dataclasses import asdict, dataclass, field

from .authenticity import validate_authenticity_state
from .identity import Identity
from .ownership import OwnershipEvent
from .provenance import ProvenanceEvent
from .trust_score import calculate_trust_score


@dataclass
class Passport:
    identity: Identity
    owner: str
    authenticity: str = "unverified"
    provenance: list[ProvenanceEvent] = field(default_factory=list)
    ownership: list[OwnershipEvent] = field(default_factory=list)

    def snapshot(self) -> dict:
        score = calculate_trust_score(
            has_identity=bool(self.identity.label),
            has_owner=bool(self.owner),
            authenticity=self.authenticity,
            provenance_count=len(self.provenance),
            transfer_count=len(self.ownership),
        )
        return {
            "asset_id": self.identity.asset_id,
            "label": self.identity.label,
            "owner": self.owner,
            "authenticity": self.authenticity,
            "provenance": [asdict(event) for event in self.provenance],
            "ownership": [asdict(event) for event in self.ownership],
            "trust_score": score,
            "capability_state": "prototype",
        }


class HawkPassportEngine:
    def __init__(self):
        self._passports: dict[str, Passport] = {}

    def initialize(self):
        return {"status": "hawk_passport_ready", "capability_state": "prototype"}

    def issue(self, asset_id: str, label: str, owner: str) -> dict:
        if asset_id in self._passports:
            raise ValueError(f"passport already exists: {asset_id}")
        passport = Passport(identity=Identity(asset_id, label), owner=owner)
        self._passports[asset_id] = passport
        return passport.snapshot()

    def add_provenance(
        self, asset_id: str, kind: str, source: str, note: str = ""
    ) -> dict:
        passport = self._get(asset_id)
        passport.provenance.append(ProvenanceEvent(kind, source, note))
        return passport.snapshot()

    def set_authenticity(self, asset_id: str, state: str) -> dict:
        passport = self._get(asset_id)
        passport.authenticity = validate_authenticity_state(state)
        return passport.snapshot()

    def transfer(self, asset_id: str, owner: str, source: str = "manual") -> dict:
        passport = self._get(asset_id)
        event = OwnershipEvent(owner, source)
        passport.owner = event.owner
        passport.ownership.append(event)
        return passport.snapshot()

    def get(self, asset_id: str) -> dict:
        return self._get(asset_id).snapshot()

    def _get(self, asset_id: str) -> Passport:
        try:
            return self._passports[asset_id]
        except KeyError as exc:
            raise KeyError(f"passport not found: {asset_id}") from exc
