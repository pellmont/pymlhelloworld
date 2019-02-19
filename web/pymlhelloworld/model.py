# pylint: disable= R0903,R0201,W0613
"""Prediction model used by the service.

Prediction model loads persisted state from the training process and use
model to do the prediction.

"""
import logging
import pickle

import pandas as pd

from .api.healthcheck import expected_response

logger = logging.getLogger(__name__)


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

    _pipeline = None

    @classmethod
    def load_model(cls):
        """Loads model from pickle. Model is kept on the class level."""
        if cls._pipeline is None:
            try:
                with open('model.pkl', 'rb') as f:
                    cls._pipeline = pickle.load(f)
            except FileNotFoundError:
                # Pickled model file doesn't exist during fast testing
                # stage. Dummy model will be used in that case.
                # During real testing stage the test will fail if the model
                # is not loaded.
                logger.warning('Warning: model.pkl not loaded.')

    @classmethod
    def predict(cls, input_args):
        """Return prediction based on the input arguments.

        :param input_args: The input data arguments.
        :type input_args: dict

        :return: the Prediction object.
        :rtype: Prediction
        """
        cls.load_model()
        from .api.predict import api_model_name_mapping
        predict_dict = {api_model_name_mapping.get(k, k): v
                        for k, v in input_args.items()}
        input_frame = pd.DataFrame(predict_dict, index=[0])

        from pymlhelloworld import app
        if 'FAKE_MODEL' not in app.config:
            prediction = cls._pipeline.predict(input_frame)
            import numpy as np
            probas = cls._pipeline.predict_proba(input_frame)[0]
            proba = probas[np.where(cls._pipeline.classes_ == prediction[0])]
            return Prediction(prediction[0], proba)

        return Prediction(expected_response['good_loan'],
                          expected_response['confidence'])
