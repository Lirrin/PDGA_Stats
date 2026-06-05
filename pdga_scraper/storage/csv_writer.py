"""
CSV writer for exporting scraped data.

This storage layer accepts model objects from the scraper layer
and exports them to CSV files.
"""

import logging
import csv
from typing import List, Dict, Any
from pathlib import Path
from dataclasses import asdict

from ..models import Event, Player, RoundScore, HoleScore


logger = logging.getLogger(__name__)



class CSVWriter:
    """Writes scraped model objects to CSV files."""

    def __init__(self, output_dir: str = "output/csv"):
        """Initialize CSV writer.
        
        Args:
            output_dir: Directory to write CSV files to.
        """
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized CSVWriter with output directory: {output_dir}")

    def save_events(self, events: List[Event], filename: str = "events.csv") -> None:
        """Save events to CSV file.
        
        Args:
            events: List of Event model objects
            filename: Name of the output CSV file
        """
        if not events:
            logger.info("No events to write to CSV")
            return
        
        out_path = Path(self.output_dir) / filename
        
        # Convert dataclass to dict
        rows = []
        for event in events:
            row = asdict(event)
            # Convert datetime objects to ISO format strings
            if row.get("date_start"):
                row["date_start"] = row["date_start"].isoformat() if row["date_start"] else None
            if row.get("date_end"):
                row["date_end"] = row["date_end"].isoformat() if row["date_end"] else None
            rows.append(row)
        
        fieldnames = sorted(set().union(*(r.keys() for r in rows)))
        
        with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        logger.info(f"Wrote {len(events)} events to {out_path}")

    def save_players(self, players: List[Player], filename: str = "players.csv") -> None:
        """Save players to CSV file.
        
        Args:
            players: List of Player model objects
            filename: Name of the output CSV file
        """
        if not players:
            logger.info("No players to write to CSV")
            return
        
        out_path = Path(self.output_dir) / filename
        
        rows = [asdict(player) for player in players]
        fieldnames = sorted(set().union(*(r.keys() for r in rows)))
        
        with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        logger.info(f"Wrote {len(players)} players to {out_path}")

    def save_round_scores(self, round_scores: List[RoundScore], filename: str = "round_scores.csv") -> None:
        """Save round scores to CSV file.
        
        Args:
            round_scores: List of RoundScore model objects
            filename: Name of the output CSV file
        """
        if not round_scores:
            logger.info("No round scores to write to CSV")
            return
        
        out_path = Path(self.output_dir) / filename
        
        rows = []
        for rs in round_scores:
            row = asdict(rs)
            # Remove nested hole_scores for CSV export
            row.pop("hole_scores", None)
            if row.get("timestamp"):
                row["timestamp"] = row["timestamp"].isoformat() if row["timestamp"] else None
            rows.append(row)
        
        fieldnames = sorted(set().union(*(r.keys() for r in rows)))
        
        with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        logger.info(f"Wrote {len(round_scores)} round scores to {out_path}")

    def save_hole_scores(self, hole_scores: List[HoleScore], filename: str = "hole_scores.csv") -> None:
        """Save hole scores to CSV file.
        
        Args:
            hole_scores: List of HoleScore model objects
            filename: Name of the output CSV file
        """
        if not hole_scores:
            logger.info("No hole scores to write to CSV")
            return
        
        out_path = Path(self.output_dir) / filename
        
        rows = [asdict(hs) for hs in hole_scores]
        fieldnames = sorted(set().union(*(r.keys() for r in rows)))
        
        with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        logger.info(f"Wrote {len(hole_scores)} hole scores to {out_path}")

