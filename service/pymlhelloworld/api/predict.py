"""This module implements prediction API."""
from collections import namedtuple

from flask_restplus import Namespace, Resource, fields

from prometheus_client import Histogram

from pymlhelloworld.model import PredictionModel

api = Namespace('predict', description='Prediction related operations')

prediction = api.model('Prediction', {
    'good_loan': fields.Boolean(description='The prediction outcome'),
    'confidence': fields.Float(description='The prediction confidence')
})

PredictParam = namedtuple('PredictParam', 'name type required help')

# TODO: Correct meta-data for parameters (types, help messages...)
predict_input_params = (
    PredictParam('home_ownership', type=bool, required=True, help='???'),
    PredictParam('purpose', type=str, required=True, help='???'),
    PredictParam('addr_state', type=str, required=True, help='???'),
    PredictParam('loan_amnt', type=float, required=True, help='???'),
    PredictParam('installment', type=int, required=True, help='???'),
    PredictParam('annual_income', type=float, required=True, help='???'),
    PredictParam('int_rate', type=float, required=True, help='???'),
    PredictParam('emp_length', type=int, required=True, help='???'),
)

# If the feature names from the model differs from the names used in API
# specify here the mapping. If mapping is not found in this dict the same name
# is used to do the prediction.
api_model_name_mapping = {
    'annual_income': 'annual_inc'
}

predict_parser = api.parser()
for param in predict_input_params:
    predict_parser.add_argument(param.name,
                                type=param.type,
                                required=param.required,
                                help=param.help)

LATENCY = Histogram('request_latency_seconds', 'Request Latency')


@api.route('/')
class Predict(Resource):
    """Resource providing model prediction."""

    @api.expect(predict_parser)
    @api.marshal_with(prediction)
    @LATENCY.time()
    def post(self):
        """Call model prediction for the given parameters.

        :returns: Prediction instance.
        """
        # Parses and validates input arguments
        # In case of validation error HTTP 400 will be returned
        data = predict_parser.parse_args()
        return PredictionModel.predict(data), 200
