# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
from setuptools import setup, find_packages


requires = [
    'mock>=1.0.1',
]


setup(
    name="pytest-spec",
    packages=['pytest_spec'],
    version="3.0.0",
    entry_points={'pytest11': ['pytest_spec = pytest_spec.plugin']},
    description="pytest plugin to display test execution output like a SPECIFICATION",
    author="Pawel Chomicki",
    author_email="pawel.chomicki@gmail.com",
    install_requires=requires,
    url="https://github.com/pchomik/pytest-spec",
)
