# pylint: disable= R0903,R0201,W0613
"""Prediction model implementation."""
import pickle

import pandas as pd

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
        self.load_model()

    def load_model(self):
        """Loads model from pickle."""
        with open('model.pkl', 'rb') as f:
            self.pipeline = pickle.load(f)

    def predict(self, input_args):
        """Return prediction based on the input arguments.

        :param input_args: The input data arguments.
        :type input_args: dict

        :return: the Prediction object.
        :rtype: Prediction
        """
        from .api.predict import api_model_name_mapping
        predict_dict = {api_model_name_mapping.get(k, k): v
                        for k, v in input_args.items()}
        input_frame = pd.DataFrame(predict_dict, index=[0])
        prediction = self.pipeline.predict(input_frame)

        # TODO: How to get confidence?
        return Prediction(prediction[0], 0.7)
