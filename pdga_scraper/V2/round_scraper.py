import requests
import time

def get_round(event_id, division, round_number):
    url = "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_round"
    
    params = {
        "TournID": event_id,
        "Division": division,
        "Round": round_number
    }
    
    return requests.get(url, params=params).json()

def get_hole_breakdown(score_id):
    url = f"https://www.pdga.com/api/v1/feat/live-scores/{score_id}/hole-breakdowns"  
    return requests.get(url).json()

def get_round_stats(score_id):
    url = f"https://www.pdga.com/api/v1/feat/live-scores/{score_id}/round-stats"  
    return requests.get(url).json()

def parse_round(event_id: int, division: str, round_number: int, payload: dict):
    data = payload["data"]
    layouts = data["layouts"][0] # should only be 1 layout but its a list in the data so we have to pull it out like this - might need to change if we want to support multiple layouts in a round in the future
    round_info = {
        "event_id": event_id,
        "division": division,
        "round_number": round_number,
        "pool": data["pool"],
        #"round_name": data["RoundName"],
        "course_id": layouts["CourseID"],
        "layout_id": layouts["LayoutID"],
        "live_round_id": data["live_round_id"], #might need this unsure
        "shotgun_time": data["shotgun_time"],
        "tee_times": data["tee_times"],
    }

    round_context = []
    hole_scores = []
    players = []
    round_context_stats = []
    for player_round in data["scores"]:
        pars = player_round.get("Pars", "").split(",")
        score_id = player_round["ScoreID"]

        hole_breakdowns = get_hole_breakdown(score_id=score_id)
        round_stats = get_round_stats(score_id=score_id)

        breakdown_by_hole = {
            h["holeOrdinal"]: h
            for h in hole_breakdowns
        }

        for i, score in enumerate(player_round.get("HoleScores", [])):
            breakdown = breakdown_by_hole.get(i+1, None)

            hole_score = int(score) if score != "" else None
            par = int(pars[i]) if i < len(pars) and pars[i] != "" else None

            score_to_par = (
                hole_score - par
                if hole_score is not None and par is not None
                else None
            )

            hole_scores.append({
                "result_id": player_round["ResultID"], # unsure the difference between result id and score id
                "round_id": player_round["RoundID"], #ties to live round ID at round info level, so theoretically don't need event id
                "score_id": score_id, # score id ties to the stats for the hole score and round
                "round_number": round_number,
                "pdga_number": player_round["PDGANum"],
                "hole_number": i+1,
                "score": hole_score,
                "par": par,
                "score_to_par": score_to_par,
                #additional breakdown info we can pull in if we want
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
                "penalty": breakdown.get("penalty")
            })
        round_context.append({
            # IDs
            "result_id": player_round["ResultID"], # unsure the difference between result id and score id
            "round_id": player_round["RoundID"], #ties to live round ID at round info level - should uniquely id a round
            "score_id": player_round["ScoreID"], # unsure the difference between result id and score id
            "round_number": round_number,
            "pdga_number": player_round["PDGANum"],

            # Card Info 
            "pool": player_round["Pool"],
            "card_number": player_round["CardNum"],
            "tee_time": player_round["TeeTime"],

            #Results Info
            "rating_at_event": player_round["Rating"],
            "won_playoff": player_round["WonPlayoff"],
            "prize": player_round["Prize"],
            "previous_place": player_round["PreviousPlace"], #place after prior round
            "running_place": player_round["RunningPlace"], #place currently - after round if round is done
            "tied": player_round["Tied"], # binary for tied - true or false
            #"holes": player_round["Holes"], # number of holes in the layout
            "round_rating": player_round["RoundRating"],
            "completed": player_round["Completed"], #  binary for completed round 1 = true, 0 = false
            
            #Total Scores
            #"played": player_round["Played"], # number of holes played in the round
            "previous_round_score": player_round["PrevRndTotal"], # total score from prior round
            "grand_total": player_round["GrandTotal"], # total for the tournament so far - only updates after round ends
            "round_score": player_round["RoundScore"], #total for the round - live if in progress 
            #"sub_total": player_round["SubTotal"], # live if in progress, total for all strokes played in tournament
            "round_to_par": player_round["RoundtoPar"], # difference between round score and par
            #"par_thru_round": player_round["ParThruRound"], #running total of par thru current round
            "total_to_par": player_round["ToPar"] #what is difference between this and par thru round?
        })
        players.append({
            "pdga_number": player_round["PDGANum"],
            "full_name": player_round["Name"],
            "first_name": player_round["FirstName"],
            "last_name": player_round["LastName"],
            "home_city": player_round["City"],
            "home_state": player_round["StateProv"],
            "home_country": player_round["Country"],
            "full_location": player_round["FullLocation"]
        })
        for stat in round_stats:
            round_context_stats.append({
                "score_id": score_id,
                "stat_id": stat["statId"],
                "stat_count": stat["statCount"],
                "stat_opportunity_count:": stat["statOpportunityCount"],
                "stat_value": stat["statValue"]
            })
        
        time.sleep(0.5) # to avoid hitting api rate limits 

    return round_info, hole_scores, round_context, players, round_context_stats


payload = get_round(96410, "MPO", 1)

round_info, hole_scores, round_context, players, round_stats = parse_round(96410, "MPO", 1, payload)
print(round_info)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(hole_scores[0])
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(round_context[0])
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(players[0])
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(round_stats[0])