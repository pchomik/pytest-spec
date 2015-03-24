pytest-spec
===========
pytest plugin to display test execution output like a SPECIFICATION.


Available features
==================
* Format output to look like specification.
* Group tests by classes.
* Failed, passed and skipped are marked and colored.
* Remove test\_ and underscores for every test.
* Method under test may be highlighted (method) like in example.

Output example
==============

::

    py.test --spec

    test/test_example.py::TestWhenExamplePassed
        [PASS]  Execute returns positive return code

    test/test_example.py::TestWhenExampleFailed
        [FAIL]  Execute returns negative return code

    test/test_example.py::TestWhenExampleIsSkipped
        [SKIP]  Execute returns something

    test/test_example.py::TestExamplesWhenMethodUnderTestIsHighlighted
        [FAIL]  The (execute_command) returns negative return code
        [PASS]  The (execute_command) returns positive return code
        [SKIP]  The (execute_command) returns something

Highlight method under test
===========================
Simple test definition is required (double '__' characters before and after method)
to put method under test between '<>' characters e.g.
::

    def test__execute_method__returns_something(self):

may be displayed as:
::

    [PASS]  The (execute_command) returns something
    [FAIL]  The (execute_command) returns something
    [SKIP]  The (execute_command) returns something

This type of format provides clear information:

* which method is under test
* what kind of result should be expected

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

Copyright (C) 2014 Pawel Chomicki

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
