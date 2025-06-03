<p>
    <h1 align="center">pytest-spec</h1>
    <p align="center">
        <img src="https://badgen.net/badge/python/3.9/green">
        <img src="https://badgen.net/badge/python/3.10/green">
        <img src="https://badgen.net/badge/python/3.11/green">
        <img src="https://badgen.net/badge/python/3.12/green">
        <img src="https://badgen.net/badge/python/3.13/green">
    </p>
    <p align="center">
        <img src="https://badgen.net/badge/os/linux/blue">
        <img src="https://badgen.net/badge/os/windows/blue">
        <img src="https://badgen.net/badge/os/macos/blue">
    </p>
    <p align="center">
        <img src="https://badgen.net/badge/pytest/4.6.11/purple">
        <img src="https://badgen.net/badge/pytest/5.4.3/purple">
        <img src="https://badgen.net/badge/pytest/6.2.5/purple">
        <img src="https://badgen.net/badge/pytest/7.4.4/purple">
        <img src="https://badgen.net/badge/pytest/8.4.0/purple">
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

<details>

<summary>spec_header_format</summary>

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

or in your [pyproject.toml](https://docs.pytest.org/en/stable/reference/customize.html#pyproject-toml) file:

```toml
    [tool.pytest.ini_options]
    spec_header_format = "{module_path}:"
```

In addition to the ``{path}`` and ``{class_name}`` replacement fields, there is also ``{test_case}`` that holds a more human readable name.

</details>

<details>

<summary>spec_test_format</summary>

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

Similar configuration could be done in your [pyproject.toml](https://docs.pytest.org/en/stable/reference/customize.html#pyproject-toml) file:

```toml
    [tool.pytest.ini_options]
    spec_test_format = "{result} {name}"
```

or

```toml
    [tool.pytest.ini_options]
    spec_test_format = "{result} {docstring_summary}"
```

</details>


<details>

<summary>spec_success_indicator</summary>

### spec_success_indicator

You can configure the indicator displayed when test passed.

*ini-file*

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_success_indicator = ✓

    ; legacy pytest
    [tool:pytest]
    spec_success_indicator = ✓
```

*or pyproject.toml*

```toml
    [tool.pytest.ini_options]
    spec_success_indicator = "✓"
```

</details>

<details>

<summary>spec_failure_indicator</summary>

### spec_failure_indicator

You can configure the indicator displated when test failed.

*ini-file*

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_failure_indicator = ✗

    ; legacy pytest
    [tool:pytest]
    spec_failure_indicator = ✗
```

or *pyproject.toml*

```toml
    [tool.pytest.ini_options]
    spec_failure_indicator = "✗"
```

</details>

<details>

<summary>spec_skipped_indicator</summary>

### spec_skipped_indicator

You can configure the indicator displated when test is skipped.

*ini-file*

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_skipped_indicator = »

    ; legacy pytest
    [tool:pytest]
    spec_skipped_indicator = »
```

or *pyproject.toml*

```toml
    [tool.pytest.ini_options]
    spec_skipped_indicator = "»"
```

</details>

<details>

<summary>spec_ignore</summary>

### spec_ignore

Comma-separated settings to ignore/hide some tests or output from from plugins like FLAKE8 or ISORT.
Any test which contain provided string will be ignored in output spec.

*ini-file*

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_ignore = FLAKE8

    ; legacy pytest
    [tool:pytest]
    spec_ignore = FLAKE8
```

or *pyproject.toml*

```toml
    [tool.pytest.ini_options]
    spec_ignore = "FLAKE8"
```

</details>

<details>

<summary>spec_indent</summary>

### spec_indent

*ini-file*

```ini
    ; since pytest 4.6.x
    [pytest]
    spec_indent = "   "

    ; legacy pytest
    [tool:pytest]
    spec_indent = "   "
```

or *pyproject.toml*

```toml
    [tool.pytest.ini_options]
    spec_indent = "   "
```

</details>

## Continuous Integration

[![Tests](https://github.com/pchomik/pytest-spec/workflows/test/badge.svg)](https://github.com/pchomik/pytest-spec/actions)


## Download

All versions of library are available on official [pypi server](https://pypi.org/project/pytest-spec/#history).

## Install

### From [pypi.org](https://pypi.org)

```sh
    pip install pytest-spec
```

### From source

```sh
    cd pytest-spec
    uv sync
```

### From source for testing

```sh
    cd pytest-spec
    uv sync --all-extras --dev
```

### From source for build or deployment

```sh
    cd pytest-spec
    uv sync
    uv build
    uv publish
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
* [@hugovk](https://github.com/hugovk)
* [@b0g3r](https://github.com/b0g3r)
* [@paxcodes](https://github.com/paxcodes)
* [@s-t-e-v-e-n-k](https://github.com/s-t-e-v-e-n-k)
* [@yk-kd](https://github.com/yk-kd)


## License

pytest-spec - pytest plugin to display test execution output like a SPECIFICATION.

Copyright (C) 2014-2025 Pawel Chomicki

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
