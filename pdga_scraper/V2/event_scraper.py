import requests

def get_event(event_id):
    url = f"https://www.pdga.com/apps/tournament/live-api/live_results_fetch_event"
    params = {"TournID": event_id}
    return requests.get(url, params=params).json()  



def parse_event(event_id: int, payload: dict):
    data = payload["data"]

    event = {
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
        "tier_x": data["TierX"] # binary flag for if its an X tier event
    }

    divisions = []
    for d in data["Divisions"]:
        divisions.append({
            "event_id": event_id,
            "division_id": d["DivisionID"],
            "division": d["Division"],
            "division_name": d["DivisionName"],
            "players": d["Players"],
            "is_pro": d["IsPro"],
            "latest_round": d["LatestRound"],
            "short_name": d["ShortName"]
        })

    course_layouts = []
    holes = []
    for c in data["Layouts"]:
        courseID = c["CourseID"]
        layoutID = c["LayoutID"]
        units = c["Units"]

        course_layouts.append({
            "event_id": event_id,
            "layout_id": layoutID,
            "layout_name": c["Name"],
            "course_id": courseID,
            "course_name": c["CourseName"],
            "holes": c["Holes"],
            "par": c["Par"],
            "length": c["Length"],
            "units": units
        })
        for h in c["Details"]:
            holes.append({ #assumes layouts are unique across courses and across events i.e. course changed 1 hole its a new layout
                "layout_id": layoutID,
                "course_id": courseID,
                "hole_number": h["Label"],
                "hole_par": h["Par"],
                "hole_length": h["Length"],
                "units": units
            })

    progress = {
        "event_id": event_id,
        "highest_completed_round": data["HighestCompletedRound"], #if playoff it will be greater than latest round/final round
        "latest_round": data["LatestRound"],
        "final_round": data["FinalRound"],
        "finals": data["Finals"]
    }

    return event, divisions, progress , course_layouts, holes

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
