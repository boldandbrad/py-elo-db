import math

from peewee import *

from model.base import db
from model.match import Match
from model.player import Player
from service import match_service
from service import player_service
from typing import Any, Tuple
from util import db_util

PRECISION = 1
K_FACTOR = 30


# Calculate probability
def probability(elo_a: float, elo_b: float) -> Tuple[float, float]:
    prob_a = 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (elo_b - elo_a) / 400))
    return prob_a, 1.0 - prob_a


# Calculate score difference weight
def score_weight(score_a: int, score_b: int) -> float:
    score_diff = abs(score_a - score_b)

    if (score_diff == 0 or score_diff == 1):
        return 1
    elif (score_diff == 2):
        return 1.25
    else:
        return (11 + score_diff) / 10


# Calculate updated elo rating
def calculate_elo(elo: float, prob: float, diff: float,
                  outcome: float) -> float:
    return round(elo + ((K_FACTOR * diff) * (outcome - prob)), PRECISION)


# Update Elo Ratings
def update_elos(elo_a: float, elo_b: float, score_a: int,
                score_b: int) -> Any:

    orig_elo_a = elo_a

    prob_a, prob_b = probability(elo_a, elo_b)

    diff = score_weight(score_a, score_b)

    # player a won
    if (score_a > score_b):
        elo_a = calculate_elo(elo_a, prob_a, diff, 1)
        elo_b = calculate_elo(elo_b, prob_b, diff, 0)
    # player b won
    elif (score_a < score_b):
        elo_a = calculate_elo(elo_a, prob_a, diff, 0)
        elo_b = calculate_elo(elo_b, prob_b, diff, 1)
    # draw
    else:
        elo_a = calculate_elo(elo_a, prob_a, diff, 0.5)
        elo_b = calculate_elo(elo_b, prob_b, diff, 0.5)

    return elo_a, elo_b, abs(orig_elo_a - elo_a)


# Update Traditional Stats
def update_stats(home_player: Player, away_player: Player,
                 home_score: int, away_score: int) -> None:

    home_player.goals_for += home_score
    home_player.goals_against += away_score
    away_player.goals_for += away_score
    away_player.goals_against += home_score

    # home won
    if (home_score > away_score):
        home_player.wins += 1
        away_player.losses += 1
    # away won
    elif (home_score < away_score):
        home_player.losses += 1
        away_player.wins += 1
    # draw
    else:
        home_player.draws += 1
        away_player.draws += 1


# Recalculates all elo's from beginning or specific match
def recalculate():
    NotImplemented


# Adds new match to database and updates Elos
def record_match(home_name: str, away_name: str, home_score: int,
                 away_score: int, ot: bool=False) -> None:

    home_player = player_service.get_or_create_by_name(home_name)

    away_player = player_service.get_or_create_by_name(away_name)

    home_player.elo, away_player.elo, rating_change = update_elos(
                                                            home_player.elo,
                                                            away_player.elo,
                                                            home_score,
                                                            away_score
                                                        )

    update_stats(home_player, away_player,
                 home_score, away_score)

    player_service.save(home_player)
    player_service.save(away_player)

    match = Match(
        home_player=home_player.id,
        away_player=away_player.id,
        home_score=home_score,
        away_score=away_score,
        ot=ot,
        rating_change=rating_change
    )

    match_service.save(match)


def main():
    print('start')

    db.connect()
    db_util.create_tables()

    record_match('name1', 'name2', 4, 2)

    db.close()
    
    print('end')


if (__name__ == '__main__'):
    main()