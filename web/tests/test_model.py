"""Just some basic tests for prediction model."""
from pymlhelloworld import app
from pymlhelloworld.api.healthcheck import expected_response, test_payload
from pymlhelloworld.model import PredictionModel


def test_model_loading():
    """Test model loading."""
    PredictionModel.load_model()

    # Since there is no pickled model pipeline is None
    assert PredictionModel.pipeline is None


def test_model_predict():
    """Test calling model prediction method."""
    # If we are using fake model we should get fake predict result.
    app.config['FAKE_MODEL'] = True

    p = PredictionModel.predict(test_payload)
    assert p.good_loan == expected_response['good_loan']
    assert p.confidence == expected_response['confidence']
