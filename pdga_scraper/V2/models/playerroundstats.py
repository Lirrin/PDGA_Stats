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

def to_player_round_stats(rnd_stats:dict):
    return PlayerRoundStats(
        score_id = rnd_stats["score_id"],
        stat_id = rnd_stats["stat_id"],
        stat_count = rnd_stats["stat_count"],
        stat_opportunity = rnd_stats["stat_opportunity_count"],
        stat_value = rnd_stats["stat_value"]
    )