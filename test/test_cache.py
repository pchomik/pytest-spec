# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import unittest

from pytest_spec.cache import Cache


class TestPluginCache(unittest.TestCase):
    def setUp(self):
        self.default = "default test value"
        self.cache = Cache(self.default)

    def test_cache_is_a_singleton(self):
        cache = Cache()
        self.assertIs(self.cache, cache)

    def test_cache_stores_default_value(self):
        cache = Cache()
        self.assertEqual(cache.default, self.default)

    def test_cache_stores_keys_and_values(self):
        self.cache.put('k1', 'value1')
        self.cache.put('k2', 'value2')
        self.cache.put('k3', 'value3')

        self.assertEqual(self.cache.get('k2'), 'value2')
        self.assertEqual(self.cache.get('k3'), 'value3')
        self.assertEqual(self.cache.get('k1'), 'value1')

    def test_cache_returns_none_when_key_does_not_exist(self):
        self.assertIsNone(self.cache.get('wrong key'))


if __name__ == '__main__':
    unittest.main()
