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
