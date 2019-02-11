import pytest
from flask import url_for
from pymlhelloworld import app


valid_data = {
    'home_ownership': 1,
    'purpose': 1,
    'addr_state': 1,
    'loan_amnt': 1,
    'installement': 1,
    'annual_income': 1,
    'int_rate': 1,
    'emp_lenght': 1,
}


@pytest.fixture(scope="module")
def ep():
    with app.test_request_context():
        ep = url_for('predict_predict')
    return ep


def test_success(client, ep):
    """
    Tests that the proper response is given if the parameters are correct.
    """
    response = client.post(ep, data=valid_data)
    assert response.status_code == 200


def test_invalid_parameter_type(client, ep):
    """
    Test that invalid parameter type will be rejected with the proper HTTP
    reponse code and message.
    """
    invalid_type = dict(valid_data)
    # Make parameter type bool instead of int
    invalid_type['installement'] = True
    response = client.post(ep, data=invalid_type)
    assert response.status_code == 400
    assert 'installement' in response.json['errors']
    assert 'invalid literal for int' in response.json['errors']['installement']


def test_missing_required_parameter(client, ep):
    """
    Test that payload with missing parameter will be rejected with the proper
    HTTP reponse code and message.
    """
    missing_param = dict(valid_data)
    del missing_param['installement']
    response = client.post(ep, data=missing_param)
    assert response.status_code == 400
    assert 'installement' in response.json['errors']
    assert 'Missing required parameter' \
        in response.json['errors']['installement']
