"""
:author: Pawel Chomicki
:e-mail: pawel.chomicki@gmail.com
"""

import unittest


def some_method(arg):
    return arg


def test__some_method__returns_true():
    assert some_method(True) is True


@unittest.skip("Remove docorator to see fail result")
def test__some_method__returns_false():
    assert some_method(True) is False


@unittest.skip("To implement")
def test__some_method__return_none():
    assert some_method(True) is None


if __name__ == "__main__":
    unittest.main()
