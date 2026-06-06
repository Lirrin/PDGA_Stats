from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class TournamentPlayer:
    "Represents a Player Entry in a Tournament"
    event_id: int
    pdga_number: int
    rating_at_event: int
    won_playoff: bool
    prize: str
    total_strokes: int


    def __str__(self):
        return f"{self.event_id} {self.pdga_number}"