"""
pytest configuration. E.g. fixtures for all tests.
"""

import pytest
from pymlhelloworld import app


@pytest.fixture
def client():
    return app.test_client()
