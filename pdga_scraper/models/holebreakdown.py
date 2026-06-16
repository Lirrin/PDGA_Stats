from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class HoleBreakdown:
    "Represents stats for a hole"
    score_id: int
    hole_sequence: int

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
    

def to_hole_breakdown(score:dict):
    return HoleBreakdown(
        score_id = score["score_id"],
        #pdga_number = score["pdga_number"],
        hole_sequence = score["hole_number"],
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