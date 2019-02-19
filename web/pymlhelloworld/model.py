# pylint: disable= R0903,R0201,W0613
"""Prediction model used by the service.

Prediction model loads persisted state from the training process and use
model to do the prediction.

"""
import logging
import pickle

import pandas as pd

from . import api


logger = logging.getLogger(__name__)

pipeline = None
try:
    with open('model.pkl', 'rb') as f:
        pipeline = pickle.load(f)
except FileNotFoundError:
    # Pickled model file doesn't exist during fast testing
    # stage. Dummy model will be used in that case.
    # During real testing stage the test will fail if the model
    # is not loaded.
    logger.warning('Warning: model.pkl not loaded.')


class Prediction:
    """Prediction class used to pass an answer from prediction model."""

    def __init__(self, good_loan=False, confidence=0):
        """Initialize the prediction."""
        self.good_loan = good_loan
        self.confidence = confidence


def predict(input_args):
    """Return prediction based on the input arguments.

    :param input_args: The input data arguments.
    :type input_args: dict

    :return: the Prediction object.
    :rtype: Prediction
    """
    predict_dict = {api.predict.api_model_name_mapping.get(k, k): v
                    for k, v in input_args.items()}
    input_frame = pd.DataFrame(predict_dict, index=[0])

    prediction = pipeline.predict(input_frame)

    # TODO: How to get confidence?
    return Prediction(prediction[0], 0.7)
