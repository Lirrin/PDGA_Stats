"""
Course and layout data models.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Layout:
    """Represents a specific layout of a disc golf course."""

    id: int
    name: str
    holes: int
    par: int
    distance: Optional[int] = None  # Total distance in feet
    difficulty: Optional[float] = None  # Difficulty rating


@dataclass
class Course:
    """Represents a disc golf course."""

    id: int
    name: str
    location: str
    country: Optional[str] = None
    state: Optional[str] = None
    layouts: Optional[list[Layout]] = None

    def __str__(self):
        return f"{self.name} ({self.location})"
