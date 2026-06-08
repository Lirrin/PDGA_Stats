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
    

def to_hole_score(score:dict):
    return HoleScore(
        round_id = score["round_id"],
        pdga_number = score["pdga_number"],
        hole_number = score["hole_num"],
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