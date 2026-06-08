import requests
import event_scraper
import round_scraper
from models.event import Event
from models.eventdivision import EventDivision
from models.course import Course
from models.courselayout import CourseLayout
from models.hole import Hole
from models.tournamentround import TournamentRound
from models.playerround import PlayerRound
from models.eventplayer import EventPlayer
from models.pdgaplayer import PDGAPlayer
from models.holescore import HoleScore
from models.playerroundstats import PlayerRoundStats
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


    format = event_scraper.get_tournament_format(event_id)
    rounds = event_scraper.map_tournament_format(format)
    
    payload = event_scraper.get_event(event_id)

    event_data, divisions, progress, layouts, holes = event_scraper.parse_event(event_id, payload, debug=debug)


    events[event_id] = Event(
        event_id= event_id,
        name=event_data["name"],
        #date_range=event_data["date_range"],
        start_date=event_data["start_date"],
        end_date=event_data["end_date"],
        location_full=event_data["location"],
        location_short=event_data["location_short"],
        country=event_data["country"],
        name_main=event_data["name_main"],
        name_pre=event_data["name_pre"],
        name_post=event_data["name_post"],
        tier_code=event_data["raw_tier"],
        tier_name=event_data["tier"],
        #semis=event_data["semis"],
        td_name=event_data["td_name"],
        td_pdga_number=event_data["td_pdga_number"],
        time_zone=event_data["timezone"],
        scoring_format=event_data["scoring_format"],
        is_x_tier=event_data["tier_x"],
    )
    for division in divisions:
        division_id = division["division_id"]
        
        if (event_id, division_id) not in event_divisions.keys():
            event_divisions[(event_id, division_id)] = EventDivision(
                event_id = event_id,
                division_id = division_id,
                division_code = division["division"],
                division_name = division["division_name"],
                player_count = int(division["players"]) if division["players"] != "" else None,
                is_pro = division["is_pro"],
                final_round_code = progress["final_round"]
            )

    for layout in layouts:
        course_id = layout["course_id"]
        layout_id = layout["layout_id"]
        if course_id not in courses.keys():
            courses[course_id] = Course(
                    course_id=course_id,
                    course_name=layout["course_name"]
            )

        if (course_id, layout_id) not in course_layouts.keys():
            course_layouts[(course_id, layout_id)] = CourseLayout(
                course_id=course_id,
                layout_id=layout_id,
                layout_name = layout["layout_name"],
                hole_count = layout["holes"],
                course_par = layout["par"],
                total_length = layout["length"],
                length_unit = layout["units"]
            )

    for hole in holes:
        layout_id = hole["layout_id"]
        hole_num = hole["hole_number"]

        if (layout_id, hole_num) not in layout_holes.keys():
                layout_holes[layout_id, hole_num] = Hole(
                layout_id = layout_id,
                hole_number = hole_num,
                hole_par = hole["hole_par"],
                hole_length = hole["hole_length"],
                length_unit = hole["units"]
        )



    for round in rounds:
        round_payload = round_scraper.get_round(event_id, round["division"], round["round_code"])
        round_id = round["round_id"]
        if int(round_id) > int(progress["final_round"]):
            playoff=True
        else:
            playoff=False
        round_info, hole_scores, round_context, players, round_context_stats = round_scraper.parse_round(event_id, round["division"], round["ordinal_round"], round_payload, debug=debug)
        
        #tournament_rounds = {}
        if round_id not in tournament_rounds.keys():
            tournament_rounds[round_id] = TournamentRound(
                event_id = event_id,
                round_id = round_id,
                round_code = round["round_code"],
                round_num = round["ordinal_round"],
                division_code = round["division"],
                pool = round_info["pool"],
                course_id = round_info["course_id"],
                layout_id = round_info["layout_id"],
                is_playoff = playoff
            )

        #player_rounds = {}
        for context in round_context:
            result_id = context["result_id"]
            score_id = context["score_id"]
            pdga_num = context["pdga_number"]
            if (round_id, result_id, score_id) not in player_rounds.keys(): #do we need this theoretically no dupes
                player_rounds[(round_id, result_id, score_id)] = PlayerRound(
                    #result_id = result_id,
                    round_id = round_id,
                    score_id = score_id,
                    pdga_number = pdga_num,
                    round_code = round["round_code"],
                    round_number = round["ordinal_round"],
                    is_playoff = playoff,
                    pool = context["pool"],
                    card_number = context["card_number"],
                    tee_time = context["tee_time"],
                    place_before_round = context["previous_place"] if round["ordinal_round"] > 1 else None,
                    place_after_round = context["running_place"],
                    is_tied = context["tied"],
                    round_rating = context["round_rating"],
                    is_complete = bool(context["completed"]),
                    total_score_before_round = context["previous_round_score"],
                    round_score = context["round_score"],
                    total_score_after_round = context["sub_total"],
                    round_to_par = context["round_to_par"],
                    to_par_after_round = context["par_thru_round"]
                )
            #tournament_player = {}
            if (event_id, pdga_num) not in tournament_player.keys():
                tournament_player[(event_id, pdga_num)] = EventPlayer(
                    event_id = event_id,
                    pdga_number = pdga_num, 
                    player_rating_at_event = context["rating_at_event"],
                    won_playoff = context["won_playoff"],
                    prize = context["prize"],
                    total_strokes = context["grand_total"]
                )


        #player_scores = {}
        for score in hole_scores:
            result_id = score["result_id"]
            score_id = score["score_id"]
            hole_num = score["hole_number"]
            if (round_id, result_id, score_id, hole_num) not in player_scores.keys(): # is this needed, theoretically there should be no dupes
                player_scores[(round_id, result_id, score_id, hole_num)] = HoleScore(
                    #result_id = result_id,
                    round_id = round_id,
                    #score_id = score_id,
                    pdga_number = score["pdga_number"],
                    hole_number = hole_num,
                    strokes = score["score"],
                    par = score["par"],
                    score_to_par = score["score_to_par"],
                    driving_landing_zone = score["driving"],
                    scramble = score["scramble"],
                    green_regulation_zone = score["green"],
                    c1x_putts = score["c1x"],
                    c1_putts = score["c1"],
                    c2_putts = score["c2"],
                    made_distance = score["throwIn"],
                    ob_strokes = score["ob"],
                    hazard_strokes = score["hazard"],
                    missed_mando_strokes = score["missedMando"],
                    lost_disc_strokes = score["lostDisc"],
                    penalty_strokes = score["penalty"]
                )


        #all_players = {}
        for player in players: #No versioning for player data, which is ok for now
            pdga_num = player["pdga_number"]
            if pdga_num not in all_players.keys():
                player[pdga_num] = PDGAPlayer(
                    pdga_number= pdga_num,
                    full_name = player["full_name"],
                    first_name = player["first_name"],
                    last_name = player["last_name"],
                    home_city = player["home_city"],
                    home_state = player["home_state"],
                    home_country = player["home_country"],
                    home_location = player["full_location"]
                )


        #player_round_stats = {}
        for rnd_stats in round_context_stats: 
            score_id = rnd_stats["score_id"]
            player_round_stats[score_id] = PlayerRoundStats(
                score_id = score_id,
                stat_id = rnd_stats["stat_id"],
                stat_count = rnd_stats["stat_count"],
                stat_opportunity = rnd_stats["stat_opportunity_count"],
                stat_value = rnd_stats["stat_value"]
            )
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