"""
Player data model.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    """Represents a PDGA player."""

    id: int
    name: str
    pdga_number: str
    rating: Optional[float] = None
    division: Optional[str] = None
    country: Optional[str] = None

    def __str__(self):
        return f"{self.name} ({self.pdga_number})"
