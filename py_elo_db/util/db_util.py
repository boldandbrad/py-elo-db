from py_elo_db.model.base import db
from py_elo_db.model.match import Match
from py_elo_db.model.player import Player


def create_tables() -> None:
    """Initialize database tables."""
    with db:
        db.create_tables([Player, Match])
