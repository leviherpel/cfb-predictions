import os
import cfbd
from cfbd.rest import ApiException
import csv

configuration = cfbd.Configuration(
    access_token = os.environ["CFBD_KEY"]
)

api_instance = cfbd.GamesApi(cfbd.ApiClient(configuration))

yearToParse = input("Enter the year to process (e.g., 2025): ")
try:
    process_year = int(yearToParse)
except ValueError:
    print("Invalid year entered. Defaulting to 2025.")
    process_year = 2025

print("Fetching game weather data...")
all_weather = []
try:
    response = api_instance.get_weather(year=process_year)
    for r in response:
        weather = r.to_dict()
        # Only include games with weather data
        if weather:
            all_weather.append(weather)
    print(f"Successfully fetched weather data for {process_year}")

    # Determine all weather-related keys for CSV columns
    weather_keys = set()
    for game in all_weather:
        for k in game.keys():
            weather_keys.add(k)
    # Ensure game_id is first column
    fieldnames = ["game_id"] + sorted([k for k in weather_keys if k != "game_id"])

    with open(f"game_weather_{process_year}.csv", "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for game in all_weather:
            writer.writerow(game)
    print(f"CSV file 'game_weather_{process_year}.csv' written successfully.")
except ApiException as e:
    print(f"Error fetching weather data for {process_year}: {e}")