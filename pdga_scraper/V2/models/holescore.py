from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class HoleScore:
    "Represents an Outcome on a Hole"
    round_id: int
    pdga_number: int
    hole_number: int

    #Core Scoring
    strokes: int
    par: int
    score_to_par: int

    def __str__(self):
        return f"{self.round_id} {self.hole_number}"
    

def to_hole_score(score:dict):
    return HoleScore(
        round_id = score["round_id"],
        pdga_number = score["pdga_number"],
        hole_number = score["hole_num"],
        strokes = score["score"],
        par = score["par"],
        score_to_par = score["score_to_par"],
    )