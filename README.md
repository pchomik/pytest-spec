pytest-spec
===========
pytest plugin to display test execution output like a SPECIFICATION.


Available features
==================
* Format output to look like specification.
* Group tests by classes.
* Failed, passed and skipped are marked and colored.
* Remove test_ and underscores for every test.

Output example
==============

    py.test --spec

    test/test_plugin.py::TestPlugin
        [PASS]  Pytest adoption adds spec option
        [PASS]  Pytest adoption gets general group
        [FAIL]  Should be failed

    test/test_plugin.py::TestPlugin2
        [SKIP]  Should be skipped

    test/test_plugin.py::TestPlugin3
        [PASS]  Should be passed when is subclassed

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

Copyright (C) 2012 Pawel Chomicki

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
