# pylint: disable= R0903,R0201,W0613
"""Prediction model implementation."""
from .api.healthcheck import expected_response


class Prediction:
    """Prediction class used to pass an answer from prediction model."""

    def __init__(self, good_loan=False, confidence=0):
        """Initialize the prediction."""
        self.good_loan = good_loan
        self.confidence = confidence


class PredictionModel:
    """Prediction model used by the service.

    Prediction model loads persisted state from the training process and use
    model to do the prediction.

    """

    def __init__(self):
        """Load the persisted trained model."""

    def predict(self, input_args):
        """Return prediction based on the input arguments.

        :param input_args: The input data arguments.
        :type input_args: dict

        :return: the Prediction object.
        :rtype: Prediction
        """
        # Return some dummy data at the moment until we implement the proper
        # model. This is here to be able to test swagger UI.
        return Prediction(expected_response['good_loan'],
                          expected_response['confidence'])
