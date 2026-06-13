from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Event:
    """Represents a PDGA tournament event."""

    event_id: int
    name: str
    name_main: Optional[str]
    name_pre: Optional[str]
    name_post: Optional[str]
    start_date: datetime
    end_date: datetime
    location_full: str
    location_short: str
    country: str

    tier_code: str
    tier_name: str
    td_name: str
    td_pdga_number: int
    time_zone: str
    scoring_format: str
    is_x_tier: bool

    def __str__(self):
        return f"{self.name} ({self.date_start.year})"
    

def to_event(event_data:dict):
    return Event(
        event_id= event_data["event_id"],
        name=event_data["name"],
        #date_range=event_data["date_range"],
        start_date=event_data["start_date"],
        end_date=event_data["end_date"],
        location_full=event_data["location"],
        location_short=event_data["location_short"],
        country=event_data["country"],
        name_main=event_data["name_main"],
        name_pre=event_data["name_pre"],
        name_post=event_data["name_post"],
        tier_code=event_data["raw_tier"],
        tier_name=event_data["tier"],
        td_name=event_data["td_name"],
        td_pdga_number=event_data["td_pdga_number"],
        time_zone=event_data["timezone"],
        scoring_format=event_data["scoring_format"],
        is_x_tier=event_data["tier_x"],
    )