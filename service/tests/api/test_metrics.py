"""Test the mtrics api."""
# pylint: disable=W0621
from flask import url_for

import pytest

from pymlhelloworld import app


@pytest.fixture(scope="module")
def ep_url():
    """Fixture for predict endpoint URL."""
    with app.test_request_context():
        ep = url_for('metrics_metrics')
    return ep


def test_getting_metrics(client, ep_url):
    """Test the mtric endpoint."""
    response = client.get(ep_url)
    assert response.status_code == 200
