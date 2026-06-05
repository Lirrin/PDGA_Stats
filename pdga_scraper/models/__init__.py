"""
Domain models for PDGA data.

These are pure data structures with no parsing or API logic.
Models can be used independently in notebooks and analytics workflows.
"""

from .event import Event
from .player import Player
from .round import Round
from .course import Course, Layout
from .score import HoleScore, RoundScore

__all__ = [
    "Event",
    "Player",
    "Round",
    "Course",
    "Layout",
    "HoleScore",
    "RoundScore",
]
