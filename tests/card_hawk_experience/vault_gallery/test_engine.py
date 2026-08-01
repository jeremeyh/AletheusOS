from aletheus.card_hawk_experience.vault_gallery.engine import Engine


def test_x():
    e = Engine()
    assert e.vault().surface_id == "vault" and e.gallery().surface_id == "gallery"
