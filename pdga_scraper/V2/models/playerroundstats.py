from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from decimal import Decimal

@dataclass
class PlayerRoundStats:
    "Represents a Player Round Stats Entry"
    score_id: int
    stat_id: int
    stat_count: int
    stat_opportunity: int
    stat_value: Decimal


    def __str__(self):
        return f"{self.score_id} {self.stat_id}"

