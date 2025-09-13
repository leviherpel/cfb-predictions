from __future__ import print_function

import csv
import os
from pprint import pprint

import cfbd
from cfbd.models.division_classification import DivisionClassification
from cfbd.models.game import Game
from cfbd.models.season_type import SeasonType
from cfbd.rest import ApiException

from CsvHeaders import CSV_HEADERS
import ExtractFeatures

configuration = cfbd.Configuration(
    access_token = os.environ["CFBD_KEY"]
)

yearToParse = input("Enter the year to process (e.g., 2025): ")
try:
    process_year = int(yearToParse)
except ValueError:
    print("Invalid year entered. Defaulting to 2025.")
    year = 2025

fileName = f"cfb-{process_year}-season.csv"

with cfbd.ApiClient(configuration) as api_client:
    games_api = cfbd.GamesApi(api_client)
    betting_api = cfbd.BettingApi(api_client)
    stats_api = cfbd.StatsApi(api_client)

    with open(fileName, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)
        
        print(f"Processing year: {process_year}")
        
        games = games_api.get_games(year=process_year)
        print(f"Games for {process_year}:")
        pprint(games)
        
        for game in games:
            try:
                print("Compiling game: ", game.id, " - ", game.home_team, " vs. ", game.away_team)

                # Get the game lines and advanced stats
                game_line = betting_api.get_lines(game_id=game.id)

                # advanced stats for home
                home_game_stats = stats_api.get_advanced_game_stats(
                    year=process_year, week=game.week, team=game.home_team,
                    opponent=game.away_team, exclude_garbage_time=True
                )
                home_offensive_stats = home_game_stats[0].offense if home_game_stats else None
                home_defensive_stats = home_game_stats[0].defense if home_game_stats else None

                # advanced stats for away
                away_game_stats = stats_api.get_advanced_game_stats(
                    year=process_year, week=game.week, team=game.away_team,
                    opponent=game.home_team, exclude_garbage_time=True
                )
                away_offensive_stats = away_game_stats[0].offense if away_game_stats else None
                away_defensive_stats = away_game_stats[0].defense if away_game_stats else None

                flattenStats = ExtractFeatures.extract_game_features({
                    "game": game.to_dict() if hasattr(game, "to_dict") else str(game),
                    "lines": [line.to_dict() if hasattr(line, "to_dict") else str(line) for line in game_line[0].lines],
                    "home_offensive_stats": home_offensive_stats.to_dict() if hasattr(home_offensive_stats, "to_dict") else str(home_offensive_stats),
                    "home_defensive_stats": home_defensive_stats.to_dict() if hasattr(home_defensive_stats, "to_dict") else str(home_defensive_stats),
                    "away_offensive_stats": away_offensive_stats.to_dict() if hasattr(away_offensive_stats, "to_dict") else str(away_offensive_stats),
                    "away_defensive_stats": away_defensive_stats.to_dict() if hasattr(away_defensive_stats, "to_dict") else str(away_defensive_stats),
                })

                writer.writerow(flattenStats)

            except Exception as e:
                print(f"Exception when processing game {game}: {e}")