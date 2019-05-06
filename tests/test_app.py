from py_elo_db import app
from py_elo_db.model.player import Player

def test_win_probability():
    prob1, prob2 = app.win_probability(1000.0, 1000.0)
    assert prob1 == 0.5
    assert prob2 == 0.5

def test_score_weight():
    weight1 = app.score_weight(1, 1)
    assert weight1 == 1

    weight2 = app.score_weight(3, 1)
    assert weight2 == 1.25

    weight3 = app.score_weight(5, 1)
    assert weight3 == 1.5

def test_calculate_elo():
    elo = app.calculate_elo(1000.0, 0.5, 1, 0.5)
    assert elo == 1000.0

def test_update_elos():
    elo1, elo2, change = app.update_elos(1000.0, 1000.0, 1, 1)
    assert elo1 == 1000.0
    assert elo2 == 1000.0
    assert change == 0.0

def test_update_stats():
    player1 = Player(name='p1')
    player2 = Player(name='p2')
    app.update_stats(player1, player2, 3, 1)

    assert player1.wins == 1
    assert player1.losses == 0
    assert player1.draws == 0
    assert player1.goals_for == 3
    assert player1.goals_against == 1
    assert player1.elo > 1000.0 

    assert player2.wins == 0
    assert player2.losses == 1
    assert player2.draws == 0
    assert player2.goals_for == 1
    assert player2.goals_against == 3
    assert player2.elo < 1000.0

def test_recalculate():
    pass

def test_record_match():
    pass

def test_record_match_file():
    pass
