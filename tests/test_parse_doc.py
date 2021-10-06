#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the stance_finder module.
"""
import pytest

from stance_finder import parse_docs


def test_preprocess():
    text = '„žë"'
    preprocessed_text = parse_docs.preprocess(text)
    assert preprocessed_text == '"ze"'
