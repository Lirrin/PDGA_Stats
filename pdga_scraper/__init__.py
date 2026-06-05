"""
PDGA Scraper - Clean architecture for fetching PDGA tournament data.

This package provides:
- scraper/ - Orchestration layer for data collection
- models/ - Domain objects representing PDGA data
- storage/ - Persistence layer for multiple formats
- client/ - HTTP client for PDGA Live API

Example:
    from pdga_scraper.scraper import scrape_event
    from pdga_scraper.storage import SQLiteWriter
    
    event, scores, players = scrape_event(59876)
    db = SQLiteWriter("pdga_data.db")
    db.create_tables()
    db.save_event(event)
    db.save_players(players)
    db.save_round_scores(scores)
"""

__version__ = "0.1.0"
__author__ = "PDGA Scraper Contributors"
