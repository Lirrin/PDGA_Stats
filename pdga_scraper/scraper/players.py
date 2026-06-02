"""
Player data scraping utilities.
"""

import logging


logger = logging.getLogger(__name__)


class PlayersScraper:
    """Handles scraping of player data."""

    def __init__(self, client):
        """Initialize players scraper with a client."""
        self.client = client

    def scrape_players(self):
        """Scrape all available players."""
        raise NotImplementedError("Method not yet implemented")

    def scrape_player_stats(self, player_id):
        """Scrape statistics for a specific player."""
        raise NotImplementedError("Method not yet implemented")
