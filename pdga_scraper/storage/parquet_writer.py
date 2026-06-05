"""
Parquet format writer for scraped data.

This storage layer accepts model objects from the scraper layer
and exports them to Parquet files (requires pandas and pyarrow).
"""

import logging
from typing import List
from pathlib import Path
from dataclasses import asdict

from ..models import Event, Player, RoundScore, HoleScore


logger = logging.getLogger(__name__)



class ParquetWriter:
    """Writes scraped model objects to Parquet files."""

    def __init__(self, output_dir: str = "output/parquet"):
        """Initialize Parquet writer.
        
        Args:
            output_dir: Directory to write Parquet files to.
        """
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        logger.info(f"Initialized ParquetWriter with output directory: {output_dir}")
        
        try:
            import pandas as pd
            self.pd = pd
        except ImportError:
            logger.error("pandas is required for ParquetWriter. Install with: pip install pandas pyarrow")
            self.pd = None

    def save_events(self, events: List[Event], filename: str = "events.parquet") -> None:
        """Save events to Parquet file.
        
        Args:
            events: List of Event model objects
            filename: Name of the output Parquet file
        """
        if self.pd is None:
            raise RuntimeError("pandas is not installed")
        
        if not events:
            logger.info("No events to write to Parquet")
            return
        
        rows = []
        for event in events:
            row = asdict(event)
            # Convert datetime objects to ISO format strings
            if row.get("date_start"):
                row["date_start"] = row["date_start"].isoformat() if row["date_start"] else None
            if row.get("date_end"):
                row["date_end"] = row["date_end"].isoformat() if row["date_end"] else None
            rows.append(row)
        
        df = self.pd.DataFrame(rows)
        out_path = Path(self.output_dir) / filename
        df.to_parquet(str(out_path), index=False)
        logger.info(f"Wrote {len(events)} events to {out_path}")

    def save_players(self, players: List[Player], filename: str = "players.parquet") -> None:
        """Save players to Parquet file.
        
        Args:
            players: List of Player model objects
            filename: Name of the output Parquet file
        """
        if self.pd is None:
            raise RuntimeError("pandas is not installed")
        
        if not players:
            logger.info("No players to write to Parquet")
            return
        
        rows = [asdict(player) for player in players]
        df = self.pd.DataFrame(rows)
        out_path = Path(self.output_dir) / filename
        df.to_parquet(str(out_path), index=False)
        logger.info(f"Wrote {len(players)} players to {out_path}")

    def save_round_scores(self, round_scores: List[RoundScore], filename: str = "round_scores.parquet") -> None:
        """Save round scores to Parquet file.
        
        Args:
            round_scores: List of RoundScore model objects
            filename: Name of the output Parquet file
        """
        if self.pd is None:
            raise RuntimeError("pandas is not installed")
        
        if not round_scores:
            logger.info("No round scores to write to Parquet")
            return
        
        rows = []
        for rs in round_scores:
            row = asdict(rs)
            # Remove nested hole_scores for Parquet export
            row.pop("hole_scores", None)
            if row.get("timestamp"):
                row["timestamp"] = row["timestamp"].isoformat() if row["timestamp"] else None
            rows.append(row)
        
        df = self.pd.DataFrame(rows)
        out_path = Path(self.output_dir) / filename
        df.to_parquet(str(out_path), index=False)
        logger.info(f"Wrote {len(round_scores)} round scores to {out_path}")

    def save_hole_scores(self, hole_scores: List[HoleScore], filename: str = "hole_scores.parquet") -> None:
        """Save hole scores to Parquet file.
        
        Args:
            hole_scores: List of HoleScore model objects
            filename: Name of the output Parquet file
        """
        if self.pd is None:
            raise RuntimeError("pandas is not installed")
        
        if not hole_scores:
            logger.info("No hole scores to write to Parquet")
            return
        
        rows = [asdict(hs) for hs in hole_scores]
        df = self.pd.DataFrame(rows)
        out_path = Path(self.output_dir) / filename
        df.to_parquet(str(out_path), index=False)
        logger.info(f"Wrote {len(hole_scores)} hole scores to {out_path}")

