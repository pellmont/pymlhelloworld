# pylint: disable=W0621
"""pytest configuration. E.g. fixtures for all tests."""

import logging
import time
from multiprocessing import Process

import pytest

from pymlhelloworld import app


# To test with externally run flask instance set this to True
DEBUG_STANDALONE = False

PORT = 15000

logging.basicConfig(level=logging.WARN)


def pytest_addoption(parser):
    """Adding parser options."""
    parser.addoption(
        "--real-model", action="store_true",
        help="if the real model should be used instead of mocked.")


@pytest.fixture(scope='session')
def real_model(request):
    """Fixture used to pass --real-model param from CLI."""
    return request.config.option.real_model


@pytest.fixture
def fake_model():
    """Configure Flake application to use fake model."""
    app.config['FAKE_MODEL'] = True


@pytest.fixture
def client():
    """Client for testing REST calls."""
    return app.test_client()


if DEBUG_STANDALONE:
    @pytest.fixture(scope="session")
    def flask_server():
        """Use an external Flask instance."""
        return 'http://localhost:5000'
else:
    @pytest.fixture(scope="session")
    def flask_server(real_model):
        """Create an instance of Flask server."""
        def run_app(port):
            if not real_model:
                app.config['FAKE_MODEL'] = True
            app.run(port=port, use_reloader=False)

        server_process = Process(target=run_app, args=(PORT, ))
        server_process.start()

        # Give 2 secs for the Flask server to start up
        time.sleep(2)

        yield f'http://localhost:{PORT}'

        server_process.terminate()
