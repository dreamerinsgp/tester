"""Pytest fixtures for API tests."""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.client import get_client


@pytest.fixture(scope="session")
def base_url():
    """Base URL of the API under test."""
    return os.getenv("BASE_URL", "http://localhost:5000")


@pytest.fixture
def client(base_url):
    """HTTP client (session) for API calls."""
    return get_client(base_url)


@pytest.fixture(scope="session")
def auth_token(base_url):
    """Obtain auth token by logging in. Reused across the whole test session."""
    c = get_client(base_url)
    r = c.post(
        f"{base_url}/login",
        json={"email": "alice@test.com", "password": "secret123"},
    )
    assert r.status_code == 200, f"Login failed: {r.text}"
    j = r.json()
    assert "token" in j
    return j["token"]
