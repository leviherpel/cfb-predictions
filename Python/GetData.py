from __future__ import print_function
from Constants import csv_headers
from cfbd.rest import ApiException
from pprint import pprint
import cfbd
import csv

# Configure API key authorization: ApiKeyAuth
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = '<Add key here>'
configuration.api_key_prefix['Authorization'] = 'Bearer'

# create an instance of the API class
games_api = cfbd.GamesApi(cfbd.ApiClient(configuration))
stats_api = cfbd.StatsApi(cfbd.ApiClient(configuration))
betting_api = cfbd.BettingApi(cfbd.ApiClient(configuration))

# settings for fetching data
year = 2023
div = "fbs"
fileName="cfb2023-postseason.csv"

try:
    print("Welcome to CfbAlright #FreeMac")

    # Get a list of all games for the specified season
    print("Getting games for year: ", year)
    regular_season_games= games_api.get_games(year=year,division=div)
    post_season_games = games_api.get_games(year=year,division=div,season_type="postseason")
    games = regular_season_games + post_season_games

    # Write object properties to CSV file
    with open(fileName, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Iterate through each game and collect data
        writer.writerow(csv_headers)
        for game in games:
            print("Compiling game: ", game.id, " - ", game.home_team, " vs. ", game.away_team)
            
            game_line = betting_api.get_lines(game_id=game.id)
            #game_stats = stats_api.get_advanced_team_game_stats(year=year, week=game.week, team=game.home_team, opponent=game.away_team, exclude_garbage_time=True)

            # Update the dictionary with properties from GameLine object
            for line in game_line[0].lines:
                
                # Create a dictionary to store the combined row
                combined_row = {}

                # Update the dictionary with properties from objects
                for property in csv_headers:
                    try:
                        combined_row[property] = getattr(game, property)
                    except AttributeError:
                        pass

                    try:
                        combined_row[property] = getattr(line, property)
                    except AttributeError:
                        pass
                        
                # Set the favorite
                if combined_row["formatted_spread"].find(game.home_team) != -1:
                    combined_row["favorite"] = game.home_id
                else:
                    combined_row["favorite"] = game.away_id

                writer.writerow([combined_row.get(attr, '') for attr in csv_headers])


except ApiException as e:
    print("Exception when calling BettingApi->get_lines: %s\n" % e)
    
