"""This module collects all namespaces under a single API."""
from flask_restplus import Api

from .healthcheck import api as healthcheck_api
from .predict import api as predict_api

api = Api(
    title='Loan Prediction API',
    version='0.1',
    description='A simple example REST API for loan prediction',
)

api.add_namespace(predict_api)
api.add_namespace(healthcheck_api)
