"""This module implements healthcheck API for monitoring."""
# pragma: no cover
from flask import abort, request, url_for

from flask_restplus import Namespace, Resource

import requests


api = Namespace('healthcheck', description='Healthcheck operation')


test_payload = {
    'home_ownership': True,
    'purpose': 'some purpose',
    'addr_state': 'some state',
    'loan_amnt': 1.0,
    'installement': 1,
    'annual_income': 1.0,
    'int_rate': 1.0,
    'emp_length': 1,
}

expected_response = {
    'good_loan': True,
    'confidence': 0.7,
}


@api.route('/')
class Health(Resource):
    """Health resource implements healthcheck API operations."""

    def get(self):
        """Check the service health.

        Call services of this application and verify that all endpoints
        behave as expected.
        """
        predict_ep = url_for('predict_predict')
        predict_url = 'http://{0}:{1}{2}'.format(
            request.environ['SERVER_NAME'],
            request.environ['SERVER_PORT'],
            predict_ep)
        try:
            r = requests.post(predict_url,
                              data=test_payload, timeout=0.02)
        except requests.exceptions.Timeout:
            abort(500)

        if r.json() != expected_response:
            abort(500)

        return '', 200
