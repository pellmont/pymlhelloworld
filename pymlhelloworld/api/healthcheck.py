"""
This module implements healthcheck API for monitoring.
"""
from flask_restplus import Resource, Namespace


api = Namespace('healthcheck', description='Healthcheck operation')


@api.route('/')
class Health(Resource):
    """
    Health resource implements healthcheck API operations.
    """

    def get(self):
        """
        Calls the services of this application and verify that all endpoints
        behave as expected.
        """
        print("Healthcheck called!")
