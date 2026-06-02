"""
Rounds/scores data scraping utilities.
"""

import logging


logger = logging.getLogger(__name__)


class RoundsScraper:
    """Handles scraping of tournament round and score data."""

    def __init__(self, client):
        """Initialize rounds scraper with a client."""
        self.client = client

    def scrape_rounds(self, event_id):
        """Scrape all rounds for a specific event."""
        raise NotImplementedError("Method not yet implemented")

    def scrape_round_details(self, event_id, round_number):
        """Scrape details for a specific round."""
        raise NotImplementedError("Method not yet implemented")
