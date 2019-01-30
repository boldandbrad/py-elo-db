from typing import Any, Tuple

from model.player import Player


# Retrieves all players ordered by rank
def get_all_ordered() -> Any:
    return Player.select().order_by(-Player.rank)


# Retrieves a player by unique id
def get_by_id(id: int) -> Player:
    return Player.select().where(Player.id == id).get()


# Retrieves a player by unique name
def get_by_name(name: str) -> Player:
    return Player.select().where(Player.name == name).get()


# Retrieves a player by name if exists, creates otherwise
def get_or_create_by_name(name: str) -> Player:
    player, created = Player.get_or_create(name=name)
    if (created):
        print('Created player', player.name)
    else:
        print('Retrieved player', player.name, player.elo)
    return player


# Persists player
def save(player: Player):
    player.save()
