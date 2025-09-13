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
    process_year = 2025

weekToParse = input("Enter the week to process (e.g., 2): ")
try:
    process_week = int(weekToParse)
except ValueError:
    print("Invalid week entered. Defaulting to 1.")
    process_week = 1

fileName = f"cfb-{process_year}-week{process_week}-predictions.csv"

with cfbd.ApiClient(configuration) as api_client:
    games_api = cfbd.GamesApi(api_client)
    betting_api = cfbd.BettingApi(api_client)

    with open(fileName, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)
        
        print(f"Processing year: {process_year}, week: {process_week}")
        
        games = games_api.get_games(year=process_year)
        print(f"Games for {process_year}:")
        pprint(games)
        
        # Filter for games in the selected week that have not been played
        selected_games = [game for game in games if game.week == process_week and not game.completed]
        
        def zero_stats():
            return {
                "passingPlays": {"explosiveness": 0, "successRate": 0, "totalPPA": 0, "ppa": 0},
                "rushingPlays": {"explosiveness": 0, "successRate": 0, "totalPPA": 0, "ppa": 0},
                "passingDowns": {"explosiveness": 0, "successRate": 0, "ppa": 0},
                "standardDowns": {"explosiveness": 0, "successRate": 0, "ppa": 0},
                "openFieldYardsTotal": 0,
                "openFieldYards": 0,
                "secondLevelYardsTotal": 0,
                "secondLevelYards": 0,
                "lineYardsTotal": 0,
                "lineYards": 0,
                "stuffRate": 0,
                "powerSuccess": 0,
                "explosiveness": 0,
                "successRate": 0,
                "totalPPA": 0,
                "ppa": 0,
                "drives": 0,
                "plays": 0
            }

        for game in selected_games:
            try:
                print("Compiling game: ", game.id, " - ", game.home_team, " vs. ", game.away_team)

                # Get the game lines
                game_line = betting_api.get_lines(game_id=game.id)

                flattenStats = ExtractFeatures.extract_game_features({
                    "game": game.to_dict() if hasattr(game, "to_dict") else str(game),
                    "lines": [line.to_dict() if hasattr(line, "to_dict") else str(line) for line in game_line[0].lines] if game_line else [],
                    "home_offensive_stats": zero_stats(),
                    "home_defensive_stats": zero_stats(),
                    "away_offensive_stats": zero_stats(),
                    "away_defensive_stats": zero_stats(),
                })

                writer.writerow(flattenStats)

            except Exception as e:
                print(f"Exception when processing game {game}: {e}")