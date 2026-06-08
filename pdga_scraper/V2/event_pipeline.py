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
        
        if (event_id, division_id) not in event_divisions.keys():
            event_divisions[(event_id, division_id)] = to_event_division(division)

    #Map Courses & Layouts and save to dict of courses & layouts
    layouts, holes = event_scraper.map_layouts(event_id, data)
    for layout in layouts:
        course_id = layout["course_id"]
        layout_id = layout["layout_id"]
        if course_id not in courses.keys():
            courses[course_id] = to_course(layout) #returns a Course class object

        if (course_id, layout_id) not in course_layouts.keys():
            course_layouts[(course_id, layout_id)] = to_course_layout(layout)

    #Map Layout Holes and save to dict of holes
    for hole in holes:
        layout_id = hole["layout_id"]
        hole_num = hole["hole_number"]

        if (layout_id, hole_num) not in layout_holes.keys():
                layout_holes[layout_id, hole_num] = to_hole(hole)


    ### BELOW HERE IS THE OLD Logic

    event_data, divisions, progress, layouts, holes = event_scraper.parse_event(event_id, payload, debug=debug)


    events[event_id] = to_event(event_data)

    for division in divisions:
        division_id = division["division_id"]
        division["final_round"] = progress["final_round"]
        
        if (event_id, division_id) not in event_divisions.keys():
            event_divisions[(event_id, division_id)] = to_event_division(division)

    for layout in layouts:
        course_id = layout["course_id"]
        layout_id = layout["layout_id"]
        if course_id not in courses.keys():
            courses[course_id] = to_course(layout) #returns a Course class object

        if (course_id, layout_id) not in course_layouts.keys():
            course_layouts[(course_id, layout_id)] = to_course_layout(layout)

    for hole in holes:
        layout_id = hole["layout_id"]
        hole_num = hole["hole_number"]

        if (layout_id, hole_num) not in layout_holes.keys():
                layout_holes[layout_id, hole_num] = to_hole(hole)

    for round in rounds:
        round_payload = round_scraper.get_round(event_id, round["division"], round["round_code"])
        round_id = round["round_id"]
        round_code = round["round_code"],
        round_num = round["ordinal_round"]
        if int(round_id) > int(progress["final_round"]):
            playoff=True
        else:
            playoff=False
        round_info, hole_scores, round_context, players, round_context_stats = round_scraper.parse_round(event_id, round["division"], round["ordinal_round"], round_payload, debug=debug)
        
        #tournament_rounds = {}
        if round_id not in tournament_rounds.keys():
            tournament_rounds[round_id] = to_tournament_round(round_info, round_id, round_code, round_num, playoff)

        #player_rounds = {}
        for context in round_context:
            result_id = context["result_id"]
            score_id = context["score_id"]
            pdga_num = context["pdga_number"]
            if (round_id, result_id, score_id) not in player_rounds.keys(): #do we need this theoretically no dupes
                player_rounds[(round_id, result_id, score_id)] = to_player_round(context, playoff)
            #tournament_player = {}
            if (event_id, pdga_num) not in tournament_player.keys():
                tournament_player[(event_id, pdga_num)] = to_event_player(context)


        #player_scores = {}
        for score in hole_scores:
            result_id = score["result_id"]
            score_id = score["score_id"]
            hole_num = score["hole_number"]
            if (round_id, result_id, score_id, hole_num) not in player_scores.keys(): # is this needed, theoretically there should be no dupes
                player_scores[(round_id, result_id, score_id, hole_num)] = to_hole_score(score)

        #all_players = {}
        for player in players: #No versioning for player data, which is ok for now
            pdga_num = player["pdga_number"]
            if pdga_num not in all_players.keys():
                player[pdga_num] = to_player(player)


        #player_round_stats = {}
        for rnd_stats in round_context_stats: 
            score_id = rnd_stats["score_id"]
            player_round_stats[score_id] = to_player_round_stats(rnd_stats)
        #sleep between rounds
        time.sleep(5) # to avoid hitting api rate limits 

    #sleep between events
    time.sleep(30) # to avoid hitting api rate limits 

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
    }
    return data_sets