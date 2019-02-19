# pylint: disable=W0613
"""Just some basic tests for prediction model."""
from pymlhelloworld.api.healthcheck import expected_response, test_payload
from pymlhelloworld.model import PredictionModel


def test_model_loading(real_model):
    """Test model loading based on real_model CLI param."""
    PredictionModel.load_model()

    if real_model:
        assert PredictionModel.pipeline is not None
    else:
        assert PredictionModel.pipeline is None


def test_model_predict(fake_model):
    """Test calling model prediction method."""
    p = PredictionModel.predict(test_payload)
    assert p.good_loan == expected_response['good_loan']
    assert p.confidence == expected_response['confidence']
