"""PDGA Scraper module - orchestration layer.

This layer coordinates API calls (client) with data parsing and storage.
"""

from .client import PDGAClient
from .event import scrape_event, scrape_round_hole_scores

__all__ = [
    "PDGAClient",
    "scrape_event",
    "scrape_round_hole_scores",
]
