import getopt
import math
import os
import sys
from typing import Any, Tuple

from model.base import db
from model.match import Match
from model.player import Player
from service import match_service, player_service
from util import db_util, out_util

__license__ = "MIT"
__version__ = 1.0

PRECISION = 1
K_FACTOR = 20


def probability(home_elo: float, away_elo: float) -> Tuple[float, float]:
    """Calculate probability that either player will win."""
    home_prob = 1.0 / (1 + 1.0 * math.pow(10, 1.0 *
                                          (away_elo - home_elo) / 400))
    return home_prob, 1.0 - home_prob


def score_weight(home_score: int, away_score: int) -> float:
    """Calculate score difference weight to be applied."""
    score_diff = abs(home_score - away_score)

    if (score_diff == 0 or score_diff == 1):
        return 1
    elif (score_diff == 2):
        return 1.25
    else:
        return (11 + score_diff) / 10


def calculate_elo(elo: float, prob: float, diff: float,
                  outcome: float) -> float:
    """Calculate a player's new elo rating."""
    return round(elo + ((K_FACTOR * diff) * (outcome - prob)), PRECISION)


def update_elos(home_elo: float, away_elo: float, home_score: int,
                away_score: int) -> Tuple[float, float, float]:
    """Update both player's elo ratings from match outcome."""
    orig_home_elo = home_elo

    home_prob, away_prob = probability(home_elo, away_elo)
    diff = score_weight(home_score, away_score)

    # home won
    if (home_score > away_score):
        home_elo = calculate_elo(home_elo, home_prob, diff, 1)
        away_elo = calculate_elo(away_elo, away_prob, diff, 0)
    # away won
    elif (home_score < away_score):
        home_elo = calculate_elo(home_elo, home_prob, diff, 0)
        away_elo = calculate_elo(away_elo, away_prob, diff, 1)
    # draw
    else:
        home_elo = calculate_elo(home_elo, home_prob, diff, 0.5)
        away_elo = calculate_elo(away_elo, away_prob, diff, 0.5)

    return home_elo, away_elo, abs(orig_home_elo - home_elo)


def update_stats(home_player: Player, away_player: Player,
                 home_score: int, away_score: int) -> None:
    """Update both player's statistics from match outcome."""
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


def recalculate() -> None:
    """Recalculate all stats and elos from beginning or specific match."""
    NotImplemented


def record_match(home_name: str, away_name: str, home_score: int,
                 away_score: int, sudden_death: bool=False) -> None:
    """Record new match in database and update players."""
    out_util.print_recording_match()

    home_player = player_service.get_or_create_by_name(home_name)
    away_player = player_service.get_or_create_by_name(away_name)

    home_player.elo, away_player.elo, rating_change = update_elos(
                                                            home_player.elo,
                                                            away_player.elo,
                                                            home_score,
                                                            away_score
                                                        )

    update_stats(home_player, away_player, home_score, away_score)

    player_service.save(home_player)
    out_util.print_player_update(home_player)

    player_service.save(away_player)
    out_util.print_player_update(away_player)

    match = Match(
        home_player=home_player.id,
        away_player=away_player.id,
        home_score=home_score,
        away_score=away_score,
        sudden_death=sudden_death,
        rating_change=rating_change
    )

    match_service.save(match)
    out_util.print_match_recorded(match)


def record_match_file(filename: str) -> None:
    """Records new matches from a match file."""
    with open(filename, 'r') as f:
        for line in f:
            words = line.split()
            if len(words) == 5 and words[4] == 'SD':
                record_match(words[0], words[3], int(words[1]), int(words[2]),
                             True)
            else:
                record_match(words[0], words[3], int(words[1]), int(words[2]))


def main(argv) -> None:
    """Handles arguments and script execution."""
    try:
        opts, args = getopt.getopt(argv, "hvm:f:", ["help",
                                                    "version",
                                                    "match=",
                                                    "file=",
                                                    "stats",
                                                    "matches",
                                                    "ratings"])
    except getopt.GetoptError:
        out_util.print_help()
        sys.exit(2)

    # Initialize database
    db.connect()
    db_util.create_tables()

    # Handle arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            out_util.print_help()
            sys.exit()
        elif opt in ("-m", "--match"):
            match = str.split(arg)
            if len(match) is 4 and match[1].isdigit() and match[2].isdigit():
                record_match(match[0], match[3], int(match[1]), int(match[2]))
            elif (len(match) is 5 and match[1].isdigit() and
                    match[2].isdigit() and match[4].lower() == 'sd'):
                record_match(match[0], match[3], int(match[1]), int(match[2]),
                             True)
            else:
                out_util.print_help()
                sys.exit()
        elif opt in ("-f", "--file"):
            if (os.path.isfile(arg)):
                record_match_file(arg)
            else:
                out_util.print_no_file(arg)
                sys.exit()
        elif opt in ("--stats"):
            players = player_service.get_all_ordered()
            out_util.print_stats(players)
        elif opt in ("--ratings"):
            players = player_service.get_all_ordered()
            out_util.print_ratings(players)
        elif opt in ("--matches"):
            matches = match_service.get_all_ordered()
            out_util.print_matches(matches)
        elif opt in ("-v", "--version"):
            print('py-elo-db v' + str(__version__))

    # Close database connection and exit
    db.close()
    sys.exit()


if (__name__ == '__main__'):
    main(sys.argv[1:])
