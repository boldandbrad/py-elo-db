from py_elo_db import app

def test_win_probability():
    prob1, prob2 = app.win_probability(1000.0, 1000.0)
    assert prob1 == 0.5
    assert prob2 == 0.5
