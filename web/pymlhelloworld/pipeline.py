"""The pipeline for this machine learning model configured."""

import re

import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

target = "good_loan"
cat_features = ['home_ownership', 'purpose', 'addr_state']
num_features = ['loan_amnt', 'installment', 'annual_inc',
                'int_rate', 'emp_length']
features = cat_features + num_features


def emp_length_num(string):
    """Parse length."""
    if string == '< 1 year':
        emp_length = 0
    else:
        emp_length = find_number(string)
    return emp_length


def find_number(string):
    """Extract number from String."""
    if isinstance(string, float):
        first_number = float('NaN')
    elif isinstance(string, str):
        first_number = int(re.findall(pattern='([0-9]+)', string=string)[0])
    elif isinstance(string, int):
        first_number = string
    else:
        raise Exception('invalid type ' + str(type(string)))
    return first_number


class CreateDerivedFeatures(TransformerMixin, BaseEstimator):
    """Transformer for derived feature."""

    # pylint: disable=W0613
    def fit(self, X, *_):
        """Fit the model."""
        return self

    def transform(self, X, *_):
        """Apply learned transformation."""
        X_transformed = X.assign(
            loan_income_ratio=pd.Series(X.loan_amnt / X.annual_inc),
            interest_income_ratio=pd.Series(
                (X.loan_amnt * 0.01 * X.int_rate) / X.annual_inc),
            emp_length=pd.Series(X.emp_length.apply(emp_length_num)))
        return X_transformed


def init_pipeline():
    """Define the production pipeline."""
    derive_step = ('derive', CreateDerivedFeatures())
    derive_features = Pipeline([derive_step])
    si_step_cat = ('si_cat', SimpleImputer(strategy='constant',
                                           fill_value='missing_value'))
    ohe_step_cat = ('ohe_cat', OneHotEncoder(handle_unknown='ignore',
                                             sparse=False))
    pipe_cat = Pipeline([si_step_cat, ohe_step_cat])
    si_step_num = ('si_num', SimpleImputer(strategy='constant',
                                           fill_value=-999))
    pipe_num = Pipeline([si_step_num])
    preprocessor = ColumnTransformer(
        transformers=[('cat', pipe_cat, cat_features),
                      ('num', pipe_num, num_features)]
    )
    classifier = rf(n_estimators=20, max_depth=20)
    preprocessor_classifier = Pipeline([
        ('derive_features', derive_features),
        ('preprocessor', preprocessor),
        ('classifier', classifier)
    ])
    return preprocessor_classifier
