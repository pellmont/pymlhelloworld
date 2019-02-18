"""Test for healthcheck endpoint."""

from flask import url_for

import requests

from pymlhelloworld import app


def test_healthcheck(flask_server):
    """Test that healthcheck endpoint operates correctly."""
    with app.test_request_context():
        healthcheck_ep = url_for('healthcheck_health')

    r = requests.get(f"{flask_server}{healthcheck_ep}", timeout=1)
    assert r.status_code == 200
