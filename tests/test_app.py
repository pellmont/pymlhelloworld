"""Tests for app.py."""

from unittest import TestCase

from pymlhelloworld.app import APP


class TestApp(TestCase):
    """Integration Test for app.py."""

    def test_app_movies(self):
        """Test /api endpoint."""
        APP.testing = True
        with APP.test_client() as client:
            resp = client.get('/api')
            # to be fixed once running
            self.assertEqual(resp.status, "404 NOT FOUND")
