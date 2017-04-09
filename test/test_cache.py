# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
import pytest

from asserts import assert_equal, assert_is, assert_is_none
from pytest_spec.cache import Cache


class TestPluginCache(object):
    
    def setup_class(self):
        self.default = "[{result}]  {name}"
        self.cache = Cache()

    def test_cache_is_a_singleton(self):
        cache = Cache()
        assert_is(self.cache, cache)

    def test_cache_stores_default_value(self):
        cache = Cache()
        assert_equal(cache.default, self.default)

    def test_cache_stores_keys_and_values(self):
        self.cache.put('k1', 'value1')
        self.cache.put('k2', 'value2')
        self.cache.put('k3', 'value3')

        assert_equal(self.cache.get('k2'), 'value2')
        assert_equal(self.cache.get('k3'), 'value3')
        assert_equal(self.cache.get('k1'), 'value1')

    def test_cache_returns_none_when_key_does_not_exist(self):
        assert_is_none(self.cache.get('wrong key'))


if __name__ == '__main__':
    pytest.main()
