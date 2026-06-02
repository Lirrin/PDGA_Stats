"""
Event data scraping utilities.
"""

import logging
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


class EventScraper:
    """Handles scraping of event/tournament data from PDGA live API.

    The PDGA live API endpoint used is:
    https://www.pdga.com/apps/tournament/live-api/live_results_fetch_event
    which accepts a `TournID` query parameter and returns JSON results.
    """

    def __init__(self, client: Optional[Any] = None, session: Optional[requests.Session] = None):
        """Initialize event scraper with an optional HTTP session and client.

        Args:
            client: optional higher-level client wrapper (unused by default).
            session: optional `requests.Session` to reuse headers/cookies.
        """
        self.client = client
        self.session = session or requests.Session()
        # Set sane default headers based on the curl provided by the user
        self.session.headers.update(DEFAULT_HEADERS)

    def _endpoint(self) -> str:
        return "https://www.pdga.com/apps/tournament/live-api/live_results_fetch_event"

    def scrape_events(self) -> Dict[str, Any]:
        """Placeholder for scraping multiple events (not implemented)."""
        raise NotImplementedError("Method not yet implemented")

    def scrape_event_details(self, event_id: int, cookies: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Fetch event details for a given `event_id` from the PDGA live API.

        This implements the same request shown in the provided curl. You can pass
        a `cookies` dict if you need to replicate the exact cookie string used
        in the browser. By default the request sends a minimal set of headers
        that emulate a modern browser.

        Args:
            event_id: numeric PDGA event id (TournID)
            cookies: optional mapping of cookie names to values

        Returns:
            Parsed JSON response as a dict on success.

        Raises:
            requests.HTTPError on non-2xx responses.
        """
        url = self._endpoint()
        params = {"TournID": event_id}
        # Update referer to match the event page
        self.session.headers["referer"] = f"https://www.pdga.com/live/event/{event_id}"

        resp = self.session.get(url, params=params, cookies=cookies, timeout=20)
        resp.raise_for_status()

        try:
            return resp.json()
        except ValueError:
            # Response wasn't JSON — return raw text under a key for debugging
            logger.exception("Non-JSON response from PDGA API for event %s", event_id)
            return {"text": resp.text}

