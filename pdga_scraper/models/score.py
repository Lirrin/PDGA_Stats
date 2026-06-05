"""
Score data models for holes and complete rounds.
"""

from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class HoleScore:
    """Represents a score for a single hole."""

    hole_number: int
    score: int
    par: int
    player_id: int
    event_id: int
    round_number: int
    
    # Optional additional info
    thru_round: Optional[int] = None  # Cumulative score through this hole
    placement: Optional[int] = None  # Current placement after this hole
    distance_to_leader: Optional[int] = None  # Strokes behind leader
    
    @property
    def is_eagle(self) -> bool:
        """Check if score is an eagle (2 under par)."""
        return self.score <= self.par - 2
    
    @property
    def is_birdie(self) -> bool:
        """Check if score is a birdie (1 under par)."""
        return self.score == self.par - 1
    
    @property
    def is_par(self) -> bool:
        """Check if score equals par."""
        return self.score == self.par
    
    @property
    def is_bogey(self) -> bool:
        """Check if score is a bogey (1 over par)."""
        return self.score == self.par + 1


@dataclass
class RoundScore:
    """Represents a complete round score for a player in an event."""

    id: int
    player_id: int
    event_id: int
    round_number: int
    total_score: int
    total_par: int
    
    # Additional info
    placement: Optional[int] = None
    tournament_placement: Optional[int] = None
    thru_holes: Optional[int] = None  # Number of holes completed
    timestamp: Optional[datetime] = None
    notes: Optional[str] = None
    
    # Individual hole scores (can be loaded separately)
    hole_scores: Optional[List[HoleScore]] = None
    
    @property
    def score_differential(self) -> int:
        """Calculate score relative to par."""
        return self.total_score - self.total_par
    
    @property
    def is_complete(self) -> bool:
        """Check if round is complete (18 holes)."""
        return self.thru_holes == 18 if self.thru_holes else False
