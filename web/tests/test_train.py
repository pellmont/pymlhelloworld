"""Tests for the model training."""

import os
import sys
from unittest.mock import patch

import pandas as pd

from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline

import pymlhelloworld.pipeline
from pymlhelloworld.train import ModelTrainer
from pymlhelloworld.train import main
from pymlhelloworld.train import read_data


def test_train_and_pickle():
    """Test with iris dataset."""
    # arrange
    filename = 'testmodel.pkl'
    removefile(filename)
    pipeline = Pipeline([
        ('feature_selection', SelectKBest(chi2, k=2)),
        ('classification', RandomForestClassifier())
    ])
    iris = datasets.load_iris()
    # pylint: disable=E1101
    data = pd.DataFrame(iris.data, columns=iris.feature_names)
    data['target'] = iris.target
    testee = ModelTrainer(pipeline, 'target', iris.feature_names)

    try:
        # act
        testee.train(data)
        testee.write_pickled_model(filename)

        # assert
        assert os.path.exists(filename)
    finally:
        removefile(filename)


def test_data_from_url():
    """Test with loading data from url."""
    # arrange
    pipeline = Pipeline([
        ('feature_selection', SelectKBest(chi2, k=2)),
        ('classification', RandomForestClassifier())
    ])
    testee = ModelTrainer(pipeline, 'Name', ['SepalLength',
                                             'SepalWidth',
                                             'PetalLength',
                                             'PetalWidth'])

    # act
    url = ('https://raw.githubusercontent.com/'
           'pandas-dev/pandas/master/pandas/tests/data/iris.csv')
    data = read_data(url, {'X-something': 'to ignore'})
    testee.train(data)

    # assert
    pred = testee.pipeline.predict(data.drop('Name', 1))
    assert f1_score(data['Name'], pred, average='micro') >= 0.95


@patch.object(sys, 'argv', ['train',
                            'http://the.url/test.csv',
                            'tmppickle.pkl',
                            'tmptrainpickle.pkl',
                            'tmpvalidpickle.pkl',
                            'header'])
@patch.object(pymlhelloworld.pipeline, 'features',
              ['sepal length (cm)', 'sepal width (cm)',
               'petal length (cm)', 'petal width (cm)'])
@patch('pymlhelloworld.pipeline.init_pipeline')
@patch('pymlhelloworld.train.read_data')
def test_main(myreaddata, init_pipeline):
    """Test for main method."""
    # arrange
    removefile('tmppickle.pkl')
    removefile('tmptrainpickle.pkl')
    removefile('tmpvalidpickle.pkl')
    pipeline = Pipeline([
        ('feature_selection', SelectKBest(chi2, k=2)),
        ('classification', RandomForestClassifier())
    ])
    init_pipeline.return_value = pipeline
    iris = datasets.load_iris()
    # pylint: disable=E1101
    data = pd.DataFrame(iris.data, columns=iris.feature_names)
    data['loan_status'] = iris.target
    myreaddata.return_value = data

    # act
    main()

    # assert
    try:
        # assert
        assert os.path.exists('tmppickle.pkl')
        assert os.path.exists('tmptrainpickle.pkl')
        assert os.path.exists('tmpvalidpickle.pkl')
    finally:
        removefile('tmppickle.pkl')
        removefile('tmptrainpickle.pkl')
        removefile('tmpvalidpickle.pkl')


def removefile(filename):
    """Remove a temporary file if exists."""
    if os.path.exists(filename):
        os.remove(filename)
