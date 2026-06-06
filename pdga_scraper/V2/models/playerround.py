from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class PlayerRound:
    "Represents a Player's Round in a Tournament"
    #result_id: int
    round_id: int
    score_id: int
    pdga_number: int

    # Round identity
    round_code: int
    round_number: int
    is_playoff: bool

    # Context / grouping
    pool: Optional[str]
    card_number: int
    tee_time: Optional[str]

    # Placement
    place_before_round: Optional[int]
    place_after_round: int
    is_tied: bool

    # Performance metrics
    round_rating: int
    is_complete: bool

    total_score_before_round: int
    round_score: int
    total_score_after_round: int

    round_to_par: int
    to_par_after_round: int

    def __str__(self):
        return f"{self.round_id} {self.round_num}"