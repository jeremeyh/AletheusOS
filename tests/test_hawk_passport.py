from card_hawk.hawk_passport import HawkPassportEngine


def test_passport_tracks_provenance_transfer_and_trust():
    engine = HawkPassportEngine()
    issued = engine.issue("asset-1", "1986 Fleer Jordan #57", "owner-a")
    assert issued["capability_state"] == "prototype"
    assert issued["trust_score"] == 40

    engine.add_provenance("asset-1", "purchase", "dealer-1")
    engine.set_authenticity("asset-1", "verified")
    snapshot = engine.transfer("asset-1", "owner-b", "escrow")

    assert snapshot["owner"] == "owner-b"
    assert snapshot["authenticity"] == "verified"
    assert snapshot["provenance"][0]["source"] == "dealer-1"
    assert snapshot["ownership"][0]["source"] == "escrow"
    assert snapshot["trust_score"] == 82


def test_duplicate_and_missing_passports_are_rejected():
    engine = HawkPassportEngine()
    engine.issue("asset-1", "Card", "owner")
    try:
        engine.issue("asset-1", "Card", "owner")
    except ValueError as error:
        assert "already exists" in str(error)
    else:
        raise AssertionError("duplicate passport was accepted")

    try:
        engine.get("missing")
    except KeyError as error:
        assert "not found" in str(error)
    else:
        raise AssertionError("missing passport was accepted")
