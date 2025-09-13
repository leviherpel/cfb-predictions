import os
import cfbd
from cfbd.rest import ApiException
import csv

configuration = cfbd.Configuration(
    access_token = os.environ["CFBD_KEY"]
)

api_instance = cfbd.RatingsApi(cfbd.ApiClient(configuration))

yearToParse = input("Enter the year to process (e.g., 2025): ")
try:
    process_year = int(yearToParse)
except ValueError:
    print("Invalid year entered. Defaulting to 2025.")
    process_year = 2025

print("Fetching historical SP+ ratings...")
all_sp_ratings = []
try:
    response = api_instance.get_sp(year=process_year)
    for r in response:
        all_sp_ratings.append(r.to_dict())
    print(f"Successfully fetched SP+ ratings for {process_year}")

    # Write to CSV
    with open(f"sp_ratings_{process_year}.csv", "w", newline='') as csvfile:
        fieldnames = ["year", "team", "sp_rating", "off_sp_rating", "def_sp_rating", "special_sp_rating"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for team in all_sp_ratings:
            writer.writerow({
                "year": team.get("year"),
                "team": team.get("team"),
                "sp_rating": team.get("rating"),
                "off_sp_rating": team.get("offense", {}).get("rating"),
                "def_sp_rating": team.get("defense", {}).get("rating"),
                "special_sp_rating": team.get("specialTeams", {}).get("rating")
            })
    print(f"CSV file 'sp_ratings_{process_year}.csv' written successfully.")
except ApiException as e:
    print(f"Error fetching SP+ ratings for {process_year}: {e}")