"""
CSV writer for exporting scraped data.
"""

import logging
import csv
from typing import List, Dict, Any
import json
from pathlib import Path


logger = logging.getLogger(__name__)


class CSVWriter:
    """Writes scraped data to CSV files."""

    def __init__(self, output_dir: str = "output/csv"):
        """Initialize CSV writer.
        
        Args:
            output_dir: Directory to write CSV files to.
        """
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized CSVWriter with output directory: {output_dir}")

    def write_events(self, events: List[Dict[str, Any]], filename: str = "events.csv"):
        """Write events data to CSV."""
        # If events are complex or deeply nested, write a JSON lines file instead
        out_path = Path(self.output_dir) / filename
        # If filename ends with .jsonl or .ndjson, write JSON lines
        if out_path.suffix in (".jsonl", ".ndjson"):
            with out_path.open("a", encoding="utf-8") as fh:
                for ev in events:
                    fh.write(json.dumps(ev, default=str) + "\n")
            logger.info("Wrote %d events to %s", len(events), out_path)
            return

        # Otherwise, attempt to flatten top-level keys and write CSV
        if not events:
            logger.info("No events to write to CSV")
            return

        # Determine fieldnames from union of top-level keys
        fieldnames = set()
        for ev in events:
            fieldnames.update(ev.keys())
        fieldnames = list(sorted(fieldnames))

        with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for ev in events:
                # convert non-serializable values to string
                row = {k: (json.dumps(v, default=str) if isinstance(v, (dict, list)) else v) for k, v in ev.items()}
                writer.writerow(row)

        logger.info("Wrote %d events to %s", len(events), out_path)

    def write_players(self, players: List[Dict[str, Any]], filename: str = "players.csv"):
        """Write players data to CSV."""
        self.write_events(players, filename=filename)

    def write_rounds(self, rounds: List[Dict[str, Any]], filename: str = "rounds.csv"):
        """Write rounds/scores data to CSV."""
        self.write_events(rounds, filename=filename)
