"""Tests the assembly of the production pipeline."""

import pymlhelloworld.pipeline


def test_init_pipeline():
    """First fake test for the production pipeline."""
    assert pymlhelloworld.pipeline.init_pipeline()
