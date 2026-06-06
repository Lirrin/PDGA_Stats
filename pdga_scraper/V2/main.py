

# need to use this endpoint for an event to get the rounds in the event 
# https://www.pdga.com/api/v1/live-tournaments/96407/live-rounds?include=LiveRoundCut
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


def get_tournament_format(event_id):
    url = f"https://www.pdga.com/api/v1/live-tournaments/{event_id}/live-rounds?include=LiveRoundCut"
    payload = requests.get(url).json()

    # Group rounds by division
    rounds_by_division = {}
    for round in payload:
        if round["division"] in ["FPO", "MPO"]:
            if round["division"] not in rounds_by_division:
                rounds_by_division[round["division"]] = []
            rounds_by_division[round["division"]].append(round)
    
    # Sort each division's rounds and assign ordinal numbers
    round_list = []    
    num_rounds = {}
    for division in rounds_by_division:
        sorted_rounds = sorted(
        rounds_by_division[division],
        key=lambda r: r["round"]
    )
        
        num_rounds[division] = len(sorted_rounds)

        for ordinal, round in enumerate(sorted_rounds, start=1):
            round_list.append({
                "round_id": round["roundId"],
                "division": round["division"],
                "round_code": round["round"],
                "ordinal_round": ordinal
            })

    return round_list, num_rounds

event_list = [96407] # placeholder

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
players = {}
player_round_stats = {}


for event_id in event_list:
    rounds, num_rounds_dict = get_tournament_format(event_id)
    
    payload = event_scraper.get_event(event_id)

    event_data, divisions, progress, course_layouts, holes = event_scraper.parse_event(event_id, payload)


    events[event_id] = Event(
        event_id= event_id,
        name=event_data["name"],
        date_range=event_data["date_range"],
        start_date=event_data["start_date"],
        end_date=event_data["end_date"],
        location=event_data["location"],
        location_short=event_data["location_short"],
        country=event_data["country"],
        name_main=event_data["name_main"],
        name_pre=event_data["name_pre"],
        name_post=event_data["name_post"],
        raw_tier=event_data["raw_tier"],
        tier=event_data["tier"],
        semis=event_data["semis"],
        td_name=event_data["td_name"],
        td_pdga_number=event_data["td_pdga_number"],
        time_zone=event_data["timezone"],
        scoring_format=event_data["scoring_format"],
        tier_x=event_data["tier_x"],
    )
    for division in divisions:
        division_id = division["division_id"]
        
        if (event_id, division_id) not in event_divisions.keys():
            event_divisions[(event_id, division_id)] = EventDivision(
                event_id = event_id,
                division_id = division_id,
                division = division["division"],
                division_name = division["division_name"],
                players = int(division["players"]) if division["players"] != "" else None,
                is_pro = division["is_pro"],
                final_round_code = progress["final_round"]
            )

    for layout in course_layouts:
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
                holes = layout["holes"],
                length = layout["length"],
                units = layout["units"]
            )

    for hole in holes:
        layout_id = hole["layout_id"]
        hole_num = hole["hole_number"]

        if (layout_id, hole_num) not in layout_holes.keys():
                layout_holes(layout_id, hole_num) = Hole(
                layout_id = layout_id,
                hole_number = hole_num,
                par = hole["par"],
                length = hole["hole_length"],
                units = hole["units"]
        )



    for round in rounds:
        round_payload = round_scraper.get_round(event_id, round["division"], round["round_code"])
        round_id = round["round_id"]
        if int(round_id) > int(progress["final_round"]):
            playoff=True
        else:
            playoff=False
        round_info, hole_scores, round_context, players, round_context_stats = round_scraper.parse_round(event_id, round["division"], round["ordinal_round"], round_payload)
        
        #tournament_rounds = {}
        if round_id not in tournament_rounds.keys():
            tournament_rounds[round_id] = TournamentRound(
                event_id = event_id,
                round_id = round_id,
                round_code = round["round_code"],
                round_num = round["ordinal_round"],
                division = round["division"],
                pool = round_info["pool"],
                course_id = round_info["course_id"],
                layout_id = round_info["layout_id"],
                shotgun_time = round_info["shotgun_time"],
                tee_times = round_info["tee_times"],
                is_playoff = playoff
            )

        #player_rounds = {}
        result_id = hole_scores["result_id"]
        score_id = hole_scores["score_id"]
        if (round_id, result_id, score_id) not in player_rounds.keys():
            player_rounds[(round_id, result_id, score_id)] = PlayerRound(
                result_id = result_id,
                round_id = round_id,
                score_id = score_id,
                pdga_number = round_context["pdga_number"],
                round_code = round["round_code"],
                round_number = round["ordinal_round"],
                is_playoff = playoff,
                pool = round_context["pool"],
                card_number = round_context["card_number"],
                tee_time = round_context["TeeTime"],
                previous_place = round_context["previous_place"] if round["ordinal_round"] > 1 else None,
                post_place = round_context["running_place"],
                tied = round_context["tied"],
                round_rating = round_context["round_rating"],
                is_complete = bool(round_context["complete"]),
                previous_total_score = round_context["previous_round_score"],
                round_score = round_context["round_score"],
                post_total_score = round_context["subtotal"],
                round_to_par = round_context["round_to_par"],
                total_to_par = round_context["par_thru_round"]
            )
        #tournament_player = {}

        #player_scores = {}


        #players = {}


        #player_round_stats = {}



        
    