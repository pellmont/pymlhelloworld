"""The pipeline for this machine learning model configured."""

from sklearn.ensemble import RandomForestClassifier as rf
from sklearn.pipeline import Pipeline


def init_pipeline():
    """Define the production pipeline."""
    classifier = rf(n_estimators=20, max_depth=20)
    return Pipeline(steps=[('classification', classifier)])
