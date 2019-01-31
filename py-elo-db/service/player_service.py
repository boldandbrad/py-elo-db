from typing import Any, Tuple

from model.player import Player


def get_all_ordered() -> Any:
    """Retrieve all players ordered by rank field."""
    return Player.select().order_by(-Player.rank)


def get_by_id(id: int) -> Player:
    """Retrieve a player by its id field."""
    return Player.select().where(Player.id == id).get()


def get_by_name(name: str) -> Player:
    """Retrieve a player by its name field."""
    return Player.select().where(Player.name == name).get()


def get_or_create_by_name(name: str) -> Player:
    """Retrieve a player by its name field, create if does not exist."""
    player, created = Player.get_or_create(name=name)
    if (created):
        print('Created player', player.name)
    else:
        print('Retrieved player', player.name, player.elo)
    return player


def save(player: Player):
    """Persist new player to database."""
    player.save()
