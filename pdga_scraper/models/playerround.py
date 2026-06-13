from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class PlayerRound:
    "Represents a Player's Round in a Tournament"
    #result_id: int
    round_id: int
    score_id: int
    pdga_number: int

    # Round identity
    #round_code: int
    round_number: int
    is_playoff: bool

    # Context / grouping
    pool: Optional[str]
    card_number: int
    tee_time: Optional[str]

    # Placement
    place_before_round: Optional[int]
    place_after_round: int
    is_tied: bool

    # Performance metrics
    round_rating: int
    is_complete: bool

    total_score_before_round: int
    round_score: int
    total_score_after_round: int

    round_to_par: int
    to_par_after_round: int

    def __str__(self):
        return f"{self.round_id} {self.round_num}"
    

def to_player_round(context:dict, round_number:int, playoff:bool = False):
    return PlayerRound(
        round_id = context["round_id"],
        score_id = context["score_id"],
        pdga_number = context["pdga_number"],
        #round_code = round["round_code"],
        round_number = context["round_number"],
        is_playoff = playoff,
        pool = context["pool"],
        card_number = context["card_number"],
        tee_time = context["tee_time"],
        place_before_round = context["previous_place"] if round_number > 1 else None,
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