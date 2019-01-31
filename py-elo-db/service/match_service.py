from typing import Any

from model.match import Match


def get_all_ordered() -> Any:
    """Retrieve all matches ordered by number field."""
    return Match.select().order_by(+Match.number)


def get_all_by_player(player_id: int) -> Any:
    """Retrieve all of a player's matches by player id field."""
    return Match.select().where(Match.home_player_id == player_id |
                                Match.away_player_id == player_id)


def get_by_id(id: int) -> Match:
    """Retrieve a match by its id field."""
    return Match.select().where(Match.id == id).get()


def get_by_number(number: int) -> Match:
    """Retrieve a match by its number field."""
    return Match.select().where(Match.number == number).get()


def save(match: Match) -> Match:
    """Persist new match to database."""
    match.save()
