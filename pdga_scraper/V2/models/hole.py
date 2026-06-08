from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Hole:
    "Represents a Hole in a layout"
    layout_id: int
    hole_number: int
    hole_par: int
    hole_length: int
    length_unit: str
    
    def __str__(self):
        return f"{self.layout_id} {self.hole_number}"


def to_hole(hole:dict):
    return Hole(
        layout_id = hole["layout_id"],
        hole_number = hole["hole_num"],
        hole_par = hole["hole_par"],
        hole_length = hole["hole_length"],
        length_unit = hole["units"]
    )