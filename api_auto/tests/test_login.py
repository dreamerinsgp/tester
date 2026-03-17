"""Login endpoint tests."""
import json
import os

import pytest


def _load_users():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")
    with open(path) as f:
        return json.load(f)


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize("case", _load_users())
def test_login_parametrized(client, base_url, case):
    r = client.post(
        f"{base_url}/login",
        json={"email": case["email"], "password": case["password"]},
    )
    assert r.status_code == case["expect_status"]


@pytest.mark.regression
def test_login_missing_email(client, base_url):
    r = client.post(f"{base_url}/login", json={"password": "x"})
    assert r.status_code == 400
