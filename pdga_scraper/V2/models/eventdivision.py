from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class EventDivision:
    "Represents the mapping of an Event to a Division" # for now don't need a division table, but we'll see
    event_id: int
    division_id: int
    division_code: str
    division_name: str
    player_count: int
    is_pro: bool
    final_round_code: int


    def __str__(self):
        return f"{self.event_id} {self.division}"