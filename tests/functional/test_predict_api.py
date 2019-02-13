"""
Tests for predict API.
"""
# pylint: disable=W0621
import pytest
from unittest.mock import patch
from flask import url_for
from pymlhelloworld import app
from pymlhelloworld import model


valid_data = {
    'home_ownership': True,
    'purpose': 'some purpose',
    'addr_state': 'some state',
    'loan_amnt': 1.0,
    'installement': 1,
    'annual_income': 1.0,
    'int_rate': 1.0,
    'emp_lenght': 1,
}


@pytest.fixture(scope="module")
def ep_url():
    """
    Fixture for predict endpoint URL.
    """
    with app.test_request_context():
        ep = url_for('predict_predict')
    return ep


def test_success_real_model(client, ep_url, real_model):
    """
    Tests that the proper response is given if the parameters are correct.
    """
    if not real_model:
        # If we are not running test with the real model we shall use a mocked
        # version.
        with patch.object(
                model.PredictionModel,
                'predict',
                return_value=model.Prediction(True, 0.5)) as mock_method:
            response = client.post(ep_url, data=valid_data)
            assert response.status_code == 200
            # Assert that the predict method was called with test data.
            assert dict(mock_method.call_args[0][0]) == valid_data
    else:
        response = client.post(ep_url, data=valid_data)
        assert response.status_code == 200


def test_invalid_parameter_type(client, ep_url):
    """
    Test that invalid parameter type will be rejected with the proper HTTP
    reponse code and message.
    """
    invalid_type = dict(valid_data)
    # Make parameter type bool instead of int
    invalid_type['installement'] = True
    response = client.post(ep_url, data=invalid_type)
    assert response.status_code == 400
    assert 'installement' in response.json['errors']
    assert 'invalid literal for int' in response.json['errors']['installement']


def test_missing_required_parameter(client, ep_url):
    """
    Test that payload with missing parameter will be rejected with the proper
    HTTP reponse code and message.
    """
    missing_param = dict(valid_data)
    del missing_param['installement']
    response = client.post(ep_url, data=missing_param)
    assert response.status_code == 400
    assert 'installement' in response.json['errors']
    assert 'Missing required parameter' \
        in response.json['errors']['installement']
