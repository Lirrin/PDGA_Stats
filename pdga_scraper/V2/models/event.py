from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Event:
    """Represents a PDGA tournament event."""

    event_id: int
    name: str
    date_range: str
    start_date: datetime
    end_date: datetime
    location: str
    location_short: str
    country: str
    name_main: str
    name_pre: str
    name_post: str
    raw_tier: str
    tier: str
    semis: str
    td_name: str
    td_pdga_number: int
    time_zone: str
    scoring_format: str
    tier_x: str

    def __str__(self):
        return f"{self.name} ({self.date_start.year})"