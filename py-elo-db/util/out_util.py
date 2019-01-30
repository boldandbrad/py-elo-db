from typing import Any


def print_help():
    print('py-elo-db help:\n')
    print('- Record new match')
    print('\tmain.py -m "<home_name> <home_score>',
          '<away_score> <away_name> OT(optional)"')
    print('- Record new match file')
    print('\tmain.py -f <file_path>')
    print()


def print_no_file(path: str):
    print('file does not exist:', path)


def print_stats(players: Any):
    # TODO: fix lambda issue where player has 0 losses
    player_list = sorted(players,
                         key=lambda player: player.wins / player.losses,
                         reverse=True)

    print()
    print('Player, G, W, L, PCT, GF, GA')
    print('----------------------------')
    for player in player_list:
        games = player.wins + player.losses
        pct = round(player.wins / games, 3)
        print(str(player.name) + ', ' + str(games) + ', ' + str(player.wins) +
              ', ' + str(player.losses) + ', ' + str(pct) + ', ' +
              str(player.goals_for) + ', ' + str(player.goals_against))
    print()


def print_ratings(players: Any):
    player_list = sorted(players, key=lambda player: player.elo, reverse=True)

    print()
    print('Elo Ratings')
    print('-------------------------')
    for player in player_list:
        print(player.name + ' - ' + str(player.elo))

    print()


def print_matches(matches: Any):
    print()
    print('Matches')
    print('-------------------------')
    for match in matches:
        if match.ot:
            print(match.home_player.name,
                  str(match.home_score) + ' - ' + str(match.away_score),
                  match.away_player.name, 'OT')
        else:
            print(match.home_player.name,
                  str(match.home_score) + ' - ' + str(match.away_score),
                  match.away_player.name)

    print()
