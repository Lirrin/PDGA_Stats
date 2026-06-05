"""Storage module for writing scraped data.

This layer accepts model objects from the scraper layer
and persists them to various formats (SQLite, CSV, Parquet).
"""

from .sqlite_writer import SQLiteWriter
from .csv_writer import CSVWriter
from .parquet_writer import ParquetWriter

__all__ = [
    "SQLiteWriter",
    "CSVWriter",
    "ParquetWriter",
]
