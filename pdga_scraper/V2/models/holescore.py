from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class HoleScore:
    "Represents a Score on a Hole"
    result_id: int
    round_id: int
    score_id: int

    pdga_number: int
    hole_number: int

    strokes: int
    par: int
    score_to_par: int

    driving: str
    scramble: Optional[str]
    green: Optional[str]

    c1x: Optional[int]
    c1: Optional[int]
    c2: Optional[int]

    throw_in: Optional[int]
    ob: Optional[int]
    hazard: Optional[int]
    missed_mando: Optional[int]
    lost_disc: Optional[int]
    penalty: Optional[int]


    def __str__(self):
        return f"{self.score_id} {self.hole_number}"