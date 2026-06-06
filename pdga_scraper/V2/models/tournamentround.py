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
    division: str
    pool: str
    course_id: int
    layout_id: int
    shotgun_time: str
    tee_times: str 
    is_playoff: bool


    def __str__(self):
        return f"{self.event_id} {self.round_num}"