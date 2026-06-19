import requests
import time

ROUND_URL = "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_round"
HOLE_URL = "https://www.pdga.com/api/v1/feat/live-scores/{score_id}/hole-breakdowns"
STATS_URL = "https://www.pdga.com/api/v1/feat/live-scores/{score_id}/round-stats"


def get_round(event_id, division, round_id):
    return requests.get(
        ROUND_URL,
        params={
            "TournID": event_id,
            "Division": division,
            "Round": round_id,
        },
    ).json()


def get_hole_breakdown(score_id):
    return requests.get(HOLE_URL.format(score_id=score_id)).json()


def get_round_stats(score_id):
    return requests.get(STATS_URL.format(score_id=score_id)).json()

def map_round_info(event_id: int, division: str, round_number: int, data: dict) -> dict:
    layout = data["layouts"][0]

    return {
        "event_id": event_id,
        "division": division,
        "round_number": round_number,
        "pool": data["pool"],
        "course_id": layout["CourseID"],
        "layout_id": layout["LayoutID"],
        "live_round_id": data["live_round_id"],
        "shotgun_time": data["shotgun_time"],
        "tee_times": data["tee_times"],
    }

def map_players(data):
    return [
        {
            "pdga_number": p["PDGANum"],
            "full_name": p["Name"],
            "first_name": p["FirstName"],
            "last_name": p["LastName"],
            "home_city": p["City"],
            "home_state": p["StateProv"],
            "home_country": p["Country"],
            "full_location": p["FullLocation"],
            "nationality": p["Nationality"],
        }
        for p in data["scores"]
    ]

def map_player_round(event_id: int, division: str, round_number: int, data):
    out = []

    for p in data["scores"]:
        out.append({
            "event_id": event_id,
            "division": division,
            "round_number": round_number,

            "result_id": p["ResultID"],
            "round_id": p["RoundID"],
            "score_id": p["ScoreID"],
            "pdga_number": p["PDGANum"],

            "pool": p["Pool"],
            "card_number": p["CardNum"],
            "tee_time": p["TeeTime"],

            "rating_at_event": p["Rating"],
            "won_playoff": p["WonPlayoff"],
            "prize": p["Prize"],
            "previous_place": p["PreviousPlace"],
            "running_place": p["RunningPlace"],
            "tied": p["Tied"],
            "round_rating": p["RoundRating"],
            "completed": p["Completed"],

            "previous_round_score": p["PrevRndTotal"],
            "grand_total": p["GrandTotal"],
            "round_score": p["RoundScore"],
            "sub_total": p["SubTotal"],
            "round_to_par": p["RoundtoPar"],
            "par_thru_round": p["ParThruRound"],
        })

    return out

def enrich_player_details(player, hole_breakdowns, round_stats):
    return player, hole_breakdowns, round_stats

def fetch_enrichment(scores, delay: float = 0.2):
    breakdown_cache = {}
    stats_cache = {}

    for s in scores:
        score_id = s.get("ScoreID")
        if not score_id:
            continue

        if score_id not in breakdown_cache:
            breakdown_cache[score_id] = get_hole_breakdown(score_id)
        time.sleep(delay)
        if score_id not in stats_cache:
            stats_cache[score_id] = get_round_stats(score_id)
        time.sleep(delay)

    return breakdown_cache, stats_cache

def map_hole_scores(event_id: int, division: str, round_number: int, data):
    hole_scores_out = []

    for p in data["scores"]:
        pars = p.get("Pars", "").split(",")
        score_id = p.get("ScoreID")

        for i, score in enumerate(p.get("HoleScores", [])):
            hole_score = int(score) if score != "" else None
            par = int(pars[i]) if i < len(pars) and pars[i] != "" else None

            hole_scores_out.append({
                # join keys (critical for later enrichment)
                "event_id": event_id,
                "division": division,
                "round_number": round_number,
                "result_id": p["ResultID"],
                "round_id": p["RoundID"],
                "score_id": score_id,
                "pdga_number": p["PDGANum"],

                # hole identity
                "hole_number": i + 1,

                # core values
                "score": hole_score,
                "par": par,
                "score_to_par": (
                    hole_score - par
                    if hole_score is not None and par is not None
                    else None
                ),
            })

    return hole_scores_out

def fetch_hole_breakdowns(scores, delay: float = 0.2):
    breakdown_cache = {}

    for s in scores:
        score_id = s.get("ScoreID")
        if not score_id:
            continue

        if score_id not in breakdown_cache:
            breakdown_cache[score_id] = get_hole_breakdown(score_id)

        time.sleep(delay)

    return breakdown_cache


def fetch_round_stats(scores, delay: float = 0.2):
    stats_cache = {}

    for s in scores:
        score_id = s.get("ScoreID")
        if not score_id:
            continue

        if score_id not in stats_cache:
            stats_cache[score_id] = get_round_stats(score_id)

        time.sleep(delay)

    return stats_cache

def map_hole_breakdowns(hole_breakdowns):
    out = []
    for score_id, holes in hole_breakdowns.items():
        #print(holes)
        for h in holes:
            #print(h)
            breakdown = h.get("holeBreakdown")

            if breakdown is None: # appears for playoff rounds there's an entry but no breakdown
                out.append({
                    "score_id": score_id,
                    "hole_number": h.get("holeOrdinal"),
                    "driving": None,
                    "scramble": None,
                    "green": None,
                    "c1x": None,
                    "c1": None,
                    "c2": None,
                    "throwIn": None,
                    "ob": None,
                    "hazard": None,
                    "missedMando": None,
                    "lostDisc": None,
                    "penalty": None,
                    "has_breakdown": False,  # optional but VERY useful
                })
                continue
            out.append({
                "score_id": score_id,
                "hole_number": h.get("holeOrdinal"),
                # raw stats (no interpretation here)
                "driving": breakdown.get("driving"),
                "scramble": breakdown.get("scramble"),
                "green": breakdown.get("green"),
                "c1x": breakdown.get("c1x"),
                "c1": breakdown.get("c1"),
                "c2": breakdown.get("c2"),
                "throwIn": breakdown.get("throwIn"),
                "ob": breakdown.get("ob"),
                "hazard": breakdown.get("hazard"),
                "missedMando": breakdown.get("missedMando"),
                "lostDisc": breakdown.get("lostDisc"),
                "penalty": breakdown.get("penalty"),
                "has_breakdown": True
            })

    return out

def map_round_stats(stats_cache):
    out = []

    for score_id, stats in stats_cache.items():
        for stat in stats:
            out.append({
                "score_id": score_id,
                "stat_id": stat["statId"],
                "stat_count": stat["statCount"],
                "stat_opportunity_count": stat["statOpportunityCount"],
                "stat_value": stat["statValue"],
            })

    return out

def parse_round(event_id: int, division: str, round_number: int, payload, debug:bool=False):
    data = payload["data"]

    if debug:
        print(f"Now Parsing: {event_id}, division: {division}, round: {round_number}")

    round_info = map_round_info(event_id, division, round_number, data)
    players = map_players(data)
    player_round = map_player_round(event_id, division, round_number, data)


    #print(data["scores"])
    breakdown_cache, stats_cache = fetch_enrichment(data["scores"])

    hole_scores = map_hole_scores(
        event_id, division, round_number, data,
    )
    #print(breakdown_cache)
    hole_breakdown = map_hole_breakdowns(breakdown_cache)

    player_round_stats = map_round_stats(data, stats_cache)

    return round_info, hole_scores, player_round, players, player_round_stats, hole_breakdown

# ~~~~~~~ OG BELOW ~~~~~~~~~~~

if __name__ == "__main__":
    payload = get_round(96407, "FPO", 12)

    #round_info, hole_scores, round_context, players, round_stats = parse_round(96410, "MPO", 1, payload)
    round_info, hole_scores, round_context, players, round_context_stats, hole_breakdowns = parse_round(96407, "FPO", 13, payload)
    print(round_info)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(hole_scores[0])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(round_context[0])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(players[0])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(round_context_stats[0])
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(hole_breakdowns[0])
    
