"""
pytest configuration. E.g. fixtures for all tests.
"""

import pytest
from pymlhelloworld import app


def pytest_addoption(parser):
    parser.addoption(
        "--real-model", action="store_true",
        help="if the real model should be used instead of mocked.")


@pytest.fixture(scope='session')
def real_model(request):
    return request.config.option.real_model


@pytest.fixture
def client():
    """
    Client for testing REST calls.
    """
    return app.test_client()
