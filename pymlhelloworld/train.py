"""Script to download the training data and train the model."""

import os
import pickle
import sys
import urllib.request
from typing import Dict

import pandas as pd

import sklearn.pipeline
from sklearn.model_selection import train_test_split

import pymlhelloworld.pipeline


class ModelTrainer():
    """Constructor takes a preconfigured Pipeline."""

    def __init__(self, pipeline, target_col):
        """Constructor."""
        self.pipeline = sklearn.base.clone(pipeline)
        self.target_col = target_col
        self.metrics = None
        self.traindata = None
        self.validdata = None

    def train(self, data):
        """Trains and evaluates the model."""
        train, valid = train_test_split(data,
                                        test_size=0.25,
                                        random_state=111)
        self.traindata = train
        self.validdata = valid
        x_train = self.traindata.drop(self.target_col, 1)
        y_train = self.traindata[self.target_col]
        self.pipeline.fit(x_train, y_train)
        x_valid = self.validdata.drop(self.target_col, 1)
        y_valid = self.validdata[self.target_col]
        y_pred = self.pipeline.predict(x_valid)
        self.metrics = sklearn.metrics.classification_report(y_valid, y_pred)

    def write_pickled_model(self, outputfilename):
        """Write the pickled model to file."""
        with open(outputfilename, 'wb') as file:
            pickle.dump(self.pipeline, file)

    def write_pickled_trainset(self, outputfilename):
        """Write the training data pickled to disk."""
        self.traindata.to_pickle(outputfilename)

    def write_pickled_validset(self, outputfilename):
        """Write the validation data pickled to disk."""
        self.validdata.to_pickle(outputfilename)


def read_data(url: str, headers: Dict = None) -> pd.DataFrame:
    """Read a CSV form an URL and put it in a pandas Dataframe."""
    if headers is None:
        headers = dict()
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
    if len(sys.argv) == 6:
        headers = sys.argv[5]
    elif len(sys.argv) == 5:
        headers = dict()
    else:
        os.write(2, b'invalid number of arguments.\n\n'
                    b'usage: train <url> <outputfile>'
                    b' <trainoutfile> <validoutfile>'
                    b' [request-headers]\n')
        sys.exit(-1)
    data = read_data(sys.argv[1], headers)
    data['loan_status'] = data['loan_status'] == 'Fully Paid'
    trainer = ModelTrainer(pymlhelloworld.pipeline.init_pipeline(),
                           'loan_status')
    trainer.train(data)
    trainer.write_pickled_model(sys.argv[2])
    trainer.write_pickled_trainset(sys.argv[3])
    trainer.write_pickled_validset(sys.argv[4])


if __name__ == '__main__':
    main()
