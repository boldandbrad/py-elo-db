from typing import Any

from model.match import Match


# Retrieves all matches ordered by number
def get_all_ordered() -> Any:
    return Match.select().order_by(+Match.number)


# Retrieves all matches by player_id
def get_all_by_player(player_id: int) -> Any:
    return Match.select().where(Match.home_player_id == player_id |
                                Match.away_player_id == player_id)


# Retrieves a match by unique id
def get_by_id(id: int) -> Any:
    return Match.select().where(Match.id == id).get()


# Retrieves a match by unique number
def get_by_number(number: int) -> Any:
    return Match.select().where(Match.number == number).get()


# Persists match
def save(match: Match) -> Match:
    match.save()
    return match
