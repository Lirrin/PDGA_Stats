from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class TournamentRound:
    "Represents a Round in a Tournament"

    event_id: int
    round_id: int
    round_code: int
    round_num: int
    division_code: str
    pool: str
    course_id: int
    layout_id: int
    is_playoff: bool


    def __str__(self):
        return f"{self.event_id} {self.round_num}"
    

def to_tournament_round(round_info:dict, round_id, round_code, round_num, playoff:bool = False):
    return TournamentRound(
        event_id = round_info["event_id"],
        round_id = round_id,
        round_code = round_code,
        round_num = round_num,
        division_code = round_info["division"],
        pool = round_info["pool"],
        course_id = round_info["course_id"],
        layout_id = round_info["layout_id"],
        is_playoff = playoff
    )