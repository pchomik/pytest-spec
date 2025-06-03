"""
:author: Pawel Chomicki
:e-mail: pawel.chomicki@gmail.com
"""

import unittest

import pytest


def some_function(arg):
    return arg


def test__some_function__returns_none():
    """Some func"""
    assert some_function(None) is None


def test_some_function__single_underscore_as_prefix():
    assert some_function(None) is None


def test__some_function_single_underscore_as_suffix():
    assert some_function(None) is None


def test_with_custom_description():
    """Shows custom message from docstring summary"""
    assert some_function(None) is None


def test_with_multiline_docstring():
    """
    Shows custom message from docstring summary

    And doesn't show additional info.
    """
    assert some_function(None) is None


@pytest.mark.parametrize("input_value", ["param1", "param2"])
def test_when_parametrized(input_value):
    assert input_value in ["param1", "param2"]


if __name__ == "__main__":
    unittest.main()
