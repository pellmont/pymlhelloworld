"""Tests the assembly of the production pipeline."""

import math

import pymlhelloworld.pipeline


def test_init_pipeline():
    """First fake test for the production pipeline."""
    assert pymlhelloworld.pipeline.init_pipeline()


def test_emp_length_num():
    """Test emp_length function."""
    assert pymlhelloworld.pipeline.emp_length_num('< 1 year') == 0
    assert pymlhelloworld.pipeline.emp_length_num('5 years') == 5


def test_find_number():
    """Test extract number from string or int field."""
    assert pymlhelloworld.pipeline.find_number('the 1st number') == 1
    assert pymlhelloworld.pipeline.find_number(5) == 5
    assert math.isnan(pymlhelloworld.pipeline.find_number(1.3))
