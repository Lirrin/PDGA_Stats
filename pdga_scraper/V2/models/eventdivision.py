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
    
def to_event_division(division:dict):
    return EventDivision(
        event_id = division["event_id"],
        division_id = division["division_id"],
        division_code = division["division"],
        division_name = division["division_name"],
        player_count = int(division["players"]) if division["players"] != "" else None,
        is_pro = division["is_pro"],
        final_round_code = division["final_round"]
    )