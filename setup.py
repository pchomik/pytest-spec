# -*- coding: utf-8 -*-
"""
:author: Pawel Chomicki
"""
from os import path

from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


requires = [
    'mock>=1.0.1',
]


setup(
    name="pytest-spec",
    packages=['pytest_spec'],
    version="3.0.1",
    entry_points={'pytest11': ['pytest_spec = pytest_spec.plugin']},
    description="pytest plugin to display test execution output like a SPECIFICATION",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Pawel Chomicki",
    author_email="pawel.chomicki@gmail.com",
    install_requires=requires,
    url="https://github.com/pchomik/pytest-spec",
    license='GPLv2',
    license_file='LICENSE.txt'
)
