"""
PDGA API client for fetching tournament and player data.

This layer is responsible ONLY for HTTP communication with the PDGA Live API.
It returns raw JSON responses without any parsing or transformation.
"""

import logging
from typing import Any, Dict, Optional

import requests


logger = logging.getLogger(__name__)


DEFAULT_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
    ),
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

BASE_URL = "https://www.pdga.com/apps/tournament/live-api"


class PDGAClient:
    """Client for making HTTP requests to PDGA Live API.
    
    This client handles:
    - HTTP session management
    - Default headers and user agent
    - Request retries and error handling
    - Rate limiting
    
    Examples:
        client = PDGAClient()
        event_json = client.get_event(59876)  # Returns raw JSON dict
        rounds_json = client.get_event_rounds(59876)
    """

    def __init__(self, session: Optional[requests.Session] = None, timeout: int = 20):
        """Initialize the PDGA client.
        
        Args:
            session: Optional requests.Session. If not provided, creates a new one.
            timeout: Request timeout in seconds (default: 20).
        """
        self.session = session or requests.Session()
        self.session.headers.update(DEFAULT_HEADERS)
        self.timeout = timeout
        logger.info("Initializing PDGAClient")

    def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        cookies: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make an HTTP GET request to the PDGA API.
        
        Args:
            endpoint: The API endpoint path (e.g., "live_results_fetch_event")
            params: Query parameters to send with the request
            cookies: Optional cookies to include
            
        Returns:
            Parsed JSON response as a dict
            
        Raises:
            requests.HTTPError: On non-2xx responses
            ValueError: If response is not valid JSON
        """
        url = f"{BASE_URL}/{endpoint}"
        resp = self.session.get(url, params=params, cookies=cookies, timeout=self.timeout)
        resp.raise_for_status()
        
        try:
            return resp.json()
        except ValueError as e:
            logger.exception("Failed to parse JSON response from %s: %s", url, resp.text)
            raise ValueError(f"Invalid JSON response from {url}") from e

    def get_event(self, event_id: int, cookies: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Fetch event details from the PDGA Live API.
        
        Args:
            event_id: PDGA tournament/event ID (TournID)
            cookies: Optional cookies to include in the request
            
        Returns:
            Raw JSON response as a dict containing event details
        """
        self.session.headers["referer"] = f"https://www.pdga.com/live/event/{event_id}"
        return self._make_request("live_results_fetch_event", params={"TournID": event_id}, cookies=cookies)

    def get_event_rounds(self, event_id: int, cookies: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Fetch all rounds for an event.
        
        Args:
            event_id: PDGA tournament/event ID
            cookies: Optional cookies to include
            
        Returns:
            Raw JSON response containing round information
        """
        self.session.headers["referer"] = f"https://www.pdga.com/live/event/{event_id}"
        return self._make_request("live_results_fetch_rounds", params={"TournID": event_id}, cookies=cookies)

    def get_round_scores(
        self, event_id: int, round_number: int, cookies: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Fetch scores for a specific round.
        
        Args:
            event_id: PDGA tournament/event ID
            round_number: Round number/index
            cookies: Optional cookies to include
            
        Returns:
            Raw JSON response containing round scores
        """
        self.session.headers["referer"] = f"https://www.pdga.com/live/event/{event_id}"
        return self._make_request(
            "live_results_fetch_round_scores",
            params={"TournID": event_id, "RoundNumber": round_number},
            cookies=cookies,
        )

    def get_player_card(self, player_id: int, cookies: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Fetch a player's scorecard/results.
        
        Args:
            player_id: PDGA player ID
            cookies: Optional cookies to include
            
        Returns:
            Raw JSON response containing player card data
        """
        return self._make_request("live_results_fetch_player_card", params={"PlayerID": player_id}, cookies=cookies)
