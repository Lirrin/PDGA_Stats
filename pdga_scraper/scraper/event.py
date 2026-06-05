"""
Event data scraping orchestration and parsing.

This module orchestrates the scraping workflow by:
1. Calling the PDGAClient to fetch raw JSON data
2. Parsing JSON into domain model objects
3. Coordinating the collection of events, rounds, and scores

This layer contains NO HTTP logic (that's in client.py).
This layer contains NO storage logic (that's in storage/).
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

from .client import PDGAClient
from ..models import Event, Player, Round, HoleScore, RoundScore


logger = logging.getLogger(__name__)



# ============================================================================
# PARSING FUNCTIONS: Convert raw JSON to domain models
# ============================================================================


def parse_event(event_json: Dict[str, Any]) -> Event:
    """Parse raw event JSON into an Event model.
    
    Args:
        event_json: Raw JSON response from client.get_event()
        
    Returns:
        Event model object
        
    Raises:
        KeyError: If required fields are missing from JSON
        ValueError: If data types don't match expectations
    """
    try:
        event_id = int(event_json["TournID"])
        name = event_json.get("TournName", "Unknown")
        location = event_json.get("Location", "Unknown")
        
        # Parse dates - handle various formats
        start_date_str = event_json.get("StartDate", "")
        end_date_str = event_json.get("EndDate", "")
        
        start_date = _parse_date(start_date_str)
        end_date = _parse_date(end_date_str)
        
        event = Event(
            id=event_id,
            name=name,
            location=location,
            date_start=start_date,
            date_end=end_date,
            course=event_json.get("CourseName"),
            level=event_json.get("TournLevel"),
            division=event_json.get("Division"),
        )
        return event
    except (KeyError, ValueError, TypeError) as e:
        logger.error("Failed to parse event JSON: %s\nData: %s", e, event_json)
        raise


def parse_player(player_json: Dict[str, Any]) -> Player:
    """Parse raw player JSON into a Player model.
    
    Args:
        player_json: Raw JSON for a player
        
    Returns:
        Player model object
    """
    try:
        player_id = int(player_json["PlayerID"])
        name = player_json.get("PlayerName", "Unknown")
        pdga_number = player_json.get("PDGANumber", "")
        
        player = Player(
            id=player_id,
            name=name,
            pdga_number=pdga_number,
            rating=_safe_float(player_json.get("Rating")),
            division=player_json.get("Division"),
            country=player_json.get("Country"),
        )
        return player
    except (KeyError, ValueError, TypeError) as e:
        logger.error("Failed to parse player JSON: %s", e)
        raise


def parse_hole_score(
    hole_json: Dict[str, Any], player_id: int, event_id: int, round_number: int
) -> HoleScore:
    """Parse raw hole score JSON into a HoleScore model.
    
    Args:
        hole_json: Raw JSON for a single hole score
        player_id: Player ID
        event_id: Event ID
        round_number: Round number
        
    Returns:
        HoleScore model object
    """
    try:
        hole_score = HoleScore(
            hole_number=int(hole_json.get("HoleNumber", 0)),
            score=int(hole_json.get("Score", 0)),
            par=int(hole_json.get("Par", 3)),
            player_id=player_id,
            event_id=event_id,
            round_number=round_number,
            thru_round=_safe_int(hole_json.get("ThruRound")),
            placement=_safe_int(hole_json.get("Placement")),
            distance_to_leader=_safe_int(hole_json.get("DistanceToLeader")),
        )
        return hole_score
    except (KeyError, ValueError, TypeError) as e:
        logger.error("Failed to parse hole score JSON: %s", e)
        raise


def parse_round_score(
    round_json: Dict[str, Any], event_id: int
) -> RoundScore:
    """Parse raw round score JSON into a RoundScore model.
    
    Args:
        round_json: Raw JSON for a round score
        event_id: Event ID
        
    Returns:
        RoundScore model object
    """
    try:
        round_score = RoundScore(
            id=int(round_json.get("ScoreID", 0)),
            player_id=int(round_json.get("PlayerID", 0)),
            event_id=event_id,
            round_number=int(round_json.get("RoundNumber", 0)),
            total_score=int(round_json.get("Score", 0)),
            total_par=int(round_json.get("Par", 54)),
            placement=_safe_int(round_json.get("Placement")),
            tournament_placement=_safe_int(round_json.get("TournamentPlacement")),
            thru_holes=_safe_int(round_json.get("ThruHoles")),
            timestamp=_parse_date(round_json.get("Timestamp")) if round_json.get("Timestamp") else None,
            notes=round_json.get("Notes"),
        )
        return round_score
    except (KeyError, ValueError, TypeError) as e:
        logger.error("Failed to parse round score JSON: %s", e)
        raise


# ============================================================================
# HELPER FUNCTIONS: Utility parsing functions
# ============================================================================


def _parse_date(date_str: Any) -> Optional[datetime]:
    """Safely parse date strings into datetime objects.
    
    Args:
        date_str: Date string in various possible formats
        
    Returns:
        datetime object or None if parsing fails
    """
    if not date_str:
        return None
    
    # Try common date formats
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M:%S",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(str(date_str), fmt)
        except (ValueError, TypeError):
            continue
    
    logger.warning("Could not parse date: %s", date_str)
    return None


def _safe_int(value: Any) -> Optional[int]:
    """Safely convert a value to int, returning None on failure."""
    try:
        return int(value) if value is not None else None
    except (ValueError, TypeError):
        return None


def _safe_float(value: Any) -> Optional[float]:
    """Safely convert a value to float, returning None on failure."""
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None


# ============================================================================
# ORCHESTRATION FUNCTIONS: High-level scraping workflows
# ============================================================================


def scrape_event(
    event_id: int,
    client: Optional[PDGAClient] = None,
    cookies: Optional[Dict[str, str]] = None,
) -> tuple[Event, List[RoundScore], List[Player]]:
    """Scrape all data for a single event.
    
    This is the main orchestration function that:
    1. Fetches event details
    2. Fetches all player scores
    3. Returns parsed model objects
    
    Args:
        event_id: PDGA event ID
        client: PDGAClient instance. Creates one if not provided.
        cookies: Optional cookies for API requests
        
    Returns:
        Tuple of (Event, list[RoundScore], list[Player])
        
    Raises:
        Exception: If API calls fail or parsing fails
    """
    if client is None:
        client = PDGAClient()
    
    logger.info("Starting to scrape event %s", event_id)
    
    try:
        # Fetch and parse event details
        logger.debug("Fetching event details for event %s", event_id)
        event_json = client.get_event(event_id, cookies=cookies)
        event = parse_event(event_json)
        logger.info("Parsed event: %s", event)
        
        # Fetch and parse round scores (all rounds for all players)
        logger.debug("Fetching round scores for event %s", event_id)
        scores_json = client.get_event_rounds(event_id, cookies=cookies)
        round_scores, players = _parse_round_scores_and_players(scores_json, event_id)
        logger.info("Parsed %d round scores and %d players", len(round_scores), len(players))
        
        return event, round_scores, players
        
    except Exception as e:
        logger.exception("Failed to scrape event %s: %s", event_id, e)
        raise


def scrape_round_hole_scores(
    event_id: int,
    round_number: int,
    client: Optional[PDGAClient] = None,
    cookies: Optional[Dict[str, str]] = None,
) -> List[HoleScore]:
    """Scrape hole-by-hole scores for a specific round.
    
    Args:
        event_id: PDGA event ID
        round_number: Round number/index
        client: PDGAClient instance. Creates one if not provided.
        cookies: Optional cookies for API requests
        
    Returns:
        List of HoleScore objects
    """
    if client is None:
        client = PDGAClient()
    
    logger.info("Scraping hole scores for event %s round %s", event_id, round_number)
    
    try:
        scores_json = client.get_round_scores(event_id, round_number, cookies=cookies)
        hole_scores = _parse_hole_scores_from_round(scores_json, event_id, round_number)
        logger.info("Parsed %d hole scores", len(hole_scores))
        return hole_scores
    except Exception as e:
        logger.exception("Failed to scrape round %s hole scores for event %s", round_number, event_id)
        raise


# ============================================================================
# INTERNAL PARSING HELPERS: Complex data structure parsing
# ============================================================================


def _parse_round_scores_and_players(
    scores_json: Dict[str, Any], event_id: int
) -> tuple[List[RoundScore], List[Player]]:
    """Parse round scores and players from round results JSON.
    
    This handles the complex JSON structure returned by get_event_rounds.
    
    Args:
        scores_json: Raw JSON response from client.get_event_rounds()
        event_id: Event ID
        
    Returns:
        Tuple of (list[RoundScore], list[Player])
    """
    round_scores: List[RoundScore] = []
    players_map: Dict[int, Player] = {}
    
    # Parse scorecards or results array
    results = scores_json.get("results", [])
    for result in results:
        try:
            # Create player if we haven't seen them
            player_id = int(result.get("PlayerID", 0))
            if player_id not in players_map:
                player = parse_player(result)
                players_map[player_id] = player
            
            # Parse each round score entry
            round_score = parse_round_score(result, event_id)
            round_scores.append(round_score)
            
        except Exception as e:
            logger.warning("Failed to parse a round score entry: %s", e)
            continue
    
    return round_scores, list(players_map.values())


def _parse_hole_scores_from_round(
    round_json: Dict[str, Any], event_id: int, round_number: int
) -> List[HoleScore]:
    """Parse hole-by-hole scores from a round details JSON.
    
    Args:
        round_json: Raw JSON response from client.get_round_scores()
        event_id: Event ID
        round_number: Round number
        
    Returns:
        List of HoleScore objects
    """
    hole_scores: List[HoleScore] = []
    
    # Parse holes array
    holes = round_json.get("holes", [])
    for hole_data in holes:
        try:
            player_id = int(hole_data.get("PlayerID", 0))
            hole_score = parse_hole_score(hole_data, player_id, event_id, round_number)
            hole_scores.append(hole_score)
        except Exception as e:
            logger.warning("Failed to parse a hole score: %s", e)
            continue
    
    return hole_scores


