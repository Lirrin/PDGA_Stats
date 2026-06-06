from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class HoleScore:
    "Represents a Score on a Hole"



    def __str__(self):
        return f"{self.score_id} {self.hole_number}"