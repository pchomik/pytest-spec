"""Module contains cache class which may limit number of read operations.

:author: Pawel Chomicki
"""


class Cache(object):

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self, default=''):
        self._default = default
        self._cached = {}

    def put(self, key, value):
        self._cached[key] = value

    def get(self, key):
        return self._cached.get(key, None)

    @property
    def default(self):
        return self._default
