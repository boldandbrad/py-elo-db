from model.base import db
from model.match import Match
from model.player import Player


def create_tables() -> None:
    """Initialize database tables."""
    with db:
        db.create_tables([Player, Match])
