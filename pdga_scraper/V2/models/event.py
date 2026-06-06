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
    #date_range: str
    start_date: datetime
    end_date: datetime
    location_full: str
    location_short: str
    country: str

    tier_code: str
    tier_name: str
    #semis: str
    td_name: str
    td_pdga_number: int
    time_zone: str
    scoring_format: str
    is_x_tier: bool

    def __str__(self):
        return f"{self.name} ({self.date_start.year})"