from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EventPlayer:
    "Represents a Player Entry in an Event"
    event_id: int
    pdga_number: int
    player_rating_at_event: int
    won_playoff: bool
    prize: str
    total_strokes: int


    def __str__(self):
        return f"{self.event_id} {self.pdga_number}"