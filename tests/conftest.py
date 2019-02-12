"""
pytest configuration. E.g. fixtures for all tests.
"""

import pytest
from pymlhelloworld import app


@pytest.fixture
def client():
    """
    Client for testing REST calls.
    """
    return app.test_client()
