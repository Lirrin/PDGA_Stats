"""
Round/score data model.
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Round:
    """Represents a round/score in a tournament event."""

    id: int
    event_id: int
    player_id: int
    round_number: int
    score: int
    date: datetime
    course: Optional[str] = None
    notes: Optional[str] = None

    def __str__(self):
        return f"Round {self.round_number}: {self.score} ({self.player_id})"
