from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class HoleScore:
    "Represents an Outcome on a Hole"
    #result_id: int
    round_id: int
    #score_id: int
    pdga_number: int
    hole_number: int

    #Core Scoring
    strokes: int
    par: int
    score_to_par: int

    #Hole Stats
    driving_landing_zone: str
    scramble: Optional[bool]
    green_regulation_zone: Optional[str] #can maybe use to derive fairway hits on par 4/5 2nd throws

    c1x_putts: Optional[int]
    c1_putts: Optional[int]
    c2_putts: Optional[int]

    made_distance: Optional[int]
    ob_strokes: Optional[int]
    hazard_strokes: Optional[int]
    missed_mando_strokes: Optional[int]
    lost_disc_strokes: Optional[int] 
    penalty_strokes: Optional[int]


    def __str__(self):
        return f"{self.score_id} {self.hole_number}"