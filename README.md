<p>
    <h1 align="center">pytest-spec</h1>
    <p align="center">
        <img src="https://badgen.net/badge/python/2.7/green">
        <img src="https://badgen.net/badge/python/3.5/green">
        <img src="https://badgen.net/badge/python/3.6/green">
        <img src="https://badgen.net/badge/python/3.7/green">
        <img src="https://badgen.net/badge/python/3.8/green">
        <img src="https://badgen.net/badge/python/3.9/green">
    </p>
    <p align="center">
        <img src="https://badgen.net/badge/os/linux/blue">
        <img src="https://badgen.net/badge/os/windows/blue">
        <img src="https://badgen.net/badge/os/macos/blue">
    </p>
    <p align="center">
        <img src="https://badgen.net/badge/pytest/3.9.3/purple">
        <img src="https://badgen.net/badge/pytest/4.6.11/purple">
        <img src="https://badgen.net/badge/pytest/5.4.3/purple">
        <img src="https://badgen.net/badge/pytest/6.1.2/purple">
    </p>
    <p align="center">
        Library pytest-spec is a pytest plugin to display test execution output like a SPECIFICATION.
    </p>
</p>


## Available features

* Format output to look like specification.
* Group tests by classes and files
* Failed, passed and skipped are marked and colored.
* Remove test\_ and underscores for every test.
* It is possible to use docstring summary instead of test name.
* Supports function based, class based test.
* Supports describe like tests.


## Output example

![Example](https://github.com/pchomik/pytest-spec/raw/master/docs/output.gif)


## Configuration

### spec_header_format

You can configure the format of the test headers by specifying a [format string](https://docs.python.org/2/library/string.html#format-string-syntax) in your [ini-file](https://docs.pytest.org/en/stable/customize.html#pytest-ini):


```ini
    ; since pytest 4.6.x
    [pytest]
    spec_header_format = {module_path}:
    
    ; legacy pytest
    [tool:pytest]
    spec_header_format = {module_path}:
```

In addition to the ``{path}`` and ``{class_name}`` replacement fields, there is also ``{test_case}`` that holds a more human readable name.

### spec_test_format

You can configure the format of the test results by specifying a [format string](https://docs.python.org/2/library/string.html#format-string-syntax) in your [ini-file](https://docs.pytest.org/en/stable/customize.html#pytest-ini):

3 variables are available:
* result - place for indicator
* name - name of test
* docstring_summary - first line from test docstring if available

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_test_format = {result} {name}
    
    ; legacy pytest
    [tool:pytest]
    spec_test_format = {result} {name}
```

or

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_test_format = {result} {docstring_summary}
    
    ; legacy pytest
    [tool:pytest]
    spec_test_format = {result} {docstring_summary}
```

In second example where docstring is not available the name will be added to spec output.

### spec_success_indicator

You can configure the indicator displayed when test passed.

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_success_indicator = ✓

    ; legacy pytest
    [tool:pytest]
    spec_success_indicator = ✓
```

### spec_failure_indicator

You can configure the indicator displated when test failed.

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_failure_indicator = ✗

    ; legacy pytest
    [tool:pytest]
    spec_failure_indicator = ✗
```

### spec_skipped_indicator

You can configure the indicator displated when test is skipped.

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_skipped_indicator = ?

    ; legacy pytest
    [tool:pytest]
    spec_skipped_indicator = ?
```

### spec_ignore

Comma-separated settings to ignore/hide some tests or output from from plugins like FLAKE8 or ISORT.
Any test which contain provided string will be ignored in output spec.

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_ignore = FLAKE8

    ; legacy pytest
    [tool:pytest]
    spec_ignore = FLAKE8
```

### spec_indent

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_indent = "   "

    ; legacy pytest
    [tool:pytest]
    spec_indent = "   "
```

## Continuous Integration

[![Tests](https://github.com/pchomik/pytest-spec/workflows/test/badge.svg)](https://github.com/pchomik/pytest-spec/actions)


## Download

All versions of library are available on official [pypi server](https://pypi.org/project/pytest-spec/#history).

## Install

```sh
    pip install pytest-spec
```

## Contribution

Please feel free to present your idea by code example (pull request) or reported issues.

## Contributors

* [@0x64746b](https://github.com/0x64746b)
* [@lucasmarshall](https://github.com/lucasmarshall)
* [@amcgregor](https://github.com/amcgregor)
* [@jhermann](https://github.com/jhermann)
* [@frenzymadness](https://github.com/frenzymadness)
* [@chrischambers](https://github.com/chrischambers)
* [@maxalbert](https://github.com/maxalbert)
* [@jayvdb](https://github.com/jayvdb)

## License

pytest-spec - pytest plugin to display test execution output like a SPECIFICATION.

Copyright (C) 2014-2021 Pawel Chomicki

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
