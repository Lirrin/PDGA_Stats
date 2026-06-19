from pdga_scraper import event_scraper
from pdga_scraper import round_scraper
from pdga_scraper.models.event import to_event
from pdga_scraper.models.eventdivision import to_event_division
from pdga_scraper.models.course import to_course
from pdga_scraper.models.courselayout import to_course_layout
from pdga_scraper.models.hole import to_hole
from pdga_scraper.models.tournamentround import to_tournament_round
from pdga_scraper.models.playerround import to_player_round
from pdga_scraper.models.eventplayer import to_event_player
from pdga_scraper.models.pdgaplayer import to_player
from pdga_scraper.models.holescore import to_hole_score
from pdga_scraper.models.playerroundstats import to_player_round_stats
from pdga_scraper.models.holebreakdown import to_hole_breakdown
import traceback
import json

import time

def pipeline(event_id:int, datasets, debug: bool = False, round_limit:int = None, sleep = 10):
    
    rounds = process_event(event_id, datasets, debug)
    cnt = 0
    for round_info in rounds:
        try:
            process_round(event_id, datasets, round_info, debug)
            time.sleep(sleep) # small wait between rounds to avoid api limits
            if round_limit:
                cnt += 1
                if cnt >= round_limit:
                    break #testing function to allow only running 1
        except Exception as e:
            print(f'Failure at {event_id}. Round: {round_info["division"]}-{round_info["ordinal_round"]}')
            traceback.print_exc()
            print(e)
            continue

    return datasets

def process_event(event_id, datasets, debug:bool=False):
    if debug:
        print(f'[EVENT START] {event_id=}')

    # Get and Parse Event Format
    format = event_scraper.get_tournament_format(event_id)
    rounds = event_scraper.map_tournament_format(format)

    #Get Event API 
    payload = event_scraper.get_event(event_id)
    data = payload["data"]

    # if debug:
    #     with open(f"debug/Event_Format_Format_{event_id}.json", "w") as f:
    #         json.dump(format, f, indent=4)
    #     with open(f"debug/Event_Response_{event_id}.json", "w") as f1:
    #         json.dump(payload, f1, indent=4)

    #Map Event Data and save to dict of events
    event_data = event_scraper.map_event(event_id, data)
    datasets.events[event_id] = to_event(event_data)

    #Map progress
    progress = event_scraper.map_progress(event_id, data)
    for rnd in rounds:
        rnd['final_round'] = progress['final_round']

    #Map Division data and save to dict of divisions
    divisions = event_scraper.map_divisions(event_id, data)
    for division in divisions:
        division_id = division["division_id"]
        division["final_round"] = progress["final_round"]
        
        if (event_id, division_id) not in datasets.event_divisions:
            datasets.event_divisions[(event_id, division_id)] = to_event_division(division)

    #Map Courses & Layouts and save to dict of courses & layouts
    layouts, holes = event_scraper.map_layouts(event_id, data)
    for layout in layouts:
        course_id = layout["course_id"]
        layout_id = layout["layout_id"]
        if course_id not in datasets.courses:
            datasets.courses[course_id] = to_course(layout) #returns a Course class object

        if layout_id not in datasets.course_layouts:
            datasets.course_layouts[layout_id] = to_course_layout(layout)

    #Map Layout Holes and save to dict of holes
    for hole in holes:
        layout_id = hole["layout_id"]
        hole_seq = hole["hole_seq"]

        if (layout_id, hole_seq) not in datasets.layout_holes:
                datasets.layout_holes[(layout_id, hole_seq)] = to_hole(hole)

    return rounds

def process_hole_breakdowns(scores, datasets, debug = False):
    breakdown_cache = round_scraper.fetch_hole_breakdowns(scores)

    hole_breakdowns = round_scraper.map_hole_breakdowns(
        breakdown_cache
    )

    for breakdown in hole_breakdowns:
        score_id = breakdown["score_id"]
        hole_seq = breakdown["hole_number"]
        datasets.player_hole_stats[(score_id, hole_seq)] = (
            to_hole_breakdown(breakdown)
        )


def process_round_stats(scores, datasets,debug = False):
    stats_cache = round_scraper.fetch_round_stats(scores)

    round_stats = round_scraper.map_round_stats(
        stats_cache
    )

    for rnd_stats in round_stats:
        score_id = rnd_stats["score_id"]
        stat_id = rnd_stats["stat_id"]
        datasets.player_round_stats[(score_id, stat_id)] = (
            to_player_round_stats(rnd_stats)
        )


def process_round(event_id, datasets, round_info, debug = False):
        round_id = round_info["round_id"]
        round_code = round_info["round_code"]
        round_number = round_info["ordinal_round"]
        division_code = round_info["division"] #e.g. MPO/FPO
        if debug:
            print(f"[ROUND START] {event_id=} {division_code=} {round_number=}")

        if int(round_code) > int(round_info["final_round"]):
            playoff=True
        else:
            playoff=False

        #Fetch the round API results
        round_payload = round_scraper.get_round(event_id, division_code, round_code)
        data = round_payload["data"]

        # if debug:
        #     with open(f"debug/Data_Event_{event_id}_Division_{division_code}_Round_{round_code}.json", "w") as f:
        #         json.dump(round_payload, f, indent=4)

        #Get Round Metadata
        round_info = round_scraper.map_round_info(event_id, division_code, round_number, data)
        if round_id not in datasets.tournament_rounds:
            datasets.tournament_rounds[round_id] = to_tournament_round(round_info, round_id, round_code, round_number, playoff)

        #Get Player Rounds
        played_rounds = round_scraper.map_player_round(event_id, division_code, round_number, data)
        for p_round in played_rounds:
            result_id = p_round["result_id"] # the id uniquely identifying a round in PDGA data 
            score_id = p_round["score_id"]
            pdga_num = p_round["pdga_number"]
            if (round_id, score_id, pdga_num) not in datasets.player_rounds:
                datasets.player_rounds[(round_id, score_id, pdga_num)] = to_player_round(p_round, round_number, playoff)
            if (event_id, pdga_num) not in datasets.tournament_player:
                datasets.tournament_player[(event_id, pdga_num)] = to_event_player(p_round)

        hole_scores = round_scraper.map_hole_scores(event_id, division_code, round_number, data)
        for score in hole_scores:
            result_id = score["result_id"]
            score_id = score["score_id"]
            hole_seq = score["hole_number"]
            if (round_id, score_id, hole_seq) not in datasets.player_scores: # is this needed, theoretically there should be no dupes
                datasets.player_scores[(round_id, score_id, hole_seq)] = to_hole_score(score)

        players = round_scraper.map_players(data)
        for player in players: 
            pdga_num = player["pdga_number"]
            if pdga_num not in datasets.all_players:
                datasets.all_players[pdga_num] = to_player(player)

        players = round_scraper.map_players(data)

        process_hole_breakdowns(data["scores"], datasets)
        process_round_stats(data["scores"], datasets)
        

from pdga_scraper.Datasets.datasets import DataSets
if __name__ == "__main__":
    scores =  [
            {
                "ResultID": 212274762,
                "RoundID": 122765866,
                "ScoreID": 27904496,
            },
            {
                "ResultID": 212274837,
                "RoundID": 122765866,
                "ScoreID": 27903530,
            }
    ]
    datasets = DataSets()
    # #Testing Hole Breakdowns
    
    breakdown_cache = round_scraper.fetch_hole_breakdowns(scores)
    print(breakdown_cache[scores[0]["ScoreID"]][0])
    hole_breakdowns = round_scraper.map_hole_breakdowns(
        breakdown_cache
    )
    print('~~~~~~~~~~~~~~~~~')
    print(hole_breakdowns[0])
    for breakdown in hole_breakdowns:
        score_id = breakdown["score_id"]
        datasets.player_hole_stats[score_id] = (
            to_hole_breakdown(breakdown)
        )

    #Test Round stats
    # stats_cache = round_scraper.fetch_round_stats(scores)
    # #print(stats_cache)
    # round_stats = round_scraper.map_round_stats(
    #     stats_cache
    # )

    # for rnd_stats in round_stats:
    #     score_id = rnd_stats["score_id"]
    #     stat_id = rnd_stats["stat_id"]
    #     datasets.player_round_stats[(score_id,stat_id)] = (
    #         to_player_round_stats(rnd_stats)
    #     )
    #     print(rnd_stats)

    # print(datasets.player_round_stats)