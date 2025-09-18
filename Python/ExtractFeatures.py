import requests
from CsvHeaders import CSV_HEADERS

PROVIDERS = {
    "ESPN Bet": "espn",
    "DraftKings": "draftkings",
    "Bovada": "bovada"
}

def extract_game_features(game_json):
    game = game_json.get("game", {})
    lines = {p: {} for p in PROVIDERS.values()}
    for line in game_json.get("lines", []):
        key = PROVIDERS.get(line.get("provider"))
        if key:
            lines[key] = {
                f"{key}_spread": line.get("spread", ""),
                f"{key}_spread_open": line.get("spreadOpen", ""),
                f"{key}_over_under": line.get("overUnder", ""),
                f"{key}_over_under_open": line.get("overUnderOpen", ""),
                f"{key}_home_moneyline": line.get("homeMoneyline", ""),
                f"{key}_away_moneyline": line.get("awayMoneyline", ""),
            }
    def flatten_stats(prefix, stats):
        stats = stats or {}
        passing = stats.get("passingPlays", {})
        rushing = stats.get("rushingPlays", {})
        passing_downs = stats.get("passingDowns", {})
        standard_downs = stats.get("standardDowns", {})
        return [
            passing.get("explosiveness", ""),
            passing.get("successRate", ""),
            passing.get("totalPPA", ""),
            passing.get("ppa", ""),
            rushing.get("explosiveness", ""),
            rushing.get("successRate", ""),
            rushing.get("totalPPA", ""),
            rushing.get("ppa", ""),
            passing_downs.get("explosiveness", ""),
            passing_downs.get("successRate", ""),
            passing_downs.get("ppa", ""),
            standard_downs.get("explosiveness", ""),
            standard_downs.get("successRate", ""),
            standard_downs.get("ppa", ""),
            stats.get("openFieldYardsTotal", ""),
            stats.get("openFieldYards", ""),
            stats.get("secondLevelYardsTotal", ""),
            stats.get("secondLevelYards", ""),
            stats.get("lineYardsTotal", ""),
            stats.get("lineYards", ""),
            stats.get("stuffRate", ""),
            stats.get("powerSuccess", ""),
            stats.get("explosiveness", ""),
            stats.get("successRate", ""),
            stats.get("totalPPA", ""),
            stats.get("ppa", ""),
            stats.get("drives", ""),
            stats.get("plays", "")
        ]
    row = [
        game.get("id", ""), game.get("season", ""), game.get("week", ""), game.get("seasonType", ""), game.get("startDate", ""), game.get("completed", ""),
        game.get("neutralSite", ""), game.get("conferenceGame", ""), game.get("venueId", ""), game.get("venue", ""), game.get("excitementIndex", ""), game.get("attendance", ""),
        game.get("homeId", ""), game.get("homeTeam", ""), game.get("homeConference", ""), game.get("homeClassification", ""), game.get("homePoints", ""),
        game.get("homePostgameWinProbability", ""), game.get("homePregameElo", ""), game.get("homePostgameElo", ""),
        game.get("awayId", ""), game.get("awayTeam", ""), game.get("awayConference", ""), game.get("awayClassification", ""), game.get("awayPoints", ""),
        game.get("awayPostgameWinProbability", ""), game.get("awayPregameElo", ""), game.get("awayPostgameElo", ""),
        # Betting lines
        lines["espn"].get("espn_spread", "") if "espn" in lines else "", 
        lines["espn"].get("espn_spread_open", "") if "espn" in lines else "",
        lines["espn"].get("espn_over_under", "") if "espn" in lines else "", 
        lines["espn"].get("espn_over_under_open", "") if "espn" in lines else "",
        lines["espn"].get("espn_home_moneyline", "") if "espn" in lines else "", 
        lines["espn"].get("espn_away_moneyline", "") if "espn" in lines else "",
        lines["draftkings"].get("draftkings_spread", "") if "draftkings" in lines else "", 
        lines["draftkings"].get("draftkings_spread_open", "") if "draftkings" in lines else "",
        lines["draftkings"].get("draftkings_over_under", "") if "draftkings" in lines else "", 
        lines["draftkings"].get("draftkings_over_under_open", "") if "draftkings" in lines else "",
        lines["draftkings"].get("draftkings_home_moneyline", "") if "draftkings" in lines else "", 
        lines["draftkings"].get("draftkings_away_moneyline", "") if "draftkings" in lines else "",
        lines["bovada"].get("bovada_spread", "") if "bovada" in lines else "", 
        lines["bovada"].get("bovada_spread_open", "") if "bovada" in lines else "",
        lines["bovada"].get("bovada_over_under", "") if "bovada" in lines else "", 
        lines["bovada"].get("bovada_over_under_open", "") if "bovada" in lines else "",
        lines["bovada"].get("bovada_home_moneyline", "") if "bovada" in lines else "", 
        lines["bovada"].get("bovada_away_moneyline", "") if "bovada" in lines else "",
        # Stats
        *flatten_stats("home_off", game_json.get("home_offensive_stats")),
        *flatten_stats("home_def", game_json.get("home_defensive_stats")),
        *flatten_stats("away_off", game_json.get("away_offensive_stats")),
        *flatten_stats("away_def", game_json.get("away_defensive_stats")),
    ]
    return row

def fetch_and_extract(url):
    resp = requests.get(url)
    data = resp.json()
    return [extract_game_features(game_json) for game_json in data]