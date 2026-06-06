from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class PlayerRound:
    "Represents a Player's Round in a Tournament"
    result_id: int
    round_id: int
    score_id: int

    # Round identity
    round_code: int
    round_number: int
    is_playoff: bool

    # Context / grouping
    pool: Optional[str]
    card_number: int
    tee_time: Optional[str]

    # Placement
    previous_place: Optional[int]
    post_place: int
    tied: bool

    # Performance metrics
    round_rating: int
    is_complete: bool

    previous_total_score: int
    round_score: int
    post_total_score: int

    round_to_par: int
    total_to_par: int

    def __str__(self):
        return f"{self.round_id} {self.round_num}"