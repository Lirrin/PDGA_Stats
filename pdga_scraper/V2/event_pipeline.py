import event_scraper
import round_scraper
from models.event import to_event
from models.eventdivision import to_event_division
from models.course import to_course
from models.courselayout import to_course_layout
from models.hole import to_hole
from models.tournamentround import to_tournament_round
from models.playerround import to_player_round
from models.eventplayer import to_event_player
from models.pdgaplayer import to_player
from models.holescore import to_hole_score
from models.playerroundstats import to_player_round_stats
from models.holebreakdown import to_hole_breakdown
import time

def process_event(event_id, debug=False):
    #results objects
    events = {}
    event_divisions = {}
    courses = {}
    course_layouts = {}
    layout_holes = {}
    tournament_rounds = {}
    player_rounds = {}
    player_scores = {}
    tournament_player = {}
    all_players = {}
    player_round_stats = {}
    player_hole_stats = {}

    if debug:
        print(f'Now parsing event {event_id}')

    # Get and Parse Event Format
    format = event_scraper.get_tournament_format(event_id)
    rounds = event_scraper.map_tournament_format(format)
    
    #Get Event API 
    payload = event_scraper.get_event(event_id)
    data = payload["data"]


    #Map Event Data and save to dict of events
    event_data = event_scraper.map_event(event_id, data)
    events[event_id] = to_event(event_data)

    #Map progress
    progress = event_scraper.map_progress(event_id, data)

    #Map Division data and save to dict of divisions
    divisions = event_scraper.map_divisions(event_id, data)
    for division in divisions:
        division_id = division["division_id"]
        division["final_round"] = progress["final_round"]
        
        if (event_id, division_id) not in event_divisions:
            event_divisions[(event_id, division_id)] = to_event_division(division)

    #Map Courses & Layouts and save to dict of courses & layouts
    layouts, holes = event_scraper.map_layouts(event_id, data)
    for layout in layouts:
        course_id = layout["course_id"]
        layout_id = layout["layout_id"]
        if course_id not in courses:
            courses[course_id] = to_course(layout) #returns a Course class object

        if (course_id, layout_id) not in course_layouts:
            course_layouts[(course_id, layout_id)] = to_course_layout(layout)

    #Map Layout Holes and save to dict of holes
    for hole in holes:
        layout_id = hole["layout_id"]
        hole_num = hole["hole_number"]

        if (layout_id, hole_num) not in layout_holes:
                layout_holes[layout_id, hole_num] = to_hole(hole)

    #Start Round Processing
    for round in rounds:
        round_id = round["round_id"]
        round_code = round["round_code"],
        round_number = round["ordinal_round"]
        division_code = round["division"] #e.g. MPO/FPO
        if int(round_id) > int(progress["final_round"]):
            playoff=True
        else:
            playoff=False

        #Fetch the round API results
        round_payload = round_scraper.get_round(event_id, division_code, round_code)
        data = round_payload["data"]

        #Get Round Metadata
        round_info = round_scraper.map_round_info(event_id, division_code, round_number, data)
        if round_id not in tournament_rounds:
            tournament_rounds[round_id] = to_tournament_round(round_info, round_id, round_code, round_number, playoff)

        #Get Player Rounds
        played_rounds = round_scraper.map_player_round(event_id, division_code, round_number, data)
        for p_round in played_rounds:
            result_id = p_round["result_id"] # the id uniquely identifying a round in PDGA data 
            score_id = p_round["score_id"]
            pdga_num = p_round["pdga_number"]
            if(round_id, result_id, score_id) not in player_rounds:
                player_rounds[(round_id, result_id, score_id)] = to_player_round(p_round, playoff)
            if (event_id, pdga_num) not in tournament_player:
                tournament_player[(event_id, pdga_num)] = to_event_player(p_round)

        hole_scores = round_scraper.map_hole_scores(event_id, division_code, round_number, data)
        for score in hole_scores:
            result_id = score["result_id"]
            score_id = score["score_id"]
            hole_num = score["hole_number"]
            if (round_id, result_id, score_id, hole_num) not in player_scores: # is this needed, theoretically there should be no dupes
                player_scores[(round_id, result_id, score_id, hole_num)] = to_hole_score(score)

        players = round_scraper.map_players(data)
        for player in players: 
            pdga_num = player["pdga_number"]
            if pdga_num not in all_players:
                player[pdga_num] = to_player(player)

        breakdown_cache, stats_cache = round_scraper.fetch_enrichment(data["scores"])
        hole_breakdown = round_scraper.map_hole_breakdowns(breakdown_cache)
        for breakdown in hole_breakdown:
            score_id = breakdown["score_id"]
            player_hole_stats["score_id"] = to_hole_breakdown(breakdown)

        round_stats = round_scraper.map_round_stats(data, stats_cache)
        for rnd_stats in round_stats:
            score_id = rnd_stats["score_id"]
            player_round_stats[score_id] = to_player_round_stats(rnd_stats)
        
        time.sleep(20) #sleep between rounds


    data_sets = {
        "events": events,
        "event_divisions": event_divisions,
        "courses": courses,
        "course_layouts": course_layouts,
        "layout_holes": layout_holes,
        "tournament_rounds": tournament_rounds,
        "player_rounds": player_rounds,
        "player_scores": player_scores,
        "tournament_player": tournament_player,
        "all_players": all_players,
        "player_round_stats": player_round_stats,
        "player_hole_stats": player_hole_stats
    }
    return data_sets


