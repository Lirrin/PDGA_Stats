"""
Main entry point for PDGA Scraper application.

This demonstrates the clean layered architecture:
1. client.py - API layer (HTTP only, no parsing)
2. models/ - Domain layer (pure data structures)
3. scraper/ - Orchestration layer (coordinates API + parsing)
4. storage/ - Persistence layer (accepts model objects)

Example usage:
    python main.py --event 59876 --output-db pdga_data.db
"""

import logging
import argparse
from pathlib import Path

from .scraper import scrape_event
from .storage import SQLiteWriter, CSVWriter


logger = logging.getLogger(__name__)



def scrape_single_event(event_id: int, output_db: str = None, output_csv: str = None) -> bool:
    """Scrape a single event and save results to configured storage.
    
    Args:
        event_id: PDGA event ID to scrape
        output_db: Path to SQLite database for storage (optional)
        output_csv: Path to CSV output directory (optional)
        
    Returns:
        True if successful, False if failed
    """
    try:
        logger.info(f"=" * 70)
        logger.info(f"Scraping event {event_id}")
        logger.info(f"=" * 70)
        
        # ====================================================================
        # ORCHESTRATION LAYER: Call scraper functions (no HTTP, no storage)
        # ====================================================================
        event, round_scores, players = scrape_event(event_id)
        
        logger.info(f"Successfully scraped event: {event}")
        logger.info(f"  Players: {len(players)}")
        logger.info(f"  Scores: {len(round_scores)}")
        
        # ====================================================================
        # PERSISTENCE LAYER: Save parsed models to storage
        # ====================================================================
        
        if output_db:
            logger.info(f"Saving to SQLite: {output_db}")
            db_writer = SQLiteWriter(output_db)
            db_writer.create_tables()
            db_writer.save_event(event)
            db_writer.save_players(players)
            db_writer.save_round_scores(round_scores)
            logger.info(f"Successfully saved event data to {output_db}")
        
        if output_csv:
            logger.info(f"Saving to CSV: {output_csv}")
            csv_writer = CSVWriter(output_csv)
            csv_writer.save_events([event])
            csv_writer.save_players(players)
            csv_writer.save_round_scores(round_scores)
            logger.info(f"Successfully saved event data to {output_csv}")
        
        logger.info(f"Event {event_id} completed successfully\n")
        return True
        
    except Exception as e:
        logger.exception(f"Failed to scrape event {event_id}: {e}")
        return False


def scrape_batch_events(event_ids: list, output_db: str = None, output_csv: str = None) -> dict:
    """Scrape multiple events with individual error handling.
    
    This ensures that if one event fails, processing continues with the next.
    
    Args:
        event_ids: List of PDGA event IDs
        output_db: Path to SQLite database for storage (optional)
        output_csv: Path to CSV output directory (optional)
        
    Returns:
        Dict with success/failure counts and details
    """
    results = {
        "total": len(event_ids),
        "succeeded": 0,
        "failed": 0,
        "failed_events": [],
    }
    
    for event_id in event_ids:
        if scrape_single_event(event_id, output_db, output_csv):
            results["succeeded"] += 1
        else:
            results["failed"] += 1
            results["failed_events"].append(event_id)
    
    return results


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description="PDGA Scraper - Fetch tournament data from PDGA Live API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape single event to SQLite database
  python main.py --event 59876 --db pdga_data.db
  
  # Scrape to CSV files
  python main.py --event 59876 --csv output/csv
  
  # Scrape multiple events
  python main.py --events 59876 59877 59878 --db pdga_data.db --csv output/csv
        """,
    )
    
    parser.add_argument(
        "--event",
        type=int,
        help="Single PDGA event ID to scrape",
    )
    parser.add_argument(
        "--events",
        type=int,
        nargs="+",
        help="Multiple PDGA event IDs to scrape",
    )
    parser.add_argument(
        "--db",
        type=str,
        default=None,
        help="SQLite database path for storing results (optional)",
    )
    parser.add_argument(
        "--csv",
        type=str,
        default=None,
        help="CSV output directory for storing results (optional)",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level",
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("pdga_scraper.log"),
        ],
    )
    
    logger.info("Starting PDGA Scraper...")
    
    # Validate arguments
    if not args.event and not args.events:
        parser.print_help()
        logger.error("Must specify --event or --events")
        return 1
    
    if not args.db and not args.csv:
        logger.warning("No output specified. Data will be processed but not saved.")
    
    # Determine events to scrape
    event_ids = []
    if args.event:
        event_ids = [args.event]
    elif args.events:
        event_ids = args.events
    
    # Scrape events
    if len(event_ids) == 1:
        success = scrape_single_event(event_ids[0], output_db=args.db, output_csv=args.csv)
        return 0 if success else 1
    else:
        results = scrape_batch_events(event_ids, output_db=args.db, output_csv=args.csv)
        logger.info(f"\n" + "=" * 70)
        logger.info(f"Batch Results:")
        logger.info(f"  Total: {results['total']}")
        logger.info(f"  Succeeded: {results['succeeded']}")
        logger.info(f"  Failed: {results['failed']}")
        if results["failed_events"]:
            logger.error(f"  Failed events: {results['failed_events']}")
        logger.info(f"=" * 70)
        return 0 if results["failed"] == 0 else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())

