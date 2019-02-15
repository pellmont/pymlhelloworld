"""Script to download the training data and train the model."""

import pickle
from typing import Dict

import pandas as pd

import pymlhelloworld.pipeline

import sklearn.pipeline
from sklearn.model_selection import train_test_split


class ModelTrainer():
    """Constructor takes a preconfigured Pipeline."""

    def __init__(self, pipeline, target_col):
        """Constructor."""
        self.pipeline = sklearn.base.clone(pipeline)
        self.target_col = target_col
        self.metrics = None

    def train(self, data):
        """Trains and evaluates the model."""
        train, valid = train_test_split(data,
                                        test_size=0.25,
                                        random_state=111)
        x_train = train.drop(self.target_col, 1)
        y_train = train[self.target_col]
        self.pipeline.fit(x_train, y_train)
        x_valid = valid.drop(self.target_col, 1)
        y_valid = valid[self.target_col]
        y_pred = self.pipeline.predict(x_valid)
        self.metrics = sklearn.metrics.classification_report(y_valid, y_pred)

    def write_pickled_model(self, outputfilename):
        """Write the pickled model to file."""
        with open(outputfilename, 'wb') as file:
            pickle.dump(self.pipeline, file)


def read_data(url: str, headers: Dict = None) -> pd.DataFrame:
    """Read a CSV form an URL and put it in a pandas Dataframe."""
    import urllib.request
    opener = urllib.request.build_opener(
        urllib.request.HTTPHandler(),
        urllib.request.HTTPSHandler()
    )
    urllib.request.install_opener(opener)
    req = urllib.request.Request(url=url, headers=headers)
    with urllib.request.urlopen(req) as file:
        data = pd.read_csv(file)
    return data


def main():
    """Train the model.

    arguments: url outputfilename reqestheaders
    """
    import sys
    if len(sys.argv) == 3:
        headers = sys.argv[2]
    data = read_data(sys.argv[0], headers)
    trainer = ModelTrainer(pymlhelloworld.pipeline.init_pipeline(), 'target')
    trainer.train(data)
    trainer.write_pickled_model(sys.argv[1])


if __name__ == '__main__':
    main()
