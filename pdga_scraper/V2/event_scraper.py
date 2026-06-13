import requests

def get_event(event_id):
    url = f"https://www.pdga.com/apps/tournament/live-api/live_results_fetch_event"
    params = {"TournID": event_id}
    return requests.get(url, params=params).json()  

def get_tournament_format(event_id):
    url = f"https://www.pdga.com/api/v1/live-tournaments/{event_id}/live-rounds?include=LiveRoundCut"
    return requests.get(url).json()

def map_tournament_format( data, target_divisions = ['MPO', 'FPO']):
    # Group rounds by division
    rounds_by_division = {}
    for round in data:
        if round["division"] in target_divisions:
            if round["division"] not in rounds_by_division:
                rounds_by_division[round["division"]] = []
            rounds_by_division[round["division"]].append(round)
    
    # Sort each division's rounds and assign ordinal numbers
    round_list = []    
    for division in rounds_by_division:
        sorted_rounds = sorted(
        rounds_by_division[division],
        key=lambda r: r["round"]
    )

        for ordinal, round in enumerate(sorted_rounds, start=1):
            round_list.append({
                "round_id": round["roundId"],
                "division": round["division"],
                "round_code": round["round"],
                "ordinal_round": ordinal
            })

    return round_list

def map_event(event_id: int, data):
    return {
        "event_id": event_id,
        "date_range": data["DateRange"],
        "start_date": data["StartDate"],
        "end_date": data["EndDate"],
        "location": data["Location"],
        "location_short": data["LocationShort"],
        "country": data["Country"],
        "name": data["Name"],
        "name_main": data["MultiLineName"]["main"],
        "name_pre": data["MultiLineName"]["pre"],
        "name_post": data["MultiLineName"]["post"],
        "raw_tier": data["RawTier"],
        "tier": data["Tier"],
        "semis": data["Semis"],
        "td_name": data["TDName"],
        "td_pdga_number": data["TDPDGANum"],
        "timezone": data["TimeZone"],
        "scoring_format": data["ScoringFormat"],
        "tier_x": data["TierX"],
    }

def map_divisions(event_id: int, data):
    return [
        {
            "event_id": event_id,
            "division_id": d["DivisionID"],
            "division": d["Division"],
            "division_name": d["DivisionName"],
            "players": d["Players"],
            "is_pro": d["IsPro"],
            "latest_round": d["LatestRound"],
            "short_name": d["ShortName"],
        }
        for d in data["Divisions"]
    ]

def map_layouts(event_id: int, data):
    layouts = []
    holes = []

    for c in data["Layouts"]:
        layout_id = c["LayoutID"]
        course_id = c["CourseID"]
        units = c["Units"]

        layouts.append({
            "event_id": event_id,
            "layout_id": layout_id,
            "layout_name": c["Name"],
            "course_id": course_id,
            "course_name": c["CourseName"],
            "holes": c["Holes"],
            "par": c["Par"],
            "length": c["Length"],
            "units": units,
        })

        for h in c["Details"]:
            holes.append({
                "layout_id": layout_id,
                "course_id": course_id,
                "hole_seq": h["Hole"], #order of hole
                "hole_number": h["Label"], #actual hole
                "hole_par": h["Par"],
                "hole_length": h["Length"],
                "units": units,
            })

    return layouts, holes

def map_progress(event_id: int, data):
    return {
        "event_id": event_id,
        "highest_completed_round": data["HighestCompletedRound"],
        "latest_round": data["LatestRound"],
        "final_round": data["FinalRound"],
        "finals": data["Finals"],
    }

def parse_event(event_id: int, payload, debug: bool = False):
    data = payload["data"]

    if debug:
        print(f"Now Parsing {event_id}")

    event = map_event(event_id, data)
    divisions = map_divisions(event_id, data)
    progress = map_progress(event_id, data)
    layouts, holes = map_layouts(event_id, data)

    return event, divisions, progress, layouts, holes

if __name__ == "__main__": 
        
    payload = get_event(96410)

    event, divisions, progress , course_layouts, holes = parse_event(96410, payload)

    print(event)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(divisions)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(progress)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print(course_layouts)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    #print(holes)
