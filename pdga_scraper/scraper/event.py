"""
Event data scraping utilities.
"""

import logging


logger = logging.getLogger(__name__)


class EventScraper:
    """Handles scraping of event/tournament data."""

    def __init__(self, client):
        """Initialize event scraper with a client."""
        self.client = client

    def scrape_events(self):
        """Scrape all available events."""
        raise NotImplementedError("Method not yet implemented")

    def scrape_event_details(self, event_id):
        """Scrape details for a specific event."""
        raise NotImplementedError("Method not yet implemented")
