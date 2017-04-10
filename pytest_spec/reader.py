"""
:author: Pawel Chomicki
"""


class Reader(object):

    SPEC_TEST_FORMAT = 'SPEC_TEST_FORMAT'

    def read_spec_test_format(self, filepath):
        with open(filepath) as f:
            for index, line in enumerate(f.readlines()):
                if self.SPEC_TEST_FORMAT in line:
                    parts = line.split('=')
                    if len(parts) > 1:
                        return parts[1].strip()[1:-1]
                    if index > 100:
                        return None
