"""HTTP client wrapper for API tests."""
import requests
from .config import BASE_URL, TIMEOUT


def new_session():
    """Create a requests Session with common headers."""
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    s.timeout = TIMEOUT
    return s


def get_client(base_url: str = None):
    """Return a session configured for the given base_url."""
    s = new_session()
    s.base_url = (base_url or BASE_URL).rstrip("/")
    return s
