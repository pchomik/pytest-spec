"""some documentation"""
import pytest
import unittest


SPEC_TEST_FORMAT = '[{result}]  {name} {p0} is installed'


@pytest.mark.parametrize("name,version", [
    ("pip", "9.0.1"),
    ("pep8", "1.7.0"),
])
def test_package(Package, name, version):
    """Test format:  1111"""
    assert Package(name, version).is_installed
    assert version in Package(name, version).version


if __name__ == '__main__':
    unittest.main()
