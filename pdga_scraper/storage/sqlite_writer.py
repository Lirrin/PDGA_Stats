"""
SQLite database writer for scraped data.

This storage layer accepts model objects from the scraper layer
and persists them to SQLite.
"""

import logging
import sqlite3
from typing import List

from ..models import Event, Player, Round, RoundScore, HoleScore


logger = logging.getLogger(__name__)



class SQLiteWriter:
    """Writes scraped model objects to SQLite database."""

    def __init__(self, db_path: str = "output/pdga_data.db"):
        """Initialize SQLite writer.
        
        Args:
            db_path: Path to SQLite database file.
        """
        self.db_path = db_path
        logger.info(f"Initialized SQLiteWriter with database: {db_path}")

    def create_tables(self):
        """Create database tables for events, players, scores, and hole scores."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    location TEXT,
                    date_start TEXT,
                    date_end TEXT,
                    course TEXT,
                    level TEXT,
                    division TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Players table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    pdga_number TEXT,
                    rating REAL,
                    division TEXT,
                    country TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Rounds/Scores table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS round_scores (
                    id INTEGER PRIMARY KEY,
                    player_id INTEGER NOT NULL,
                    event_id INTEGER NOT NULL,
                    round_number INTEGER NOT NULL,
                    total_score INTEGER,
                    total_par INTEGER,
                    placement INTEGER,
                    tournament_placement INTEGER,
                    thru_holes INTEGER,
                    timestamp TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (player_id) REFERENCES players(id),
                    FOREIGN KEY (event_id) REFERENCES events(id),
                    UNIQUE(player_id, event_id, round_number)
                )
            """)
            
            # Hole scores table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hole_scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hole_number INTEGER NOT NULL,
                    score INTEGER NOT NULL,
                    par INTEGER NOT NULL,
                    player_id INTEGER NOT NULL,
                    event_id INTEGER NOT NULL,
                    round_number INTEGER NOT NULL,
                    thru_round INTEGER,
                    placement INTEGER,
                    distance_to_leader INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (player_id) REFERENCES players(id),
                    FOREIGN KEY (event_id) REFERENCES events(id)
                )
            """)
            
            conn.commit()
            logger.info("Successfully created tables")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            raise
        finally:
            conn.close()

    def save_event(self, event: Event) -> None:
        """Save an event to the database.
        
        Args:
            event: Event model object to save
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO events
                (id, name, location, date_start, date_end, course, level, division)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event.id,
                event.name,
                event.location,
                event.date_start.isoformat() if event.date_start else None,
                event.date_end.isoformat() if event.date_end else None,
                event.course,
                event.level,
                event.division,
            ))
            conn.commit()
            logger.info(f"Saved event {event.id}: {event.name}")
        except sqlite3.Error as e:
            logger.error(f"Error saving event {event.id}: {e}")
            raise
        finally:
            conn.close()

    def save_events(self, events: List[Event]) -> None:
        """Save multiple events to the database.
        
        Args:
            events: List of Event model objects to save
        """
        for event in events:
            self.save_event(event)

    def save_player(self, player: Player) -> None:
        """Save a player to the database.
        
        Args:
            player: Player model object to save
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO players
                (id, name, pdga_number, rating, division, country)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                player.id,
                player.name,
                player.pdga_number,
                player.rating,
                player.division,
                player.country,
            ))
            conn.commit()
            logger.info(f"Saved player {player.id}: {player.name}")
        except sqlite3.Error as e:
            logger.error(f"Error saving player {player.id}: {e}")
            raise
        finally:
            conn.close()

    def save_players(self, players: List[Player]) -> None:
        """Save multiple players to the database.
        
        Args:
            players: List of Player model objects to save
        """
        for player in players:
            self.save_player(player)

    def save_round_score(self, round_score: RoundScore) -> None:
        """Save a round score to the database.
        
        Args:
            round_score: RoundScore model object to save
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO round_scores
                (id, player_id, event_id, round_number, total_score, total_par,
                 placement, tournament_placement, thru_holes, timestamp, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                round_score.id,
                round_score.player_id,
                round_score.event_id,
                round_score.round_number,
                round_score.total_score,
                round_score.total_par,
                round_score.placement,
                round_score.tournament_placement,
                round_score.thru_holes,
                round_score.timestamp.isoformat() if round_score.timestamp else None,
                round_score.notes,
            ))
            conn.commit()
            logger.info(f"Saved round score for player {round_score.player_id}, round {round_score.round_number}")
        except sqlite3.Error as e:
            logger.error(f"Error saving round score: {e}")
            raise
        finally:
            conn.close()

    def save_round_scores(self, round_scores: List[RoundScore]) -> None:
        """Save multiple round scores to the database.
        
        Args:
            round_scores: List of RoundScore model objects to save
        """
        for round_score in round_scores:
            self.save_round_score(round_score)

    def save_hole_score(self, hole_score: HoleScore) -> None:
        """Save a hole score to the database.
        
        Args:
            hole_score: HoleScore model object to save
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO hole_scores
                (hole_number, score, par, player_id, event_id, round_number,
                 thru_round, placement, distance_to_leader)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                hole_score.hole_number,
                hole_score.score,
                hole_score.par,
                hole_score.player_id,
                hole_score.event_id,
                hole_score.round_number,
                hole_score.thru_round,
                hole_score.placement,
                hole_score.distance_to_leader,
            ))
            conn.commit()
            logger.debug(f"Saved hole {hole_score.hole_number} for player {hole_score.player_id}")
        except sqlite3.Error as e:
            logger.error(f"Error saving hole score: {e}")
            raise
        finally:
            conn.close()

    def save_hole_scores(self, hole_scores: List[HoleScore]) -> None:
        """Save multiple hole scores to the database.
        
        Args:
            hole_scores: List of HoleScore model objects to save
        """
        for hole_score in hole_scores:
            self.save_hole_score(hole_score)

