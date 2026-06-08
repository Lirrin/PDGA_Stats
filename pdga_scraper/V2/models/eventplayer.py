from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EventPlayer:
    "Represents a Player Entry in an Event"
    event_id: int
    division: str
    pdga_number: int
    player_rating_at_event: int
    won_playoff: bool
    prize: str
    total_strokes: int


    def __str__(self):
        return f"{self.event_id} {self.pdga_number}"
    
def to_event_player(player_round:dict):
    return EventPlayer(
        event_id = player_round["event_id"],
        division = player_round["division"],
        pdga_number = player_round["pdga_num"], 
        player_rating_at_event = player_round["rating_at_event"],
        won_playoff = player_round["won_playoff"],
        prize = player_round["prize"],
        total_strokes = player_round["grand_total"]
    )
