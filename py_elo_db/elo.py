#!/usr/bin/env python3

import click

import app
from service import match_service, player_service
from util import db_util, out_util


@click.group()
@click.version_option(1.0)
def cli():
    pass


@cli.group(help='log and manage matches for the active league')
@click.pass_context
def matches(ctx):
    pass


@matches.command('log', help='log a new match')
@click.argument('outcome', type=(str, int, int, str))
@click.option('--sudden-death', '-sd', is_flag=True)
@click.pass_obj
def matches_log(ctx, outcome, sudden_death):
    app.record_match(outcome[0], outcome[3], outcome[1], outcome[2], sudden_death)


@matches.command('list')
@click.option('--all', '-a', default=True)
@click.pass_obj
def matches_list(ctx, all):
    match_list = match_service.get_all_ordered()
    out_util.print_matches(match_list)


@matches.command('file')
@click.argument('path', type=click.Path(exists=True))
@click.pass_obj
def matches_file(ctx, path):
    app.record_match_file(path)


@cli.group()
@click.pass_context
def leagues(ctx):
    pass


@leagues.command('create')
@click.argument('name', type=str)
@click.pass_obj
def leagues_create(ctx):
    pass


@leagues.command('list')
def leagues_list(ctx):
    pass


@leagues.command('load')
@click.argument('name', type=str)
@click.pass_obj
def leagues_create(ctx):
    pass


@cli.group()
@click.pass_context
def stats(ctx):
    pass


@stats.command('elos')
@click.option('--all', '-a', default=True)
@click.pass_obj
def stats_elos(ctx, all):
    player_list = player_service.get_all_ordered()
    out_util.print_ratings(player_list)


@stats.command('standings')
@click.option('--all', '-a', default=True)
@click.pass_obj
def stats_standings(ctx, all):
    player_list = player_service.get_all_ordered()
    out_util.print_stats(player_list)


@cli.group()
@click.pass_context
def configs(ctx):
    pass


@cli.group()
@click.pass_context
def players(ctx):
    pass


if __name__ == '__main__':
    cli()
