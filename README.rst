pytest-spec
===========
pytest plugin to display test execution output like a SPECIFICATION.


Available features
==================
* Format output to look like specification.
* Group tests by classes and files
* Failed, passed and skipped are marked and colored.
* Remove test\_ and underscores for every test.


Output example
==============

::

    py.test --spec

    test/test_results/test_as_class.py::TestResults
        [SKIP]  Some method return none
        [FAIL]  Some method returns false
        [PASS]  Some method returns true

    test/test_results/test_as_functions.py
        [PASS]  Some method returns true
        [FAIL]  Some method returns false
        [SKIP]  Some method return none


Continuous Integration
======================
.. image:: https://drone.io/github.com/pchomik/pytest-spec/status.png
     :target: https://drone.io/github.com/pchomik/pytest-spec/latest

Download
========
Latest version of plugin is available in `drone.io project artifacts <https://drone.io/github.com/pchomik/pytest-spec/files>`_.

Install
=======
::

    pip install pytest-spec

Contribution
============
Please feel free to present your idea by code example (pull request) or reported issues.

Future plans
============
* Tests with other pytest plugins to check possible side-effects.
* Work to make output even better.

License
=======
pytest-spec - pytest plugin to display test execution output like a SPECIFICATION.

Copyright (C) 2014-2016 Pawel Chomicki

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
