from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EventDivision:
    "Represents the mapping of an Event to a Division" # for now don't need a division table, but we'll see

    event_id: int
    division_id: int
    division: str
    division_name: str
    players: int
    is_pro: str
    rounds_scored: int # num rounds with scores, not num of rounds in tournament - e..g playoff included


    def __str__(self):
        return f"{self.event_id} {self.division}"