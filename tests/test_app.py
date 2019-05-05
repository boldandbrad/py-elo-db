from py_elo_db import app

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
