pytest-spec
===========
pytest plugin to display test execution output like a SPECIFICATION.

.. image:: https://badgen.net/badge/python/2.7/green
.. image:: https://badgen.net/badge/python/3.5/green
.. image:: https://badgen.net/badge/python/3.6/green
.. image:: https://badgen.net/badge/python/3.7/green
.. image:: https://badgen.net/badge/python/3.8/green
.. image:: https://badgen.net/badge/python/3.9/green

.. image:: https://badgen.net/badge/os/linux/green
.. image:: https://badgen.net/badge/os/windows/green
.. image:: https://badgen.net/badge/os/macos/green

.. image:: https://badgen.net/badge/pytest/3.9.3/green
.. image:: https://badgen.net/badge/pytest/4.6.11/green
.. image:: https://badgen.net/badge/pytest/5.4.3/green
.. image:: https://badgen.net/badge/pytest/6.1.2/green


Available features
==================
* Format output to look like specification.
* Group tests by classes and files
* Failed, passed and skipped are marked and colored.
* Remove test\_ and underscores for every test.
* Supports function based, class based test.
* Supports describe like tests.


Output example
==============

.. image:: https://github.com/pchomik/pytest-spec/raw/master/docs/output.png


Configuration
=============

``spec_header_format``
----------------------

You can configure the format of the test headers by specifying a `format string <https://docs.python.org/2/library/string.html#format-string-syntax>`_ in your `ini-file <http://doc.pytest.org/en/latest/customize.html#inifiles>`_:

::

    [pytest]
    spec_header_format = {module_path}:

In addition to the ``{path}`` and ``{class_name}`` replacement fields, there is also ``{test_case}`` that holds a more human readable name.

``spec_test_format``
--------------------

You can configure the format of the test results by specifying a `format string <https://docs.python.org/2/library/string.html#format-string-syntax>`_ in your `ini-file <http://doc.pytest.org/en/latest/customize.html#inifiles>`_:

::

    [pytest]
    spec_test_format = {result} {name}

``spec_success_indicator``
--------------------------

You can configure the indicator displayed when test passed.

::

    [pytest]
    spec_success_indicator = ✓

``spec_failure_indicator``
--------------------------

You can configure the indicator displated when test failed.

::

    [pytest]
    spec_failure_indicator = ✗

``spec_skipped_indicator``
--------------------------

You can configure the indicator displated when test is skipped.

::

    [pytest]
    spec_skipped_indicator = ?

``spec_indent``
---------------

::

    [pytest]
    spec_indent = "   "

Continuous Integration
======================
.. image:: https://github.com/pchomik/pytest-spec/workflows/test/badge.svg
     :target: https://github.com/pchomik/pytest-spec/actions

Download
========
All versions of library are available on official `pypi server <https://pypi.org/project/pytest-spec/#history>`_.

Install
=======
::

    pip install pytest-spec

Contribution
============
Please feel free to present your idea by code example (pull request) or reported issues.

Contributors
============
* @0x64746b
* @lucasmarshall
* @amcgregor
* @jhermann
* @frenzymadness
* @chrischambers
* @maxalbert
* @jayvdb

License
=======
pytest-spec - pytest plugin to display test execution output like a SPECIFICATION.

Copyright (C) 2014-2019 Pawel Chomicki

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
