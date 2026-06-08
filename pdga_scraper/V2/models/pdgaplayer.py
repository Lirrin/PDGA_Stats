from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class PDGAPlayer:
    "Represents a Player"
    pdga_number: int
    full_name: str
    first_name: str
    last_name: str
    home_city: Optional[str]
    home_state: Optional[str]
    home_country: Optional[str]
    home_location: Optional[str]



    def __str__(self):
        return f"{self.pdga_number} {self.full_name}"

def to_player(player:dict):
    return PDGAPlayer(
        pdga_number= player["pdga_number"],
        full_name = player["full_name"],
        first_name = player["first_name"],
        last_name = player["last_name"],
        home_city = player["home_city"],
        home_state = player["home_state"],
        home_country = player["home_country"],
        home_location = player["full_location"]
    )