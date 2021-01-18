#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the stance_finder module.
"""
import pytest

from stance_finder import stance_finder


def test_something():
    assert True


def test_with_error():
    with pytest.raises(ValueError):
        # Do something that raises a ValueError
        raise(ValueError)


# Fixture example
@pytest.fixture
def an_object():
    return {}


def test_stance_finder(an_object):
    assert an_object == {}
