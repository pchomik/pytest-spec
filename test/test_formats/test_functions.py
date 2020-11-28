# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
:e-mail: pawel.chomicki@gmail.com
"""
import unittest


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


if __name__ == '__main__':
    unittest.main()
