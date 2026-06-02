"""
Main entry point for PDGA Scraper application.
"""

import logging
from scraper.client import PDGAClient
from storage.csv_writer import CSVWriter
from storage.sqlite_writer import SQLiteWriter
from storage.parquet_writer import ParquetWriter


logger = logging.getLogger(__name__)


def main():
    """Main execution function."""
    logger.info("Starting PDGA Scraper...")
    # TODO: Add scraping logic here


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/pdga_scraper.log'),
            logging.StreamHandler()
        ]
    )
    main()
