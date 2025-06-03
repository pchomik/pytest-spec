"""
:author: Pawel Chomicki
:e-mail: pawel.chomicki@gmail.com
"""

import unittest


class SomeClass:
    def some_method(self, arg):
        return arg


class TestFormats(unittest.TestCase):
    def test__some_method__returns_none(self):
        assert SomeClass().some_method(None) is None

    def test_some_method__single_underscore_as_prefix(self):
        assert SomeClass().some_method(None) is None

    def test__some_method_single_underscore_as_suffix(self):
        assert SomeClass().some_method(None) is None

    def test_with_custom_message(self):
        """Shows custom message from docstring summary"""
        assert SomeClass().some_method(None) is None

    def test_with_multiline_docstring(self):
        """
        Shows custom message from docstring summary

        And doesn't show additional info.
        """
        assert SomeClass().some_method(None) is None


if __name__ == "__main__":
    unittest.main()
