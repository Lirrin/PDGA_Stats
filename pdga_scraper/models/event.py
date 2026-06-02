"""
Event data model.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Event:
    """Represents a PDGA tournament event."""

    id: int
    name: str
    location: str
    date_start: datetime
    date_end: datetime
    course: Optional[str] = None
    level: Optional[str] = None
    division: Optional[str] = None

    def __str__(self):
        return f"{self.name} ({self.date_start.year})"
