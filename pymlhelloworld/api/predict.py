"""
This module implements prediction API.
"""
from collections import namedtuple
from flask_restplus import Namespace, Resource, fields, reqparse

api = Namespace('predict', description='Prediction related operations')

prediction = api.model('Predict', {
    'good_loan': fields.Boolean(description='The prediction outcome'),
    'confidence': fields.Float(description='The prediction confidence')
})

PredictParam = namedtuple('PredictParam', 'name type required help')

# TODO: Correct meta-data for parameters (types, help messages...)
predict_input_params = (
    PredictParam('home_ownership', type=int, required=True, help='???'),
    PredictParam('purpose', type=int, required=True, help='???'),
    PredictParam('addr_state', type=int, required=True, help='???'),
    PredictParam('loan_amnt', type=int, required=True, help='???'),
    PredictParam('installement', type=int, required=True, help='???'),
    PredictParam('annual_income', type=int, required=True, help='???'),
    PredictParam('int_rate', type=int, required=True, help='???'),
    PredictParam('emp_lenght', type=int, required=True, help='???'),
)


@api.route('/')
class Predict(Resource):
    """
    Resource providing model prediction.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Input Parameters
        self.parser = reqparse.RequestParser()
        for param in predict_input_params:
            self.parser.add_argument(param.name,
                                     type=param.type,
                                     required=param.required,
                                     help=param.help)

    # @api.marshal_with(prediction)
    def post(self):
        """
        Calls model prediction for the given parameters and return the
        prediction.
        """
        # Parses and validates input arguments
        # In case of validation error HTTP 400 will be returned
        data = self.parser.parse_args()
        return "Hello"  # Predictor.predict(data)
