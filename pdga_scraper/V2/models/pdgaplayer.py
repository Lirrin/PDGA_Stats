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