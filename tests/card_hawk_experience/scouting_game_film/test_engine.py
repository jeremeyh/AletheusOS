from aletheus.card_hawk_experience.scouting_game_film.engine import Engine


def test_x():
    e = Engine()
    assert (
        e.scouting_report().surface_id == "scouting_report"
        and e.game_film().surface_id == "game_film"
    )
