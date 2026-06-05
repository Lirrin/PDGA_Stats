import requests

def get_round(event_id, division, round_number):
    url = "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_round"
    
    params = {
        "TournID": event_id,
        "Division": division,
        "Round": round_number
    }
    
    return requests.get(url, params=params).json()

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
    for player_round in data["scores"]:
        pars = player_round.get("Pars", "").split(",")
        for i, score in enumerate(player_round.get("HoleScores", [])):

            hole_scores.append({
                "result_id": player_round["ResultID"], # unsure the difference between result id and score id
                "round_id": player_round["RoundID"], #ties to live round ID at round info level, so theoretically don't need event id
                "score_id": player_round["ScoreID"], # unsure the difference between result id and score id
                "round_number": round_number,
                "pdga_number": player_round["PDGANum"],
                "hole_number": i+1,
                "score": int(score) if score != "" else None,
                "par": int(pars[i]) if i < len(pars) else None,
                "score_to_par": int(score) - int(pars[i]) if score != "" and i < len(pars) else None
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



    return round_info, hole_scores, round_context, players


payload = get_round(96410, "MPO", 1)

round_info, hole_scores, round_context, players = parse_round(96410, "MPO", 1, payload)
print(round_info)
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(hole_scores[0])
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(round_context[0])
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(players[0])
